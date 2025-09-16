import Div from "@/baseComponents/reusableComponents/Div";
import AppVideo from "@/baseComponents/reusableComponents/AppVideo";

import useStreaming from "@/hooks/useStreaming";

const DisplayStreaming = ({ roomId = 1234 }) => {
  const {
    localVideoRef,
    remoteFeeds,
    audioEnabled,
    videoEnabled,
    toggleAudio,
    toggleVideo,
  } = useStreaming({ roomId });

  return (
    <Div>
      <video
        ref={localVideoRef}
        autoPlay
        muted
        playsInline
        style={{ width: 300, border: "2px solid green" }}
      />

      <div className="m-all-32">
        <button onClick={toggleAudio} className="m-r-16">
          {audioEnabled ? "Mute" : "Unmute"}
        </button>
        <button onClick={toggleVideo}>
          {videoEnabled ? "Hide Video" : "Show Video"}
        </button>
      </div>

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        {remoteFeeds.map(({ id, stream }) => (
          <video
            key={id}
            autoPlay
            playsInline
            style={{ width: 300, border: "2px solid red" }}
            ref={(el) => {
              if (el && stream && el.srcObject !== stream)
                el.srcObject = stream;
            }}
          />
        ))}
      </div>
    </Div>
  );
};

export default DisplayStreaming;
