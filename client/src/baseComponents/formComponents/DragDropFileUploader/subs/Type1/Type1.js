import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";

import { COLORS } from "@/constants/vars";

const Type1 = ({
  file,
  iconType,
  setOpenFileBrowser,
  acceptableFileString,
  removeFileClickHandler,
}) => {
  return (
    <>
      <Div
        type="flex"
        hAlign="center"
        vAlign="center"
        className={cx(
          "width-per-100 bg-white br-all-dashed-2 br-gray-bright height-px-200 bg-red p-all-8 br-rad-px-10"
        )}
      >
        {!file?.length ? (
          <Div type="flex" direction="vertical" hAlign="center">
            <Icon
              type={iconType}
              scale={3}
              color={COLORS["theme-three"]}
              className="width-px-70 height-px-80 mouse-hand"
              onClick={() => setOpenFileBrowser(true)}
            />
            <Div className="f-s-px-16 text-center text-primary m-t-16">
              <Div>Upload File</Div>
              <Div className="">Supported Format : {acceptableFileString}</Div>
            </Div>
          </Div>
        ) : (
          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            direction="vertical"
            className="width-per-100 p-all-2"
          >
            <Icon
              type={"upload"}
              scale={3}
              color={COLORS["success-two"]}
              className="width-px-70 height-px-80 mouse-hand"
              onClick={() => setOpenFileBrowser(true)}
            />
            <Div className="text-primary m-t-32"> File Uploaded!</Div>
            <Div
              type="flex"
              hAlign="center"
              vAlign="center"
              className="pos-rel"
            >
              <Div
                type="flex"
                hAlign="center"
                vAlign="center"
                className="width-px-30 height-px-30 mouse-hand"
                onClick={removeFileClickHandler}
              >
                <Icon type="trash" color={COLORS["warning-two"]} />
              </Div>
              <Div className="one-line f-s-px-12 text-primary width-per-100">
                File Name: {file?.[0]?.name}
              </Div>
            </Div>
          </Div>
        )}
      </Div>
    </>
  );
};

export default Type1;
