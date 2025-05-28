import React, { useContext } from "react";
import { Button, Tooltip, Space } from "antd";
import { PlusOutlined, FileSearchOutlined, ExportOutlined, AppstoreOutlined } from "@ant-design/icons";
import { ThemeContext } from "./ThemeContext";

const menuItems = [
  {
    icon: <PlusOutlined />,
    label: "새 창",
    tooltip: "새 실행기를 엽니다",
  },
  {
    icon: <FileSearchOutlined />,
    label: "예시",
    tooltip: "예시 명령어를 불러옵니다",
  },
  {
    icon: <ExportOutlined />,
    label: "내보내기",
    tooltip: "결과를 이미지로 저장합니다",
  },
  {
    icon: <AppstoreOutlined />,
    label: "템플릿",
    tooltip: "자주 사용하는 명령 템플릿 보기",
  },
];

function MenuBar() {
  const { dark } = useContext(ThemeContext);
  const buttonStyle = {
    fontSize: "1.08rem",
    fontWeight: 700,
    color: dark ? "#e6e6e6" : "#232733",
    fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
    transition: "all 0.18s cubic-bezier(.4,1.3,.6,1)",
    background: "none",
  };
  return (
    <Space size="large">
      {menuItems.map((item) => (
        <Tooltip title={item.tooltip} key={item.label} placement="bottom">
          <Button
            type="text"
            icon={item.icon}
            size="large"
            style={buttonStyle}
            onMouseOver={e => {
              e.currentTarget.style.color = dark ? "#38bdf8" : "#1677ff";
              e.currentTarget.style.transform = "scale(1.1)";
              e.currentTarget.style.background = dark ? "#232733" : "#f0f6ff";
            }}
            onMouseOut={e => {
              e.currentTarget.style.color = dark ? "#e6e6e6" : "#232733";
              e.currentTarget.style.transform = "scale(1)";
              e.currentTarget.style.background = "none";
            }}
            onMouseDown={e => {
              e.currentTarget.style.transform = "scale(0.95)";
            }}
            onMouseUp={e => {
              e.currentTarget.style.transform = "scale(1.1)";
            }}
          >
            {item.label}
          </Button>
        </Tooltip>
      ))}
    </Space>
  );
}

export default MenuBar; 