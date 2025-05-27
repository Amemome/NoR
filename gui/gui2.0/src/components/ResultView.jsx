import React from "react";
import { Tooltip } from "antd";

function ResultView() {
  return (
    <div style={{ width: "100%", height: 280, display: "flex", alignItems: "center", justifyContent: "center", position: "relative" }}>
      <Tooltip title={"그래프에서 우클릭하면 저장 메뉴가 나옵니다"} placement="top">
        <img
          src="https://static.thenounproject.com/png/17673-200.png"
          alt="그래프 예시"
          style={{ maxHeight: 240, maxWidth: "90%", borderRadius: 12, boxShadow: "0 2px 12px #0001", cursor: "pointer" }}
          onContextMenu={e => {
            // 브라우저 기본 우클릭 메뉴 허용 (툴팁만 안내)
          }}
        />
      </Tooltip>
    </div>
  );
}

export default ResultView; 