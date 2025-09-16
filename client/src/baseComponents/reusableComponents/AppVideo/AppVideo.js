const AppVideo = ({ width, height, src, ...props }) => {
  return (
    <>
      <video width={width} height={height} controls {...props}>
        <source src={src} />
        Your browser does not support the video tag.
      </video>
    </>
  );
};

export default AppVideo;
