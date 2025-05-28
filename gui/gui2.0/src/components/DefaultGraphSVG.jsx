// src/components/DefaultGraphSVG.jsx
import React from "react";

function DefaultGraphSVG({ width = 120, height = 80 }) {
  return (
    <svg width={width} height={height} viewBox="0 0 120 60" style={{ display: "block", margin: "0 auto" }}>
      <rect x="10" y="40" width="16" height="30" rx="4" fill="#38bdf8" />
      <rect x="36" y="25" width="16" height="45" rx="4" fill="#f472b6" />
      <rect x="62" y="55" width="16" height="15" rx="4" fill="#facc15" />
      <rect x="88" y="10" width="16" height="60" rx="4" fill="#60a5fa" />
    </svg>
  );
}

export default DefaultGraphSVG;
