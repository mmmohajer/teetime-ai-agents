import { useState, useEffect, useCallback } from "react";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Label from "@/baseComponents/formComponents/Label";

import Base from "./subs/Base";
import Type1 from "./subs/Type1";

const DragDropFileUploader = ({
  file,
  setFile,
  acceptableFileType,
  inputId = "DragDropFileUploaderId",
  acceptableFileString = "",
  iconType = "angles-right",
  type = 1,
  label = "",
  isRequired = false,
}) => {
  const [openFileBrowser, setOpenFileBrowser] = useState();
  const [inputName, setInputName] = useState("");

  const removeFileClickHandler = useCallback(() => {
    setFile(null);
    const inputFileFiled = document.getElementById(inputId);
    inputFileFiled.value = null;
  }, []);

  const draggableElement = () => {
    if (type === 1) {
      return (
        <Type1
          file={file}
          iconType={iconType}
          setOpenFileBrowser={setOpenFileBrowser}
          acceptableFileString={acceptableFileString}
          removeFileClickHandler={removeFileClickHandler}
        />
      );
    }
  };

  useEffect(() => {
    if (file) {
      Object.keys(file || {})?.forEach((key) => {
        setInputName(file[key]?.name);
      });
    }
  }, [file]);

  return (
    <>
      {label && <Label className="" label={label} isRequired={isRequired} />}
      <Div className="height-px-200">
        <Base
          file={file}
          setFile={setFile}
          acceptableFileType={acceptableFileType}
          openFileBrowser={openFileBrowser}
          setOpenFileBrowser={setOpenFileBrowser}
          draggableElement={draggableElement}
          mainContainerClassName={cx(
            type === 1 && "width-per-100 height-px-100"
          )}
          whileDraggingElementClassName={cx(
            type === 1 &&
              "pos-abs pos-abs--lt width-per-100 br-all-solid-2 br-theme-two br-rad-px-10  height-px-200 "
          )}
          inputId={inputId}
          inputName={inputName}
        />
      </Div>
    </>
  );
};

export default DragDropFileUploader;
