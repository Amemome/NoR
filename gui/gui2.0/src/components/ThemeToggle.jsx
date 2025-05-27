import React, { useState } from "react";
import { Tooltip, Switch } from "antd";
import { BulbOutlined } from "@ant-design/icons";

function ThemeToggle() {
  const [dark, setDark] = useState(false);

  React.useEffect(() => {
    document.body.setAttribute('data-theme', dark ? 'dark' : 'light');
  }, [dark]);

  return (
    <Tooltip title={dark ? "라이트 모드로 전환" : "다크 모드로 전환"} placement="left">
      <Switch
        checkedChildren={<BulbOutlined />}
        unCheckedChildren={<BulbOutlined />}
        checked={dark}
        onChange={setDark}
        style={{ marginLeft: 12 }}
      />
    </Tooltip>
  );
}

export default ThemeToggle; 