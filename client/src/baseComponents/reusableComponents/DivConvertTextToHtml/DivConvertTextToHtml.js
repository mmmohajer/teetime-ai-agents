import { useEffect, useState } from "react";
import DOMPurify from "dompurify";

import Div from "@/baseComponents/reusableComponents/Div";

const DivConvertTextToHtml = ({ text, ...props }) => {
  const [sanitizedHtml, setSanitizedHtml] = useState("");
  useEffect(() => {
    if (text) {
      setSanitizedHtml(DOMPurify.sanitize(text));
    }
  }, [text]);

  return (
    <>
      <Div dangerouslySetInnerHTML={{ __html: sanitizedHtml }} {...props} />
    </>
  );
};

export default DivConvertTextToHtml;
