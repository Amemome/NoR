import React from "react";
import { Button, Tooltip, Space } from "antd";
import { PlusOutlined, FileSearchOutlined, ExportOutlined, AppstoreOutlined } from "@ant-design/icons";

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
  return (
    <Space size="large">
      {menuItems.map((item) => (
        <Tooltip title={item.tooltip} key={item.label} placement="bottom">
          <Button type="text" icon={item.icon} size="large">
            {item.label}
          </Button>
        </Tooltip>
      ))}
    </Space>
  );
}

export default MenuBar; 