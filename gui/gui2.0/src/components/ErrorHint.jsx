import React from "react";
import { Alert, Tooltip } from "antd";
import { ExclamationCircleOutlined, CheckCircleOutlined } from "@ant-design/icons";

function ErrorHint({ code }) {
  // 실제 파싱 연동 전까지는 예시로 에러 메시지/없음 랜덤 표시
  // 예시: 3번째 줄에서 세미콜론 누락 에러
  const hasError = code && code.includes(";"); // 예시: 세미콜론이 있으면 에러 없음
  return hasError ? (
    <Alert
      type="success"
      message={
        <span>
          <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
          에러 없음
        </span>
      }
      showIcon
      style={{ marginTop: 12 }}
    />
  ) : (
    <Tooltip title="라인 3에서 ; 누락됨" placement="right">
      <Alert
        type="error"
        message={
          <span>
            <ExclamationCircleOutlined style={{ color: '#ff4d4f', marginRight: 8 }} />
            라인 3에서 ; 누락됨
          </span>
        }
        showIcon
        style={{ marginTop: 12 }}
      />
    </Tooltip>
  );
}

export default ErrorHint; 