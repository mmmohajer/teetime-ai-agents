import { useState } from "react";

import Div from "@/baseComponents/reusableComponents/Div";
import MediaPicker from "@/baseComponents/formComponents/MediaPicker";
import DragDropFileUploader from "@/baseComponents/formComponents/DragDropFileUploader";
import DatePicker from "@/baseComponents/formComponents/DatePicker";

const DisplayForm = () => {
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [video, setVideo] = useState(null);
  const [file, setFile] = useState();
  const [birthDate, setBirthDate] = useState(new Date());

  return (
    <>
      <Div>
        <Div>
          <MediaPicker
            label="Profile Photo"
            isRequired
            file={profilePhoto}
            setFile={setProfilePhoto}
            id="profilePhotoFieldHomePage"
            hasCropper={true}
            hasResizer={true}
            maxWidth={400}
            cropInfo={{
              minWidth: 50,
              maxWidth: 400,
              minHeight: 50,
              maxHeight: 400,
              aspect: 1,
            }}
          />
        </Div>
        <Div>
          <MediaPicker
            label="Video"
            isRequired
            file={video}
            setFile={setVideo}
            fileType="video"
            id="video"
          />
        </Div>
        <Div className="width-px-350">
          <DragDropFileUploader
            file={file}
            setFile={setFile}
            acceptableFileType=".pdf"
            acceptableFileString=".pdf"
            inputId={"test-drag-uplod-id"}
            iconType={"upload"}
          />
        </Div>
        <Div>
          <DatePicker
            label="Birth Date"
            isRequired
            chosenDate={birthDate}
            setChosenDate={setBirthDate}
          />
        </Div>
      </Div>
    </>
  );
};

export default DisplayForm;
