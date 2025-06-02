import React from "react";
import { Card } from "antd";
import RunButtons from "./RunButtons";
import CodeEditor from "./CodeEditor";

const panelTitleStyle = {
  fontSize: "1.08rem",
  fontWeight: 700,
  color: "#38bdf8",
  fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
};

function EditorPanel({ code, setCode, onRun, onClear, isRunning, error, style }) {
  return (
    <div className="flex-panel" style={{ ...style }}>
      <Card
        title={
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%',
            borderBottom: '1.5px solid #232733', paddingBottom: 8, marginBottom: -8
          }}>
            <span style={panelTitleStyle}>명령어 입력</span>
            <div style={{ marginLeft: 'auto' }}>
              <RunButtons onRun={onRun} onClear={onClear} isRunning={isRunning} />
            </div>
          </div>
        }
        style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}
        bodyStyle={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", padding: 0 }}
      >
        <div style={{ flex: 1, overflow: "auto", paddingTop: 12 }}>
          <CodeEditor value={code} onChange={setCode} error={error} />
        </div>
      </Card>
    </div>
  );
}

export default EditorPanel;
