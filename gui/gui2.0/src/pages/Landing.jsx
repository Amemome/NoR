import React from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

function Landing() {
  const navigate = useNavigate();

  // NoR 로고 bounce 애니메이션
  const logoVariants = {
    initial: { y: 0, scale: 1, rotate: 0 },
    bounce: {
      y: [0, -40, 0, -20, 0],
      scale: [1, 1.2, 1, 1.1, 1],
      rotate: [0, -10, 0, 8, 0],
      transition: { duration: 1.6, repeat: Infinity, repeatDelay: 1.2, ease: "easeInOut" }
    }
  };

  // 바 차트 데이터
  const bars = [
    { height: 60, delay: 0.2, color: "#38bdf8" },
    { height: 120, delay: 0.4, color: "#60a5fa" },
    { height: 90, delay: 0.6, color: "#818cf8" },
    { height: 180, delay: 0.8, color: "#f472b6" },
    { height: 140, delay: 1.0, color: "#facc15" },
  ];

  // 움직이는 배경 원
  const bgCircles = [
    { size: 120, x: -180, y: -100, color: "#38bdf822", delay: 0.2 },
    { size: 80, x: 200, y: 120, color: "#f472b622", delay: 0.5 },
    { size: 60, x: 0, y: 180, color: "#facc1522", delay: 0.8 },
  ];

  const team = [
    { name: "최현경", role: "프론트엔드 및 문서화", desc: "UI/UX, React 개발" },
    { name: "류지성", role: "Language 파트", desc: "렉서, 파서, 데이터 처리" },
    { name: "이운길", role: "graph 파트", desc: "matplotlib으로 그래프 처리" },
    // ...팀원 추가
  ];

  return (
    <div style={styles.outer}>
      {/* 그라데이션 배경 */}
      <div style={styles.gradientBg} />
      
      {/* 움직이는 배경 원 */}
      {bgCircles.map((c, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, scale: 0.7 }}
          animate={{ opacity: 1, scale: 1.1 }}
          transition={{ delay: c.delay, duration: 1.2, repeat: Infinity, repeatType: "reverse", repeatDelay: 2 }}
          style={{
            ...styles.bgCircle,
            width: c.size,
            height: c.size,
            left: `calc(50% + ${c.x}px)`,
            top: `calc(50% + ${c.y}px)`,
            background: c.color,
          }}
        />
      ))}

      <div style={styles.container}>
        {/* NoR 로고 픽사 bounce */}
        <motion.div
          variants={logoVariants}
          initial="initial"
          animate="bounce"
          style={styles.norLogo}
        >
          <span style={styles.norN}>N</span>
          <span style={styles.norO}>o</span>
          <span style={styles.norR}>R</span>
        </motion.div>

        {/* 그래프 애니메이션 */}
        <div style={styles.graphArea}>
          <div style={styles.barChart}>
            {bars.map((bar, i) => (
              <motion.div
                key={i}
                initial={{ height: 0 }}
                animate={{ height: bar.height }}
                transition={{ delay: bar.delay, duration: 0.7, type: "spring" }}
                style={{
                  ...styles.bar,
                  height: bar.height,
                  background: bar.color,
                }}
              />
            ))}
          </div>
          {/* 움직이는 선 */}
          <motion.svg
            width="220"
            height="60"
            style={{ position: "absolute", left: 0, top: 0 }}
          >
            <motion.polyline
              points="10,50 60,30 110,40 160,10 210,30"
              fill="none"
              stroke="#38bdf8"
              strokeWidth="4"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ delay: 1.2, duration: 1.2, ease: "easeInOut" }}
            />
            {/* 움직이는 점 */}
            <motion.circle
              r="7"
              fill="#f472b6"
              initial={{ cx: 10, cy: 50 }}
              animate={{ cx: 210, cy: 30 }}
              transition={{ delay: 2.2, duration: 1.2, ease: "easeInOut" }}
            />
          </motion.svg>
        </div>

        {/* 텍스트/버튼 애니메이션 */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.7, duration: 0.7 }}
          style={styles.title}
        >
          데이터, 한글로 그리다
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2.1, duration: 0.6 }}
          style={styles.subtitle}
        >
          쉽고 감성적인 한글 데이터 시각화 툴 <b>NoR</b>
        </motion.p>
        <motion.button
          onClick={() => navigate("/editor")}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 2.5, duration: 0.5 }}
          style={styles.button}
        >
          시작하기 →
        </motion.button>
        <motion.a
          href="/about"
          style={styles.aboutLink}
          whileHover={{ opacity: 1 }}
        >
          About NoR →
        </motion.a>
      </div>
    </div>
  );
}

const styles = {
  outer: {
    minHeight: "100vh",
    minWidth: "100vw",
    position: "relative",
    overflow: "hidden",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  gradientBg: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
    zIndex: 0,
  },
  container: {
    zIndex: 2,
    minHeight: "100vh",
    minWidth: "100vw",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "Pretendard, 'NanumGothic', sans-serif",
    textAlign: "center",
    padding: "2rem",
    position: "relative",
  },
  norLogo: {
    fontSize: "3.2rem",
    fontWeight: "900",
    letterSpacing: "0.1em",
    marginBottom: "1.2rem",
    color: "#38bdf8",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
    textShadow: "0 4px 16px #38bdf855",
    userSelect: "none",
  },
  norN: {
    color: "#38bdf8",
    fontWeight: "900",
    fontFamily: "Pretendard, 'NanumGothic', sans-serif",
    fontSize: "3.2rem",
    letterSpacing: "-0.05em",
  },
  norO: {
    color: "#f472b6",
    fontWeight: "900",
    fontFamily: "Pretendard, 'NanumGothic', sans-serif",
    fontSize: "3.2rem",
    margin: "0 0.1em",
    letterSpacing: "-0.05em",
  },
  norR: {
    color: "#facc15",
    fontWeight: "900",
    fontFamily: "Pretendard, 'NanumGothic', sans-serif",
    fontSize: "3.2rem",
    letterSpacing: "-0.05em",
  },
  bgCircle: {
    position: "absolute",
    borderRadius: "50%",
    filter: "blur(2px)",
    zIndex: 0,
  },
  graphArea: {
    position: "relative",
    width: 220,
    height: 200,
    margin: "0 auto 1.5rem auto",
    display: "flex",
    alignItems: "flex-end",
    justifyContent: "center",
  },
  barChart: {
    display: "flex",
    alignItems: "flex-end",
    gap: 12,
    height: 200,
    width: 220,
    zIndex: 1,
  },
  bar: {
    width: 28,
    borderRadius: "8px 8px 0 0",
    boxShadow: "0 2px 8px #0003",
    marginBottom: 0,
  },
  title: {
    fontSize: "2.2rem",
    fontWeight: "700",
    marginTop: "1.5rem",
    color: "#fff",
  },
  subtitle: {
    fontSize: "1.1rem",
    opacity: 0.85,
    marginTop: "0.5rem",
    color: "#fff",
  },
  button: {
    marginTop: "2rem",
    background: "#38bdf8",
    color: "#0f172a",
    border: "none",
    padding: "0.8rem 2rem",
    borderRadius: "10px",
    fontSize: "1rem",
    fontWeight: "bold",
    cursor: "pointer",
    transition: "all 0.3s ease",
    boxShadow: "0 2px 8px #0002",
  },
  aboutLink: {
    marginTop: "1rem",
    color: "#fff",
    opacity: 0.8,
    textDecoration: "none",
    fontSize: "0.9rem",
    transition: "opacity 0.2s",
  },
};

export default Landing;