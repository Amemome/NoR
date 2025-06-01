import React from "react";
import { Button, Tooltip, Space } from "antd";
import { ReloadOutlined, PlayCircleOutlined } from "@ant-design/icons";

const runBtnStyle = {
  background: "#38bdf8",
  color: "#0f172a",
  border: "none",
  borderRadius: 10,
  fontSize: "1.08rem",
  fontWeight: 700,
  padding: "0.7rem 2rem",
  minWidth: 120,
  boxShadow: "0 2px 8px #0002",
  transition: "all 0.18s cubic-bezier(.4,1.3,.6,1)",
};
const clearBtnStyle = {
  background: "#232733",
  color: "#fff",
  border: "none",
  borderRadius: 10,
  fontSize: "1.08rem",
  fontWeight: 700,
  padding: "0.7rem 2rem",
  minWidth: 120,
  boxShadow: "0 2px 8px #0002",
  transition: "all 0.18s cubic-bezier(.4,1.3,.6,1)",
};

function RunButtons({ onRun, onClear, isRunning }) {
  return (
    <Space style={{ marginBottom: 16 }}>
      <Tooltip title={"코드를 초기화합니다"} placement="bottom">
        <Button
          icon={<ReloadOutlined />}
          size="large"
          style={clearBtnStyle}
          onClick={onClear}
          disabled={isRunning}
          onMouseOver={e => {
            e.currentTarget.style.background = "#f472b6";
            e.currentTarget.style.color = "#181c24";
            e.currentTarget.style.transform = "scale(1.06)";
            e.currentTarget.style.boxShadow = "0 4px 16px #f472b655";
          }}
          onMouseOut={e => {
            e.currentTarget.style.background = "#232733";
            e.currentTarget.style.color = "#fff";
            e.currentTarget.style.transform = "scale(1)";
            e.currentTarget.style.boxShadow = "0 2px 8px #0002";
          }}
          onMouseDown={e => {
            e.currentTarget.style.transform = "scale(0.97)";
          }}
          onMouseUp={e => {
            e.currentTarget.style.transform = "scale(1.06)";
          }}
        >
          코드 초기화
        </Button>
      </Tooltip>
      <Tooltip title={"명령어를 실행합니다"} placement="bottom">
        <Button
          type="primary"
          icon={<PlayCircleOutlined />}
          size="large"
          style={runBtnStyle}
          onClick={onRun}
          disabled={isRunning}
          onMouseOver={e => {
            e.currentTarget.style.background = "#60a5fa";
            e.currentTarget.style.color = "#0f172a";
            e.currentTarget.style.transform = "scale(1.06)";
            e.currentTarget.style.boxShadow = "0 4px 16px #38bdf855";
          }}
          onMouseOut={e => {
            e.currentTarget.style.background = "#38bdf8";
            e.currentTarget.style.color = "#0f172a";
            e.currentTarget.style.transform = "scale(1)";
            e.currentTarget.style.boxShadow = "0 2px 8px #0002";
          }}
          onMouseDown={e => {
            e.currentTarget.style.transform = "scale(0.97)";
          }}
          onMouseUp={e => {
            e.currentTarget.style.transform = "scale(1.06)";
          }}
        >
          명령어 실행
        </Button>
      </Tooltip>
    </Space>
  );
}

export default RunButtons; 