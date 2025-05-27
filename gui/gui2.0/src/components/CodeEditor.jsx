import React from "react";

const defaultCode = `그래프생성 "2024년 월별 매출 분석"
제목은 "2024년 월별 매출 변화 추이"
x축은 "월"
y축은 "매출 (단위: 백만원)"
종류는 "막대"
색상은 "파랑"
글꼴은 "나눔고딕"
굵기는 3
크기는 800, 600
범례는 "오른쪽 위"
저장은 "매출분석.png"
그리기`;

const editorStyle = {
  background: "#181c24",
  color: "#e6e6e6",
  fontSize: "1.08rem",
  fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
  border: "1.5px solid #232733",
  borderRadius: "10px",
  padding: "1.1rem 1.2rem",
  outline: "none",
  width: "100%",
  minHeight: 180,
  boxShadow: "0 2px 8px #0002",
  transition: "all 0.18s cubic-bezier(.4,1.3,.6,1)",
  resize: "vertical",
  lineHeight: 1.6,
};

const lineNumberStyle = {
  color: "#888",
  padding: "1.1rem 8px 1.1rem 0",
  textAlign: "right",
  margin: 0,
  userSelect: "none",
  fontSize: "1.08rem",
  fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
  lineHeight: 1.6,
};

function CodeEditor({ value, onChange, placeholder }) {
  const lines = (value || defaultCode).split('\n');

  return (
    <div style={{ display: "flex", background: "#181c24", height: "100%" }}>
      <pre style={lineNumberStyle}>
        {lines.map((_, i) => (
          <div key={i} style={{ height: "1.6em" }}>{i + 1}</div>
        ))}
      </pre>
      <textarea
        style={editorStyle}
        value={value || defaultCode}
        onChange={e => onChange && onChange(e.target.value)}
        placeholder={placeholder}
        spellCheck={false}
        onFocus={e => {
          e.currentTarget.style.borderColor = "#38bdf8";
          e.currentTarget.style.boxShadow = "0 4px 16px #38bdf855";
        }}
        onBlur={e => {
          e.currentTarget.style.borderColor = "#232733";
          e.currentTarget.style.boxShadow = "0 2px 8px #0002";
        }}
        onMouseOver={e => {
          e.currentTarget.style.borderColor = "#60a5fa";
        }}
        onMouseOut={e => {
          if (document.activeElement !== e.currentTarget) {
            e.currentTarget.style.borderColor = "#232733";
          }
        }}
      />
    </div>
  );
}

export default CodeEditor;
