import { useState, useEffect } from "react";
import cx from "classnames";
import ReactCrop from "react-image-crop";

import Div from "@/baseComponents/reusableComponents/Div";
import AppImage from "@/baseComponents/reusableComponents/AppImage";
import Button from "@/baseComponents/reusableComponents/Button";

import useDivWidth from "@/hooks/useDivWidth";

import "react-image-crop/dist/ReactCrop.css";

import { cropImage, getCroppedImg } from "../utils";
import { CANVAS_ID, IMAGE_CROPPER_ID, CROPPER_ID } from "../constants";
import styles from "./Cropper.module.scss";

const Cropper = ({
  src,
  setSrc,
  setFile,
  fileName,
  setShowCropper,
  cropInfo,
  naturalWidth,
  naturalHeight,
}) => {
  const { containerRef, width } = useDivWidth();

  const aspect = cropInfo?.aspect || 1;
  const minWidth = cropInfo?.minWidth || 0;
  const minHeight = cropInfo?.minHeight || 0;
  const maxWidth = cropInfo?.maxWidth || 200;
  const maxHeight = cropInfo?.maxHeight || 200;

  const [imgWidth, setImgWidth] = useState(0);
  const [crop, setCrop] = useState();
  const [showSubmit, setShowSubmit] = useState(false);

  const doCrop = () => {
    return new Promise(function (resolve, reject) {
      const cropped = cropImage(src, crop.x, crop.y, crop.width, crop.height);
      setTimeout(() => {
        if (cropped) {
          resolve("Stuff worked!");
        } else {
          reject(Error("It broke"));
        }
      }, 1000);
    });
  };

  const cropHandler = (e) => {
    e.preventDefault();
    if (crop?.width) {
      doCrop().then(() => {
        setFile(getCroppedImg(setSrc, fileName));
        setShowCropper(false);
      });
    }
  };

  useEffect(() => {
    if (width >= naturalWidth) {
      setImgWidth(naturalWidth);
    } else {
      setImgWidth(width);
    }
  }, [width, naturalWidth]);

  return (
    <>
      <Div
        type="flex"
        hAlign="center"
        // vAlign="center"
        className="pos-fix pos-fix--lt width-per-100 height-vh-full bg-black text-white of-y-auto scroll-type-one p-all-temp-10"
        style={{ zIndex: 1000000000000000 }}
      >
        <Div ref={containerRef} className="width-per-100">
          <Div
            type="flex"
            hAlign="center"
            direction="vertical"
            className="width-per-100"
            id={CROPPER_ID}
          >
            {!showSubmit ? (
              <>
                <Div className="">
                  <AppImage
                    src={src}
                    objectFit="contain"
                    width={imgWidth}
                    height={(imgWidth * naturalHeight) / naturalWidth}
                  />
                </Div>

                <Div className="width-per-100 max-width-px-300 m-l-auto m-r-auto m-y-10">
                  <Button
                    className="width-per-100"
                    onClick={(e) => {
                      e.preventDefault();
                      setCrop({
                        width: minWidth,
                        height: minWidth / aspect,
                        x: 0,
                        y: 0,
                        unit: "px",
                      });
                      setShowSubmit(true);
                    }}
                    btnText={"Start Cropping"}
                  />
                </Div>

                <Div className="width-per-100 max-width-px-300 m-l-auto m-r-auto m-b-10">
                  <Button
                    btnType={2}
                    onClick={() => setShowCropper(false)}
                    btnText="Dismiss"
                  />
                </Div>
              </>
            ) : (
              ""
            )}

            {showSubmit && (
              <>
                <ReactCrop
                  aspect={aspect}
                  minWidth={minWidth}
                  minHeight={minHeight}
                  maxWidth={maxWidth}
                  maxHeight={maxHeight}
                  crop={crop}
                  onChange={(c) => {
                    setCrop(c);
                  }}
                  className=""
                >
                  <Div>
                    <AppImage
                      src={src}
                      objectFit="contain"
                      id={IMAGE_CROPPER_ID}
                      width={imgWidth}
                      height={(imgWidth * naturalHeight) / naturalWidth}
                    />
                  </Div>
                </ReactCrop>
                <Div className="width-per-100 max-width-px-300 m-l-auto m-r-auto">
                  <Button
                    btnType={1}
                    isDisabled={crop?.width <= cropInfo?.minWidth}
                    className={cx("m-y-10")}
                    onClick={cropHandler}
                    btnText="Apply Changes"
                  />
                </Div>
                <Div className="width-per-100 max-width-px-300 m-l-auto m-r-auto m-b-10">
                  <Button
                    btnType={2}
                    onClick={() => setShowCropper(false)}
                    btnText="Discard Changes"
                  />
                </Div>
              </>
            )}
          </Div>
        </Div>
        <Div className={cx(styles.canvasContainer)}>
          <canvas id={CANVAS_ID} className=""></canvas>
        </Div>
      </Div>
    </>
  );
};

export default Cropper;
