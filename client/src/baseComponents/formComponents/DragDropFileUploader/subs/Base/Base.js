import { useState, useEffect, useRef } from "react";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

const Base = ({
  setFile,
  openFileBrowser = false,
  setOpenFileBrowser,
  draggableElement,
  whileDraggingElement,
  multipleFileUploader,
  whileDraggingElementClassName,
  mainContainerClassName,
  acceptableFileType = ".jpg,.jpeg,.png",
  inputId = "draggableFileUploaderId",
  inputName = "file_name",
}) => {
  const inputRef = useRef();

  const [dragActive, setDragActive] = useState(false);

  const handleContainerClick = () => {
    if (inputRef.current) {
      inputRef.current.click();
    }
  };

  const handleDrag = function (e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = function (e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files);
    }
  };

  const handleChange = function (e) {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files);
    }
  };

  useEffect(() => {
    if (openFileBrowser) {
      inputRef.current.click();
      setTimeout(() => {
        setOpenFileBrowser(false);
      }, 500);
    }
  }, [openFileBrowser]);

  return (
    <>
      <Div
        className={cx("pos-rel", mainContainerClassName)}
        onClick={handleContainerClick}
        onDragEnter={handleDrag}
        onSubmit={(e) => e.preventDefault()}
      >
        <input
          ref={inputRef}
          type="file"
          className="no-display"
          accept={acceptableFileType}
          multiple={multipleFileUploader}
          onChange={handleChange}
          id={inputId}
          name={inputName}
        />
        {draggableElement && draggableElement()}
        {dragActive && (
          <Div
            className={cx(whileDraggingElementClassName)}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {whileDraggingElement && whileDraggingElement()}
          </Div>
        )}
      </Div>
    </>
  );
};

export default Base;
