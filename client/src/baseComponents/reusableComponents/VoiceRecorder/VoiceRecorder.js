import { useState, useEffect, useRef } from "react";

const VoiceRecorder = ({
  onChunk,
  onComplete,
  recording = false,
  setRecording = null,
  chunkDurationInSecond = 15,
}) => {
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioContextRef = useRef(null);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        sampleRate: 16000, // Best for STT models like Whisper/Google
        channelCount: 1, // Mono (saves bandwidth, STT doesn’t need stereo)
        noiseSuppression: true, // Browser-level background noise filter
        echoCancellation: true, // Prevents feedback from speakers
        autoGainControl: false, // We'll handle gain manually
      },
    });

    // --- Setup Web Audio pipeline ---
    audioContextRef.current = new (window.AudioContext ||
      window.webkitAudioContext)({ sampleRate: 16000 });
    const source = audioContextRef.current.createMediaStreamSource(stream);

    // Gain (boost soft voices)
    const gainNode = audioContextRef.current.createGain();
    gainNode.gain.value = 1.5; // Adjust boost (1.0 = normal, 2.0 = +100%)

    // Compressor (smooth loud/quiet parts)
    const compressor = audioContextRef.current.createDynamicsCompressor();
    compressor.threshold.setValueAtTime(
      -40,
      audioContextRef.current.currentTime
    );
    compressor.knee.setValueAtTime(30, audioContextRef.current.currentTime);
    compressor.ratio.setValueAtTime(12, audioContextRef.current.currentTime);
    compressor.attack.setValueAtTime(
      0.005,
      audioContextRef.current.currentTime
    );
    compressor.release.setValueAtTime(
      0.25,
      audioContextRef.current.currentTime
    );

    // Destination for processed audio
    const destination = audioContextRef.current.createMediaStreamDestination();

    // Connect chain: Mic → Gain → Compressor → Destination
    source.connect(gainNode).connect(compressor).connect(destination);

    // --- Setup MediaRecorder ---
    mediaRecorderRef.current = new MediaRecorder(destination.stream, {
      mimeType: "audio/webm;codecs=opus",
      audioBitsPerSecond: 128000, // 128kbps = good balance of quality/size
    });

    audioChunksRef.current = [];

    // Capture chunks
    mediaRecorderRef.current.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunksRef.current.push(event.data);
        if (onChunk) {
          onChunk(event.data); // live chunk for streaming to backend
        }
      }
    };

    // Final blob on stop
    mediaRecorderRef.current.onstop = () => {
      const audioBlob = new Blob(audioChunksRef.current, {
        type: "audio/webm",
      });
      if (onComplete) {
        onComplete(audioBlob); // full audio for backup/upload
      }
      audioChunksRef.current = [];
      audioContextRef.current.close();
      audioContextRef.current = null;
    };

    mediaRecorderRef.current.start(chunkDurationInSecond * 1000); // chunk size
    setRecording?.(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setRecording?.(false);
    mediaRecorderRef.current = null;
  };

  useEffect(() => {
    if (recording && !mediaRecorderRef.current) {
      startRecording();
    } else if (!recording && mediaRecorderRef.current) {
      stopRecording();
    }
  }, [recording]);

  return null; // no UI here, controlled externally
};

export default VoiceRecorder;
