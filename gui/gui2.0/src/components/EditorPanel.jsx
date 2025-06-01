import React from "react";
import { Card } from "antd";
import RunButtons from "./RunButtons";
import CodeEditor from "./CodeEditor";
import ErrorHint from "./ErrorHint";

const panelTitleStyle = {
  fontSize: "1.08rem",
  fontWeight: 700,
  color: "#38bdf8",
  fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
};

function EditorPanel({ code, setCode, onRun, onClear, isRunning, style }) {
  return (
    <div className="flex-panel" style={{ ...style }}>
      <Card
        title={<span style={panelTitleStyle}>명령어 입력</span>}
        style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}
        bodyStyle={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", padding: 0 }}
      >
        <RunButtons onRun={onRun} onClear={onClear} isRunning={isRunning} />
        <div style={{ flex: 1, overflow: "auto" }}>
          <CodeEditor value={code} onChange={setCode} />
        </div>
        <ErrorHint code={code} />
      </Card>
    </div>
  );
}

export default EditorPanel;
