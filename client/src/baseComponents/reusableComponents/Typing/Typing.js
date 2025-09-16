import { useState, useEffect } from "react";

import Div from "@/baseComponents/reusableComponents/Div";
import DivConvertTextToHtml from "@/baseComponents/reusableComponents/DivConvertTextToHtml";

const Typing = ({ htmlContent, speed = 20, callBackFunction = null }) => {
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    if (typeof htmlContent !== "string") {
      setDisplayed("");
      return;
    }
    let i = 0;
    const interval = setInterval(() => {
      setDisplayed(htmlContent.slice(0, i));
      if (callBackFunction) callBackFunction();
      i++;
      if (i > htmlContent.length) clearInterval(interval);
    }, speed);
    return () => clearInterval(interval);
  }, [htmlContent, speed]);

  return (
    <>
      <DivConvertTextToHtml text={displayed} />
    </>
  );
};

export default Typing;
