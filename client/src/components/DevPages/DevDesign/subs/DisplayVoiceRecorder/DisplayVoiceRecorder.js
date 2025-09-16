import { useState, useEffect } from "react";
import VoiceRecorder from "@/baseComponents/reusableComponents/VoiceRecorder/VoiceRecorder";

import Div from "@/baseComponents/reusableComponents/Div";
import Heading from "@/baseComponents/reusableComponents/Heading";
import Button from "@/baseComponents/reusableComponents/Button";

const DisplayVoiceRecorder = () => {
  const [chunks, setChunks] = useState([]);
  const [fullAudio, setFullAudio] = useState(null);
  const [recording, setRecording] = useState(false);
  const [chunkUrls, setChunkUrls] = useState([]);
  const [fullAudioUrl, setFullAudioUrl] = useState(null);

  useEffect(() => {
    // Create URLs for chunks
    const urls = chunks.map((chunk) => URL.createObjectURL(chunk));
    setChunkUrls(urls);
    // Cleanup old URLs
    return () => {
      urls.forEach((url) => URL.revokeObjectURL(url));
    };
  }, [chunks]);

  useEffect(() => {
    if (fullAudio) {
      const url = URL.createObjectURL(fullAudio);
      setFullAudioUrl(url);
      return () => URL.revokeObjectURL(url);
    } else {
      setFullAudioUrl(null);
    }
  }, [fullAudio]);

  return (
    <Div>
      <VoiceRecorder
        onChunk={(chunk) => setChunks((prev) => [...prev, chunk])}
        onComplete={(blob) => setFullAudio(blob)}
        recording={recording}
        setRecording={setRecording}
      />
      <Button
        btnText={recording ? "Stop Recording" : "Start Recording"}
        onClick={() => setRecording(!recording)}
      />
      {/* Audio Players */}
      <Div style={{ marginTop: 24 }}>
        <Heading type={4}>Full Recording</Heading>
        {fullAudioUrl && <audio controls src={fullAudioUrl} />}
      </Div>
      <Div style={{ marginTop: 24 }}>
        <Heading type={4}>Audio Chunks</Heading>
        {chunkUrls.map((url, idx) => (
          <Div key={idx} style={{ marginBottom: 8 }}>
            <span>Chunk {idx + 1}: </span>
            <audio controls src={url} />
          </Div>
        ))}
      </Div>
    </Div>
  );
};

export default DisplayVoiceRecorder;
