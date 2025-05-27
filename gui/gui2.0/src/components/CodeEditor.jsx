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

function CodeEditor({ value, onChange }) {
  return (
    <textarea
      style={{ width: "100%", height: 300, fontFamily: "monospace", fontSize: 16, borderRadius: 8, padding: 12, resize: "vertical" }}
      value={value || defaultCode}
      onChange={e => onChange && onChange(e.target.value)}
      spellCheck={false}
    />
  );
}

export default CodeEditor; 