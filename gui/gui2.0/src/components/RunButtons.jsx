import React from "react";
import { Button, Tooltip, Space } from "antd";
import { ReloadOutlined, PlayCircleOutlined } from "@ant-design/icons";

function RunButtons({ code }) {
  return (
    <Space style={{ marginBottom: 16 }}>
      <Tooltip title={"코드를 초기화합니다"} placement="bottom">
        <Button icon={<ReloadOutlined />} size="large" style={{ borderRadius: 4 }}>
          코드 초기화
        </Button>
      </Tooltip>
      <Tooltip title={"명령어를 실행합니다"} placement="bottom">
        <Button type="primary" icon={<PlayCircleOutlined />} size="large" style={{ borderRadius: 4 }}>
          명령어 실행
        </Button>
      </Tooltip>
    </Space>
  );
}

export default RunButtons; 