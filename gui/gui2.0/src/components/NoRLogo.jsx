import React from "react";

export default function NoRLogo({ size = 200 }) {
  return (
    <svg width={size * 2.2} height={size * 1.1} viewBox="0 0 180 90">
      <rect x="0" y="0" width="180" height="90" rx="18" fill="#181c24" />
      <g>
        <text
          x="48"
          y="65"
          fill="#38bdf8"
          fontWeight="900"
          fontSize="60"
          fontFamily="'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif"
          style={{
            textShadow: "0 2px 4px #38bdf822",
            letterSpacing: "-0.05em",
          }}
        >
          N
        </text>
        <text
          x="90"
          y="65"
          fill="#f472b6"
          fontWeight="900"
          fontSize="60"
          fontFamily="'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif"
          style={{
            textShadow: "0 2px 4px #f472b622",
            letterSpacing: "-0.05em",
          }}
        >
          o
        </text>
        <text
          x="132"
          y="65"
          fill="#facc15"
          fontWeight="900"
          fontSize="60"
          fontFamily="'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif"
          style={{
            textShadow: "0 2px 4px #facc1522",
            letterSpacing: "-0.05em",
          }}
        >
          R
        </text>
      </g>
    </svg>
  );
} 