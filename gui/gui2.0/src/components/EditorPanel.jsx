import React, { useState } from "react";
import { Card } from "antd";
import RunButtons from "./RunButtons";
import CodeEditor from "./CodeEditor";
import ErrorHint from "./ErrorHint";

function EditorPanel() {
  const [code, setCode] = useState("");
  return (
    <Card
      title="명령어 입력"
      style={{ width: "40%", minWidth: 400, maxWidth: 600, margin: 24, height: "calc(100% - 48px)", display: "flex", flexDirection: "column" }}
      bodyStyle={{ flex: 1, display: "flex", flexDirection: "column" }}
    >
      <RunButtons code={code} />
      <CodeEditor value={code} onChange={setCode} />
      <ErrorHint code={code} />
    </Card>
  );
}

export default EditorPanel; 