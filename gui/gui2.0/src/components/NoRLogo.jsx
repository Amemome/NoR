import React from "react";
export default function NoRLogo({ size = 32 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 40 40">
      <rect x="0" y="0" width="40" height="40" rx="6" fill="#1677ff"/>
      <text x="50%" y="60%" textAnchor="middle" fill="#fff" fontWeight="bold" fontSize="18" fontFamily="sans-serif">NoR</text>
    </svg>
  );
} 