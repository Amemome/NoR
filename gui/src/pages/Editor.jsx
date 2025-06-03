import React, { useState, useContext } from "react";
import { Layout, ConfigProvider, theme, message } from "antd";
import MenuBar from "../components/MenuBar";
import EditorPanel from "../components/EditorPanel";
import ResultPanel from "../components/ResultPanel";
import ThemeToggle from "../components/ThemeToggle";
import NoRLogo from "../components/NoRLogo";
import "../App.css";
import { ThemeContext } from "../components/ThemeContext";
import { executeCode, exportGraph } from "../services/api";
import { useNavigate } from "react-router-dom";

const { Header, Content } = Layout;

function Editor() {
  const navigate = useNavigate();
  const { dark } = useContext(ThemeContext);
  const [code, setCode] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [log, setLog] = useState([]);

  // 실행 함수
  const handleExecute = async () => {
    setLoading(true);
    setError(null);
    setLog([]);

    try {
      const result = await executeCode(code);
      console.log('API 응답:', result); // 디버깅용 로그
      
      setResult(result.result);
      setLog(result.log);
      
    } catch (error) {
      console.error('실행 오류:', error); // 디버깅용 로그
      setError(error.message || '코드 실행 중 오류가 발생했습니다.');
      setLog(error.log)
    } finally {
      setLoading(false);
    }
  };

  // 코드 초기화 함수
  const handleClear = () => {
    setCode("");
    setResult(null);
    setError(null);
    setLog([]);
  };

  // 내보내기 함수
  const handleExport = async () => {
    if (!code.trim()) {
      message.warning("내보낼 코드를 입력해주세요.");
      return;
    }

    try {
      const imageUrl = await exportGraph(code);
      const link = document.createElement('a');
      link.href = imageUrl;
      link.download = 'graph.png';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      message.success("그래프가 성공적으로 저장되었습니다.");
    } catch (error) {
      message.error("그래프 저장 중 오류가 발생했습니다.");
    }
  };

  // window.onExport 함수 설정
  React.useEffect(() => {
    window.onExport = handleExport;
    return () => {
      window.onExport = null;
    };
  }, [code]);

  return (
    <ConfigProvider
      theme={{
        algorithm: dark ? theme.darkAlgorithm : theme.defaultAlgorithm,
        token: dark
          ? {
              colorBgBase: "#181c24",
              colorBgContainer: "#232733",
              colorText: "#e6e6e6",
              colorPrimary: "#1677ff",
              colorPrimaryHover: "#4096ff",
              colorPrimaryActive: "#0958d9",
              borderRadius: 14,
            }
          : {
              colorBgBase: "#f8fafc",
              colorBgContainer: "#fff",
              colorText: "#22223b",
              colorPrimary: "#1677ff",
              colorPrimaryHover: "#60a5fa",
              colorPrimaryActive: "#2563eb",
              borderRadius: 14,
            },
      }}
    >
      <Layout style={{ minHeight: "100vh", background: dark ? "#181c24" : "#f8fafc" }}>
        <Header
          style={{
            background: dark ? "#232733" : "#fff",
            padding: "0 40px",
            boxShadow: "0 2px 8px #0008",
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            zIndex: 100,
            height: 64,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 32 }}>
            <div onClick={() => navigate("/")} style={{ cursor: "pointer" }}>
              <NoRLogo size={48} />
            </div>
            <MenuBar />
          </div>
          <ThemeToggle />
        </Header>
        <Content
          style={{
            display: "flex",
            flexDirection: "row",
            height: `calc(100vh - 64px)`,
            gap: 8,
            padding: 0,
            boxSizing: "border-box",
            minWidth: 0,
            width: "100vw",
            marginTop: 64,
            paddingTop: 64,
            overflow: "hidden",
          }}
        >
          <div style={{
            flex: 1,
            minWidth: 0,
            height: "100%",
            display: "flex",
            flexDirection: "column",
            minHeight: 0,
            overflow: "hidden"
          }}>
            <EditorPanel
              code={code}
              setCode={setCode}
              onRun={handleExecute}
              onClear={handleClear}
              isRunning={loading}
              style={{ flex: 1, height: "100%", overflow: "hidden" }}
            />
          </div>
          <div style={{
            flex: 1,
            minWidth: 0,
            height: "100%",
            display: "flex",
            flexDirection: "column",
            minHeight: 0,
            overflow: "hidden"
          }}>
            <ResultPanel
              result={result}
              error={error}
              loading={loading}
              log={log}
              style={{ flex: 1, height: "100%", overflow: "hidden" }}
            />
          </div>
        </Content>
      </Layout>
    </ConfigProvider>
  );
}

export default Editor; 