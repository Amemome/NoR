import React, { useContext } from "react";
import { Layout, ConfigProvider, theme } from "antd";
import MenuBar from "../components/MenuBar";
import EditorPanel from "../components/EditorPanel";
import ResultPanel from "../components/ResultPanel";
import ThemeToggle from "../components/ThemeToggle";
import NoRLogo from "../components/NoRLogo";
import "../App.css";
import { ThemeContext } from "../components/ThemeContext";

const { Header, Content } = Layout;

function Editor() {
  const { dark } = useContext(ThemeContext);
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
            <NoRLogo size={48} />
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
            <EditorPanel style={{ flex: 1, height: "100%", overflow: "hidden" }} />
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
            <ResultPanel style={{ flex: 1, height: "100%", overflow: "hidden" }} />
          </div>
        </Content>
      </Layout>
    </ConfigProvider>
  );
}

export default Editor; 