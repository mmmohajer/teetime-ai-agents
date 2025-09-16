import { useState, useRef, useEffect } from "react";
import cx from "classnames";

import { APP_DOMAIN_FOR_SERVER_SIDE_PROPS } from "config";

import ImagePicker from "./subs/ImagePicker";
import VideoPicker from "./subs/VideoPicker";
import Cropper from "./subs/Cropper";
import Resizer from "./subs/Resizer";

const MediaPicker = ({
  label,
  isRequired,
  setFile,
  hasCropper = true,
  cropInfo,
  hasResizer = false,
  maxWidth,
  type = "default",
  initialSrc = "",
  setInitialSrc,
  initialSrcComesFromOurServer = false,
  previewer = "default",
  className,
  hasMarginBottom,
  fileType = "image",
}) => {
  const inputFileField = useRef();

  const [src, setSrc] = useState("");
  const [fileName, setFileName] = useState("");
  const [showCropper, setShowCropper] = useState(false);
  const [showResizer, setShowResizer] = useState(false);
  const [naturalWidth, setNaturalWidth] = useState(0);
  const [naturalHeight, setNaturalHeight] = useState(0);

  useEffect(() => {
    if (initialSrc) {
      if (initialSrcComesFromOurServer) {
        setSrc(`${APP_DOMAIN_FOR_SERVER_SIDE_PROPS}${initialSrc}`);
      } else {
        setSrc(initialSrc);
      }
    }
  }, [initialSrc]);

  const fileChangeHandler = (e) => {
    if (e.target?.files?.[0]) {
      const localFile = e.target.files[0];
      setFile(localFile);
      setFileName(localFile?.name);
      if (setInitialSrc) {
        setInitialSrc("");
      }
      const objectUrl = URL.createObjectURL(localFile);
      setSrc(objectUrl);
      setShowCropper(true);
      if (hasResizer) {
        setShowResizer(true);
      }
      //
      const img = new Image();
      img.onload = () => {
        const actualWidth = img?.naturalWidth;
        const actualHeight = img?.naturalHeight;
        if (!hasResizer) {
          setNaturalWidth(actualWidth || 0);
          setNaturalHeight(actualHeight || 0);
        } else {
          if (actualWidth > maxWidth) {
            setNaturalWidth(maxWidth || 0);
            setNaturalHeight((maxWidth * actualHeight) / actualWidth || 0);
          } else {
            setNaturalWidth(actualWidth || 0);
            setNaturalHeight(actualHeight || 0);
          }
        }
      };
      img.src = objectUrl;
    }
  };

  return (
    <>
      {hasResizer && showResizer ? (
        <Resizer
          src={src}
          setSrc={setSrc}
          setFile={setFile}
          fileName={fileName}
          setShowResizer={setShowResizer}
          maxWidth={maxWidth}
        />
      ) : (
        ""
      )}

      {fileType === "image" && hasCropper && showCropper && !showResizer ? (
        <Cropper
          src={src}
          setSrc={setSrc}
          setFile={setFile}
          fileName={fileName}
          setShowCropper={setShowCropper}
          cropInfo={cropInfo}
          mainMaxWidth={maxWidth}
          naturalWidth={naturalWidth}
          naturalHeight={naturalHeight}
        />
      ) : (
        ""
      )}
      {fileType === "image" && type === "default" ? (
        <ImagePicker
          label={label}
          isRequired={isRequired}
          fileChangeHandler={fileChangeHandler}
          src={src}
          setSrc={setSrc}
          setFile={setFile}
          setFileName={setFileName}
          inputFileField={inputFileField}
          className={cx(className)}
          setInitialSrc={setInitialSrc}
          previewer={previewer}
          hasMarginBottom={hasMarginBottom}
        />
      ) : (
        ""
      )}

      {fileType === "video" && type === "default" ? (
        <VideoPicker
          label={label}
          isRequired={isRequired}
          fileChangeHandler={fileChangeHandler}
          src={src}
          setSrc={setSrc}
          setFile={setFile}
          setFileName={setFileName}
          inputFileField={inputFileField}
          className={cx(className)}
          setInitialSrc={setInitialSrc}
          previewer={previewer}
          hasMarginBottom={hasMarginBottom}
        />
      ) : (
        ""
      )}
    </>
  );
};

export default MediaPicker;
