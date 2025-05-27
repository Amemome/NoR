import React from "react";
import { Card } from "antd";
import ResultView from "./ResultView";
import LogPanel from "./LogPanel";

function ResultPanel(props) {
  return (
    <div className="flex-panel" style={{ ...props.style }}>
      <Card
        title="실행 결과"
        style={{ flex: 2, marginBottom: 8 }}
        bodyStyle={{ height: "100%", overflow: "auto", padding: 0 }}
      >
        <ResultView />
      </Card>
      <Card
        title="로그 / 출력"
        style={{ flex: 1 }}
        bodyStyle={{ height: "100%", overflow: "auto", padding: 0 }}
      >
        <LogPanel />
      </Card>
    </div>
  );
}

export default ResultPanel;
