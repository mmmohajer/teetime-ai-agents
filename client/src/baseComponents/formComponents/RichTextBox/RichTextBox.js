import { useRef } from "react";
import cx from "classnames";
import { Editor } from "@tinymce/tinymce-react";

import Div from "@/baseComponents/reusableComponents/Div";

import { TINY_CME_API_KEY } from "config";

const RichTextBox = ({ id, setText }) => {
  const editorRef = useRef();

  return (
    <>
      <Div className={cx("pos-rel")}>
        <Div className={cx("")}>
          <Editor
            id={id}
            onInit={(evt, editor) => (editorRef.current = editor)}
            initialValue={""}
            apiKey={TINY_CME_API_KEY}
            init={{
              placeholder: "",
              height: 500,
              menubar: false,
              // Commented plugins are usable in a premium plan
              plugins: [
                // 'a11ychecker',
                "advlist",
                // 'advcode',
                // 'advtable',
                "autolink",
                // 'checklist',
                "code",
                "codesample",
                // 'export',
                "lists",
                "link",
                "image",
                "charmap",
                "preview",
                "anchor",
                "searchreplace",
                "visualblocks",
                // 'powerpaste',
                "fullscreen",
                // 'formatpainter',
                "insertdatetime",
                "media",
                "table",
                "help",
                "wordcount",
              ],
              toolbar:
                "undo redo | styleselect | fontsizeselect insertdatetime | image media | link | casechange blocks | bold italic forecolor backcolor | " +
                "alignleft aligncenter alignright alignjustify | " +
                "bullist numlist checklist outdent indent | removeformat | a11ycheck code table help | codesample",
              fontsize_formats:
                "8pt 9pt 10pt 11pt 12pt 14pt 18pt 24pt 30pt 36pt 48pt 60pt 72pt 96pt",
              selector: "#tinymce",
              branding: false,
              height: 350,
              // codesample_languages: [
              //   { text: 'HTML/XML', value: 'markup' },
              //   { text: 'JavaScript', value: 'javascript' },
              //   { text: 'CSS', value: 'css' },
              //   { text: 'Java', value: 'java' },
              //   { text: 'Python', value: 'python' }
              // ],
              // invalid_elements: '',
              // extended_valid_elements: 'pre[*],code[*]'
              // content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
            }}
            onEditorChange={() => {
              if (setText) {
                setText(editorRef?.current?.getContent() || "");
              }
            }}
          />
        </Div>
      </Div>
    </>
  );
};

export default RichTextBox;
