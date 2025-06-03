import React, { useContext, useEffect } from "react";
import { ThemeContext } from "./ThemeContext";
import Editor from "@monaco-editor/react";

const defaultCode = `그래프생성 "내 첫 선 그래프"
종류는 선
데이터는 [[1, 2, 3, 4, 5], [2, 3, 5, 4, 6]]
제목은 "간단한 데이터 추이"
x축의 이름은 "X 값"
y축의 이름은 "Y 값"
선의 색은 "blue"
그리기`;

// NoR 언어 문법 정의
const norLanguageDefinition = {
  defaultToken: '',
  tokenPostfix: '.nor',
  
  keywords: [
    // 복합 키워드 (띄어쓰기 포함)
    'x축의 이름은', 'y축의 이름은', '그래프 크기는', '데이터는',
    // 단일 키워드
    '그래프생성', '제목은', 'x축은', 'y축은', '종류는', '색상은', '글꼴은', '굵기는', '크기는', '범례는', '저장은', '저장하기', '그리기',
    '막대그래프', '선그래프', '산점도그래프', '막대', '선', '산점도',
    '파랑', '빨강', '초록', '검정', '흰색', '노랑', '보라', '주황', '분홍', '갈색', '회색',
    '실선', '점선', '파선', '점선파선',
    '원', '사각형', '점', '엑스', '삼각형', '별',
    '우상단', '좌상단', '우하단', '좌하단', '중앙'
  ],

  operators: ['은', '는', '의', '='],

  symbols: /[=><!~?:&|+\-*\/\^]+/,

  tokenizer: {
    root: [
      // 주석 (다른 규칙보다 먼저 와야 함)
      [/\/\/.*/, 'comment'], // 한 줄 주석
      [/\/\*/, 'comment', '@comment'], // 블록 주석 시작
      // 복합 키워드 (띄어쓰기 포함)
      [/x축의 이름은|y축의 이름은|그래프 크기는|데이터는/, 'keyword'],
      // 문자열
      [/"[^"\\]*(\\.[^"\\]*)*"/, 'string'],
      [/'[^'\\]*(\\.[^'\\]*)*'/, 'string'],
      // 숫자
      [/\d+/, 'number'],
      // 키워드
      [/[가-힣a-zA-Z]+/, { 
        cases: {
          '@keywords': 'keyword',
          '@default': 'identifier'
        }
      }],
      // 연산자
      [/[은는의=]/, 'operator'],
      // 공백
      [/[ \t\r\n]+/, 'white'],
      // 기타
      [/./, 'text']
    ],
    comment: [
      [/[^\/*]+/, 'comment'], // 주석 내용
      [/\*\//, 'comment', '@pop'], // 블록 주석 끝
      [/[\/*]/, 'comment'] // 주석 내부에 있는 / 또는 *
    ]
  }
};

// 자동완성(인텔리센스)용 주요 명령어/속성/값 목록  
const norCompletions = [
  '그래프생성', '제목은', 'x축의 이름은', 'y축의 이름은', '종류는', '색상은', '글꼴은', '굵기는', '그래프 크기는', '범례는', '저장하기', '그리기', '데이터는',
  '막대그래프', '선그래프', '산점도그래프', '막대', '선', '산점도',
  '파랑', '빨강', '초록', '검정', '흰색', '노랑', '보라', '주황', '분홍', '갈색', '회색',
  '실선', '점선', '파선', '점선파선',
  '원', '사각형', '점', '엑스', '삼각형', '별',
  '우상단', '좌상단', '우하단', '좌하단', '중앙'
];

function CodeEditor({ value, onChange, placeholder, error }) {
  const { dark } = useContext(ThemeContext);

  useEffect(() => {
    window.onExampleSelect = (code) => {
      if (onChange) {
        onChange(code);
      }
    };

    window.onExport = async () => {
      try {
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

  const handleEditorDidMount = (editor, monaco) => {
    // NoR 언어 등록
    monaco.languages.register({ id: 'nor' });
    monaco.languages.setMonarchTokensProvider('nor', norLanguageDefinition);

    // 인텔리센스(자동완성) 등록
    monaco.languages.registerCompletionItemProvider('nor', {
      triggerCharacters: [' ', '\n', ...'abcdefghijklmnopqrstuvwxyz가나다라마바사아자차카타파하'],
      provideCompletionItems: (model, position) => {
        const suggestions = norCompletions.map(word => ({
          label: word,
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: word,
        }));
        return { suggestions };
      }
    });

    // 테마 설정
    monaco.editor.defineTheme('nor-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'keyword', foreground: '#38bdf8', fontStyle: 'bold' },
        { token: 'string', foreground: '#f472b6' },
        { token: 'number', foreground: '#facc15' },
        { token: 'operator', foreground: '#60a5fa' },
        { token: 'identifier', foreground: '#e6e6e6' },
        { token: 'text', foreground: '#e6e6e6' }
      ],
      colors: {
        'editor.background': '#181c24',
        'editor.foreground': '#e6e6e6',
        'editor.lineHighlightBackground': '#232733',
        'editorLineNumber.foreground': '#888',
        'editorCursor.foreground': '#38bdf8'
      }
    });

    monaco.editor.defineTheme('nor-light', {
      base: 'vs',
      inherit: true,
      rules: [
        { token: 'keyword', foreground: '#1677ff', fontStyle: 'bold' },
        { token: 'string', foreground: '#eb2f96' },
        { token: 'number', foreground: '#faad14' },
        { token: 'operator', foreground: '#1890ff' },
        { token: 'identifier', foreground: '#232733' },
        { token: 'text', foreground: '#232733' }
      ],
      colors: {
        'editor.background': '#ffffff',
        'editor.foreground': '#232733',
        'editor.lineHighlightBackground': '#f0f6ff',
        'editorLineNumber.foreground': '#999',
        'editorCursor.foreground': '#1677ff'
      }
    });
  };

  return (
    <div style={{ height: "100%", display: "flex", flexDirection: "column" }}>
      <Editor
        height="100%"
        language="nor"
        value={value || defaultCode}
        onChange={onChange}
        theme={dark ? "nor-dark" : "nor-light"}
        options={{
          fontSize: 16,
          fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          lineNumbers: "on",
          roundedSelection: false,
          scrollbar: {
            vertical: 'visible',
            horizontal: 'visible',
            useShadows: false,
            verticalScrollbarSize: 8,
            horizontalScrollbarSize: 8
          }
        }}
        onMount={(editor, monaco) => {
          handleEditorDidMount(editor, monaco);
          monaco.editor.setTheme(dark ? 'nor-dark' : 'nor-light');
        }}
      />
      {error && (
        <div style={{ 
          color: 'red', 
          minHeight: 24, 
          marginTop: 4,
          padding: '0.5rem 1rem',
          background: dark ? '#232733' : '#fff',
          borderTop: '1px solid #ff4d4f'
        }}>
          {Array.isArray(error) ? error.join('\n') : error}
        </div>
      )}
    </div>
  );
}

export default CodeEditor;
