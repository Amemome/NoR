import React, { useContext, useEffect } from "react";
import { ThemeContext } from "./ThemeContext"; 

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

function CodeEditor({ value, onChange, placeholder, error }) {
  const { dark } = useContext(ThemeContext);
  const lines = (value || defaultCode).split('\n');

  useEffect(() => {
    window.onExampleSelect = (code) => {
      if (onChange) {
        onChange(code);
      }
    };

    window.onExport = async () => {
      try {
        // 현재 코드를 실행하여 그래프 생성
        const response = await fetch('/api/execute', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ code: value || defaultCode }),
        });

        if (!response.ok) {
          throw new Error('그래프 생성에 실패했습니다.');
        }

        const result = await response.json();
        
        // 생성된 이미지 URL을 다운로드
        const link = document.createElement('a');
        link.href = result.imageUrl;
        link.download = 'graph.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error('내보내기 실패:', error);
        alert('그래프 내보내기에 실패했습니다.');
      }
    };

    return () => {
      window.onExampleSelect = null;
      window.onExport = null;
    };
  }, [onChange, value]);

  const backgroundColor = dark ? "#181c24" : "#ffffff";
  const textColor = dark ? "#e6e6e6" : "#1e1e1e";
  const borderColor = dark ? "#232733" : "#ccc";
  const shadowColor = dark ? "#0002" : "#ddd";

  const editorStyle = {
    background: backgroundColor,
    color: textColor,
    fontSize: "1.08rem",
    fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
    border: `1.5px solid ${borderColor}`,
    borderRadius: "10px",
    padding: "1.1rem 1.2rem",
    outline: "none",
    width: "100%",
    minHeight: 180,
    boxShadow: `0 2px 8px ${shadowColor}`,
    transition: "all 0.18s ease-in-out",
    resize: "vertical",
    lineHeight: 1.6,
  };

  const lineNumberStyle = {
    background: backgroundColor,
    color: dark ? "#888" : "#999",
    padding: "1.1rem 8px 1.1rem 0",
    textAlign: "right",
    margin: 0,
    userSelect: "none",
    fontSize: "1.08rem",
    fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
    lineHeight: 1.6,
  };

  return (
    <div style={{ display: "flex", background: backgroundColor, height: "100%" }}>
      <pre style={lineNumberStyle}>
        {lines.map((_, i) => (
          <div key={i} style={{ height: "1.6em" }}>{i + 1}</div>
        ))}
      </pre>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <textarea
          style={{ ...editorStyle, flex: 1, minHeight: 0 }}
          value={value || defaultCode}
          onChange={e => onChange && onChange(e.target.value)}
          placeholder={placeholder}
          spellCheck={false}
          onFocus={e => {
            e.currentTarget.style.borderColor = "#38bdf8";
            e.currentTarget.style.boxShadow = "0 4px 16px #38bdf855";
          }}
          onBlur={e => {
            e.currentTarget.style.borderColor = borderColor;
            e.currentTarget.style.boxShadow = `0 2px 8px ${shadowColor}`;
          }}
          onMouseOver={e => {
            e.currentTarget.style.borderColor = "#60a5fa";
          }}
          onMouseOut={e => {
            if (document.activeElement !== e.currentTarget) {
              e.currentTarget.style.borderColor = borderColor;
            }
          }}
        />
        {error && (
          <div style={{ color: 'red', minHeight: 24, marginTop: 4 }}>
            {Array.isArray(error) ? error.join('\n') : error}
          </div>
        )}
      </div>
    </div>
  );
}

export default CodeEditor;
