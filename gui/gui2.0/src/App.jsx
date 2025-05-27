import React from "react";
import { Layout, ConfigProvider, theme } from "antd";
import MenuBar from "./components/MenuBar";
import EditorPanel from "./components/EditorPanel";
import ResultPanel from "./components/ResultPanel";
import ThemeToggle from "./components/ThemeToggle";
import NoRLogo from "./components/NoRLogo";
import "./App.css";

const { Header, Content } = Layout;

function App() {
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          colorBgBase: "#181c24",
          colorBgContainer: "#232733",
          colorText: "#e6e6e6",
          colorPrimary: "#1677ff",
          colorPrimaryHover: "#4096ff",
          colorPrimaryActive: "#0958d9",
          borderRadius: 14,
        },
      }}
    >
      <Layout style={{ minHeight: "100vh", background: "#181c24" }}>
        <Header
          style={{
            background: "#232733",
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
            <NoRLogo size={32} />
            <MenuBar />
          </div>
          <ThemeToggle />
        </Header>

        <Content className="main-content">
          <EditorPanel style={{ flex: 1 }} />
          <ResultPanel style={{ flex: 1 }} />
        </Content>
      </Layout>
    </ConfigProvider>
  );
}

export default App;
