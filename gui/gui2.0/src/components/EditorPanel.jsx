import React, { useState } from "react";
import { Card } from "antd";
import RunButtons from "./RunButtons";
import CodeEditor from "./CodeEditor";
import ErrorHint from "./ErrorHint";

function EditorPanel(props) {
  const [code, setCode] = useState("");

  return (
    <div className="flex-panel" style={{ ...props.style }}>
      <Card
        title="명령어 입력"
        style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}
        bodyStyle={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", padding: 0 }}
      >
        <RunButtons code={code} />
        <div style={{ flex: 1, overflow: "auto" }}>
          <CodeEditor value={code} onChange={setCode} />
        </div>
        <ErrorHint code={code} />
      </Card>
    </div>
  );
}

export default EditorPanel;
