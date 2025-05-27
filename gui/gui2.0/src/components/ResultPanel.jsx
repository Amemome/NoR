import React from "react";
import { Card } from "antd";
import ResultView from "./ResultView";
import LogPanel from "./LogPanel";

const panelTitleStyle = {
  fontSize: "1.08rem",
  fontWeight: 700,
  color: "#38bdf8",
  fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
};

function ResultPanel(props) {
  return (
    <div className="flex-panel" style={{ ...props.style }}>
      <Card
        title={<span style={panelTitleStyle}>실행 결과</span>}
        style={{ flex: 2, marginBottom: 8 }}
        bodyStyle={{ height: "100%", overflow: "auto", padding: 0 }}
      >
        <ResultView />
      </Card>
      <Card
        title={<span style={panelTitleStyle}>로그 / 출력</span>}
        style={{ flex: 1 }}
        bodyStyle={{ height: "100%", overflow: "auto", padding: 0 }}
      >
        <LogPanel />
      </Card>
    </div>
  );
}

export default ResultPanel;
