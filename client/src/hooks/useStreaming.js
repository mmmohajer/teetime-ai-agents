import { useEffect, useRef, useState } from "react";
import {
  ICE_SERVER_DOMAIN,
  APP_DOMAIN,
  TURN_USER_NAME,
  TURN_USER_PASSWORD,
} from "config";

// 🔹 Helper: generate a black video track (canvas kept alive)
const createBlackVideoTrack = ({ width = 640, height = 480 } = {}) => {
  const canvas = Object.assign(document.createElement("canvas"), {
    width,
    height,
  });
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, width, height);
  const stream = canvas.captureStream(5); // 5 FPS black frames
  const track = stream.getVideoTracks()[0];
  return { track, canvas };
};

// 🔹 Helper: generate a silent audio track
const createSilentAudioTrack = () => {
  const ctx = new AudioContext();
  const oscillator = ctx.createOscillator();
  const dst = oscillator.connect(ctx.createMediaStreamDestination());
  oscillator.start();
  const track = dst.stream.getAudioTracks()[0];
  return track;
};

// 🔹 Robustly find video sender (works even if sender.track is null)
const getVideoSender = (pubHandle) => {
  const pc = pubHandle?.webrtcStuff?.pc;
  if (!pc) return null;

  let sender = pc.getSenders().find((s) => s?.track?.kind === "video");
  if (sender) return sender;

  if (typeof pc.getTransceivers === "function") {
    const tx = pc.getTransceivers().find((t) => {
      const k1 = t?.sender?.track?.kind;
      const k2 = t?.receiver?.track?.kind;
      return k1 === "video" || k2 === "video";
    });
    if (tx?.sender) return tx.sender;
  }
  return null;
};

// 🔹 Replace track inside PeerConnection
const replaceVideoTrack = (newTrack, pubHandle) => {
  const sender = getVideoSender(pubHandle);
  if (sender) sender.replaceTrack(newTrack);
};

const useStreaming = ({ roomId, replaceWithBlackTrack = false }) => {
  const localVideoRef = useRef(null);
  const localStreamRef = useRef(null);
  const remoteHandlesRef = useRef({});
  const remoteStreamsRef = useRef({});
  const feedMidsRef = useRef({});
  const myIdRef = useRef(null);
  const startedRef = useRef(false);
  const pubRef = useRef(null);

  const [remoteFeeds, setRemoteFeeds] = useState([]);
  const [audioEnabled, setAudioEnabled] = useState(true);
  const [videoEnabled, setVideoEnabled] = useState(true);
  const [allMuted, setAllMuted] = useState(false);

  const ICE_SERVERS = [
    // { urls: "stun:stun.l.google.com:19302" },
    {
      urls: `turn:${ICE_SERVER_DOMAIN}:3478?transport=udp`,
      username: TURN_USER_NAME,
      credential: TURN_USER_PASSWORD,
    },
    {
      urls: `turn:${ICE_SERVER_DOMAIN}:5349?transport=tcp`,
      username: TURN_USER_NAME,
      credential: TURN_USER_PASSWORD,
    },
  ];

  const JANUS_SERVER = `wss://${APP_DOMAIN}/janus`;

  useEffect(() => {
    if (startedRef.current) return;
    startedRef.current = true;

    if (!window.Janus) {
      console.error("❌ Janus.js not loaded");
      return;
    }

    let janus = null;

    const extractMids = (publisher) => {
      const mids = (publisher?.streams || [])
        .filter((s) => s.type === "video" || s.type === "audio")
        .map((s) => s.mid?.toString())
        .filter(Boolean);
      return mids.length ? mids : ["0", "1"];
    };

    window.Janus.init({
      debug: ["error"],
      callback: () => {
        janus = new window.Janus({
          server: JANUS_SERVER,
          iceServers: ICE_SERVERS,
          success: () => {
            janus.attach({
              plugin: "janus.plugin.videoroom",
              success: (handle) => {
                pubRef.current = handle;

                // 🔹 First try to create the room
                handle.send({
                  message: {
                    request: "create",
                    room: parseInt(roomId, 10), // Janus expects numbers
                    description: `Room ${roomId}`,
                    publishers: 20,
                  },
                  success: (result) => {
                    // Now join the room
                    handle.send({
                      message: {
                        request: "join",
                        room: parseInt(roomId, 10),
                        ptype: "publisher",
                        display: `user-${Math.floor(Math.random() * 1000)}`,
                      },
                    });
                  },
                  error: (err) => {
                    console.warn("⚠️ Room creation failed, maybe exists:", err);

                    // Still attempt join anyway
                    handle.send({
                      message: {
                        request: "join",
                        room: parseInt(roomId, 10),
                        ptype: "publisher",
                        display: `user-${Math.floor(Math.random() * 1000)}`,
                      },
                    });
                  },
                });

                // Once joined, publish local stream
                navigator.mediaDevices
                  .getUserMedia({
                    video: true,
                    audio: { echoCancellation: true, noiseSuppression: true },
                  })
                  .then((stream) => {
                    localStreamRef.current = stream;
                    stream
                      .getAudioTracks()
                      .forEach((t) => (t.enabled = audioEnabled));
                    stream
                      .getVideoTracks()
                      .forEach((t) => (t.enabled = videoEnabled));

                    if (localVideoRef.current)
                      localVideoRef.current.srcObject = stream;

                    handle.createOffer({
                      media: { audio: true, video: true },
                      trickle: true,
                      success: (jsep) =>
                        handle.send({ message: { request: "publish" }, jsep }),
                      error: (err) =>
                        console.error("❌ Publisher createOffer error:", err),
                    });
                  })
                  .catch((e) => console.error("❌ getUserMedia failed:", e));
              },

              onmessage: (msg, jsep) => {
                const evt = msg.videoroom;
                if (evt === "joined") {
                  myIdRef.current = msg.id;
                  (msg.publishers || []).forEach((p) => {
                    if (p.id !== myIdRef.current) {
                      feedMidsRef.current[p.id] = extractMids(p);
                      subscribeToFeed(p.id);
                    }
                  });
                }
                if (evt === "event") {
                  if (msg.publishers) {
                    msg.publishers.forEach((p) => {
                      if (p.id !== myIdRef.current) {
                        feedMidsRef.current[p.id] = extractMids(p);
                        subscribeToFeed(p.id);
                      }
                    });
                  }
                  if (msg.unpublished || msg.leaving)
                    cleanupFeed(msg.unpublished || msg.leaving);
                }
                if (jsep && jsep.type === "answer") {
                  pubRef.current?.handleRemoteJsep({ jsep });
                }
              },

              error: (err) => console.error("❌ Publisher attach error:", err),
            });
          },
          error: (err) => console.error("❌ Janus init error:", err),
        });
      },
    });

    const subscribeToFeed = (feedId) => {
      if (
        !janus ||
        feedId === myIdRef.current ||
        remoteHandlesRef.current[feedId]
      )
        return;
      janus.attach({
        plugin: "janus.plugin.videoroom",
        success: (sub) => {
          remoteHandlesRef.current[feedId] = sub;
          sub.send({
            message: {
              request: "join",
              room: parseInt(roomId, 10),
              ptype: "subscriber",
              feed: feedId,
            },
          });
        },
        onmessage: (msg, jsep) => {
          if (
            msg.videoroom === "event" &&
            (msg.unpublished || msg.leaving || msg.error_code === 428)
          ) {
            cleanupFeed(feedId);
          }
          if (jsep && jsep.type === "offer") {
            const sub = remoteHandlesRef.current[feedId];
            if (!sub) return;
            sub.createAnswer({
              jsep,
              media: { audioSend: false, videoSend: false },
              trickle: true,
              success: (jsepAnswer) =>
                sub.send({
                  message: { request: "start", room: parseInt(roomId, 10) },
                  jsep: jsepAnswer,
                }),
              error: (err) =>
                console.error("❌ Subscriber createAnswer error:", err),
            });
          }
        },
        onremotetrack: (track, mid, on) => {
          let stream = remoteStreamsRef.current[feedId];
          if (!on) {
            if (stream) {
              stream.getTracks().forEach((t) => {
                if (t.id === track.id) stream.removeTrack(t);
              });
              if (stream.getTracks().length === 0) cleanupFeed(feedId);
              else setRemoteFeeds((prev) => [...prev]);
            }
            return;
          }
          if (!stream) {
            stream = new MediaStream();
            remoteStreamsRef.current[feedId] = stream;
            setRemoteFeeds((prev) =>
              prev.find((f) => f.id === String(feedId))
                ? prev
                : [...prev, { id: String(feedId), stream }]
            );
          }
          if (!stream.getTracks().some((t) => t.id === track.id)) {
            stream.addTrack(track);
            setRemoteFeeds((prev) => [...prev]);
          }
        },
        oncleanup: () => cleanupFeed(feedId),
        error: (err) => console.error("❌ Subscriber attach error:", err),
      });
    };

    const cleanupFeed = (feedId) => {
      setRemoteFeeds((prev) => prev.filter((f) => f.id !== String(feedId)));
      const stream = remoteStreamsRef.current[feedId];
      if (stream) {
        stream.getTracks().forEach((t) => t.stop());
        delete remoteStreamsRef.current[feedId];
      }
      const sub = remoteHandlesRef.current[feedId];
      if (sub) {
        try {
          sub.hangup();
          sub.detach();
        } catch {}
        delete remoteHandlesRef.current[feedId];
      }
      delete feedMidsRef.current[feedId];
    };

    return () => {
      try {
        Object.keys(remoteHandlesRef.current).forEach((id) => {
          try {
            remoteHandlesRef.current[id].hangup();
            remoteHandlesRef.current[id].detach();
          } catch {}
        });
        Object.values(remoteStreamsRef.current).forEach((s) =>
          s.getTracks().forEach((t) => t.stop())
        );
        pubRef.current?.hangup?.();
        pubRef.current?.detach?.();
        janus?.destroy?.();
      } catch {}
    };
  }, [roomId]);

  // Toggle audio
  const toggleAudio = () => {
    setAudioEnabled((prev) => {
      const newVal = !prev;
      if (localStreamRef.current) {
        localStreamRef.current
          .getAudioTracks()
          .forEach((t) => (t.enabled = newVal));
      }
      pubRef.current?.send({
        message: { request: "configure", audio: newVal },
      });
      return newVal;
    });
  };

  // Toggle video with black replacement
  const toggleVideo = () => {
    setVideoEnabled((prev) => {
      const newVal = !prev;
      const pc = pubRef.current?.webrtcStuff?.pc;

      if (localStreamRef.current && pc) {
        const current = localStreamRef.current.getVideoTracks()[0];

        if (!newVal && replaceWithBlackTrack) {
          const { track: blackTrack, canvas } = createBlackVideoTrack();
          replaceVideoTrack(blackTrack, pubRef.current);

          if (current) {
            localStreamRef.current.removeTrack(current);
            current.stop();
          }
          localStreamRef.current.addTrack(blackTrack);

          if (localVideoRef.current)
            localVideoRef.current.srcObject = localStreamRef.current;
          pubRef.current.send({
            message: { request: "configure", video: true },
          });

          setTimeout(() => canvas.remove(), 0);
        } else if (newVal && replaceWithBlackTrack) {
          navigator.mediaDevices
            .getUserMedia({ video: true })
            .then((stream) => {
              const camTrack = stream.getVideoTracks()[0];
              replaceVideoTrack(camTrack, pubRef.current);

              if (current) {
                localStreamRef.current.removeTrack(current);
                current.stop();
              }
              localStreamRef.current.addTrack(camTrack);

              if (localVideoRef.current)
                localVideoRef.current.srcObject = localStreamRef.current;
              pubRef.current.send({
                message: { request: "configure", video: true },
              });

              stream.getTracks().forEach((t) => {
                if (t !== camTrack) t.stop();
              });
            })
            .catch((err) => {
              console.error("❌ Camera restore failed:", err);
              const { track: blackTrack } = createBlackVideoTrack();
              replaceVideoTrack(blackTrack, pubRef.current);
              localStreamRef.current.addTrack(blackTrack);
            });
        } else {
          localStreamRef.current
            .getVideoTracks()
            .forEach((t) => (t.enabled = newVal));
          pubRef.current.send({
            message: { request: "configure", video: newVal },
          });
        }
      }
      return newVal;
    });
  };

  const toggleRemoteAudio = () => {
    setAllMuted((prev) => {
      const newVal = !prev;
      setRemoteFeeds((feeds) => {
        feeds.forEach(({ stream }) => {
          stream.getAudioTracks().forEach((t) => (t.enabled = !newVal));
        });
        return [...feeds];
      });
      return newVal;
    });
  };

  return {
    localVideoRef,
    remoteFeeds,
    audioEnabled,
    videoEnabled,
    toggleAudio,
    toggleVideo,
    allMuted,
    toggleRemoteAudio,
  };
};

export default useStreaming;
