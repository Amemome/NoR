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

function ResultPanel({ result, error, loading, style }) {
  return (
    <div className="flex-panel" style={{ ...style }}>
      <Card
        title={<span style={panelTitleStyle}>실행 결과</span>}
        style={{ flex: 2, marginBottom: 8 }}
        bodyStyle={{ height: "100%", overflow: "auto", padding: 0 }}
      >
        {loading ? (
          <div>로딩중...</div>
        ) : error ? (
          <div style={{ color: "red" }}>{Array.isArray(error) ? error.join('\n') : error}</div>
        ) : (
          <ResultView result={result} />
        )}
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
