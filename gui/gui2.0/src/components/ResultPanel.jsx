import React from "react";
import { Card } from "antd";
import ResultView from "./ResultView";
import LogPanel from "./LogPanel";

function ResultPanel() {
  return (
    <div style={{ flex: 1, display: "flex", flexDirection: "column", margin: 24, marginLeft: 0 }}>
      <Card title="실행 결과" style={{ flex: 2, marginBottom: 16, minHeight: 320 }}>
        <ResultView />
      </Card>
      <Card title="로그/출력" style={{ flex: 1, minHeight: 120 }}>
        <LogPanel />
      </Card>
    </div>
  );
}

export default ResultPanel; 