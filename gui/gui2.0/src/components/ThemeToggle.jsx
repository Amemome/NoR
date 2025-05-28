import React, { useContext } from "react";
import { Tooltip, Switch } from "antd";
import { BulbOutlined } from "@ant-design/icons";
import { ThemeContext } from "./ThemeContext";

const switchStyle = {
  background: "#232733",
  boxShadow: "0 2px 8px #0002",
  transition: "all 0.18s cubic-bezier(.4,1.3,.6,1)",
};

const iconStyle = {
  fontSize: "1.2rem",
  color: "#e6e6e6",
  transition: "all 0.18s cubic-bezier(.4,1.3,.6,1)",
};

function ThemeToggle(props) {
  // Context 우선, 없으면 props fallback
  const ctx = useContext(ThemeContext);
  const dark = ctx ? ctx.dark : props.dark;
  const setDark = ctx ? ctx.setDark : props.setDark;

  React.useEffect(() => {
    document.body.setAttribute('data-theme', dark ? 'dark' : 'light');
  }, [dark]);

  return (
    <Tooltip title={dark ? "라이트 모드로 전환" : "다크 모드로 전환"} placement="left">
      <Switch
        checkedChildren={<BulbOutlined style={iconStyle} />}
        unCheckedChildren={<BulbOutlined style={iconStyle} />}
        checked={dark}
        onChange={setDark}
        style={switchStyle}
        onMouseOver={e => {
          e.currentTarget.style.transform = "scale(1.1)";
          e.currentTarget.style.boxShadow = "0 4px 16px #0004";
        }}
        onMouseOut={e => {
          e.currentTarget.style.transform = "scale(1)";
          e.currentTarget.style.boxShadow = "0 2px 8px #0002";
        }}
        onMouseDown={e => {
          e.currentTarget.style.transform = "scale(0.95)";
        }}
        onMouseUp={e => {
          e.currentTarget.style.transform = "scale(1.1)";
        }}
      />
    </Tooltip>
  );
}

export default ThemeToggle; 