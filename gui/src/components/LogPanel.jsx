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

function LogPanel({ log }) {
  if (!log || log.length === 0) {
    return <div style={{ color: '#888', padding: '1rem', fontSize: '1.1rem' }}>아직 로그가 없습니다. 명령어를 실행해보세요!</div>;
  }
  return (
    <List
      size="large"
      dataSource={log}
      renderItem={item => (
        <List.Item style={{ padding: '0.8rem 1rem' }}>
          <Tag color={item.type === "error" ? "red" : item.type === "success" ? "green" : "blue"} style={{ fontSize: '1rem', padding: '0.2rem 0.6rem' }}>
            {item.source}
          </Tag>
          <Typography.Text 
            type={item.type === "error" ? "danger" : item.type === "success" ? "success" : undefined}
            style={{ 
              fontSize: '1.1rem',
              marginLeft: '0.8rem',
              fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif"
            }}
          >
            {item.message}
          </Typography.Text>
        </List.Item>
      )}
    />
  );
}

export default LogPanel; 