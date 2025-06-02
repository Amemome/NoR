import React, { useState, useContext } from "react";
import { Layout, ConfigProvider, theme, message } from "antd";
import MenuBar from "../components/MenuBar";
import EditorPanel from "../components/EditorPanel";
import ResultPanel from "../components/ResultPanel";
import ThemeToggle from "../components/ThemeToggle";
import NoRLogo from "../components/NoRLogo";
import "../App.css";
import { ThemeContext } from "../components/ThemeContext";
import { executeCode } from "../services/api";
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
      const response = await executeCode(code);
      if (response.success) {
        setResult(response.result);
        setLog([{ source: "parser", type: "success", message: "파싱 성공! 그래프를 그릴 준비가 완료되었습니다." }]);
        message.success("코드가 성공적으로 실행되었습니다.");
      } else {
        setError(Array.isArray(response.errors) ? response.errors.join('\n') : (response.errors || "알 수 없는 오류"));
        setResult(null);
        setLog([{ source: "compileNorEngine", type: "error", message: Array.isArray(response.errors) ? response.errors.join('\n') : (response.errors || "알 수 없는 오류") }]);
        message.error("코드 실행 중 오류가 발생했습니다.");
      }
    } catch (err) {
      setError(err.message);
      setResult(null);
      setLog([{ source: "network", type: "error", message: err.message }]);
      message.error("서버 연결 중 오류가 발생했습니다.");
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