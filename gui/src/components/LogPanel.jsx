import React from "react";
import { List, Typography, Tag } from "antd";

const logs = [
  {
    source: "compileNorEngine",
    type: "error",
    message: "명령어 '그려줘 온도 변화'에 오류가 있습니다.",
  },
  {
    source: "compileNorEngine",
    type: "info",
    message: "draw() 함수는 한 개의 문자열 인자를 필요로 합니다.",
  },
  {
    source: "parser",
    type: "success",
    message: "파싱 성공! 그래프를 그릴 준비가 완료되었습니다.",
  },
];

function LogPanel() {
  return (
    <List
      size="small"
      dataSource={logs}
      renderItem={item => (
        <List.Item>
          <Tag color={item.type === "error" ? "red" : item.type === "success" ? "green" : "blue"}>
            {item.source}
          </Tag>
          <Typography.Text type={item.type === "error" ? "danger" : item.type === "success" ? "success" : undefined}>
            {item.message}
          </Typography.Text>
        </List.Item>
      )}
    />
  );
}

export default LogPanel; 