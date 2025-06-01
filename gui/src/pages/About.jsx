import React from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

function About() {
  const navigate = useNavigate();
  const team = [
    { name: "이운길", role: "Graph 파트", desc: "matplotlib으로 그래프 처리" },
    { name: "최현경", role: "GUI 파트", desc: "UI/UX, React 개발" },
    { name: "류지성", role: "Language 파트", desc: "렉서, 파서, 데이터 처리" },
  ];

  // NoR 로고 bounce 애니메이션
  const logoVariants = {
    initial: { y: 0, scale: 1, rotate: 0 },
    bounce: {
      y: [0, -20, 0, -10, 0],
      scale: [1, 1.1, 1, 1.05, 1],
      rotate: [0, -6, 0, 4, 0],
      transition: { duration: 1.6, repeat: Infinity, repeatDelay: 1.2, ease: "easeInOut" }
    }
  };

  // 반짝임 위치 랜덤 생성
  const sparkles = Array.from({ length: 18 }).map((_, i) => ({
    left: `${Math.random() * 100}%`,
    top: `${Math.random() * 100}%`,
    size: 6 + Math.random() * 8,
    delay: Math.random() * 2,
    duration: 1.5 + Math.random() * 1.5,
    key: i,
  }));

  return (
    <div style={styles.outer}>
      {/* 그라데이션 배경 */}
      <div style={styles.gradientBg} />
      {/* 전체 반짝임 */}
      {sparkles.map((s) => (
        <motion.div
          key={s.key}
          style={{
            ...styles.sparkle,
            left: s.left,
            top: s.top,
            width: s.size,
            height: s.size,
          }}
          animate={{ opacity: [0.2, 1, 0.2], scale: [0.7, 1.2, 0.7] }}
          transition={{
            duration: s.duration,
            repeat: Infinity,
            repeatType: "reverse",
            delay: s.delay,
          }}
        />
      ))}
      {/* 움직이는 배경 원 */}
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, scale: 0.7 }}
          animate={{ opacity: 1, scale: 1.1 }}
          transition={{ delay: i * 0.2, duration: 1.2, repeat: Infinity, repeatType: "reverse", repeatDelay: 2 }}
          style={{
            ...styles.bgCircle,
            width: [120, 80, 60][i],
            height: [120, 80, 60][i],
            left: `calc(50% + ${[-180, 200, 0][i]}px)`,
            top: `calc(50% + ${[-100, 120, 180][i]}px)`,
            background: ["#38bdf822", "#f472b622", "#facc1522"][i],
          }}
        />
      ))}

      <div style={styles.container}>
        {/* HERO: NoR 로고 + 그래프 */}
        <div style={styles.heroArea}>
          {/* NoR 로고 제거, 그래프만 남김 */}
          {/* 그래프 애니메이션 */}
          <div style={styles.heroGraphArea}>
            <div style={styles.barChart}>
              {[60, 120, 90, 180, 140].map((h, i) => (
                <motion.div
                  key={i}
                  initial={{ height: 0 }}
                  animate={{ height: h }}
                  transition={{ delay: 0.2 + i * 0.2, duration: 0.7, type: "spring" }}
                  style={{
                    ...styles.bar,
                    height: h,
                    background: ["#38bdf8", "#60a5fa", "#818cf8", "#f472b6", "#facc15"][i],
                  }}
                />
              ))}
            </div>
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
              <motion.circle
                r="7"
                fill="#f472b6"
                initial={{ cx: 10, cy: 50 }}
                animate={{ cx: 210, cy: 30 }}
                transition={{ delay: 2.2, duration: 1.2, ease: "easeInOut" }}
              />
            </motion.svg>
          </div>
        </div>
        <motion.h1
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          style={styles.title}
        >
          About NoR
        </motion.h1>
        <motion.button
          style={styles.backButton}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.97 }}
          onClick={() => navigate("/editor")}
        >
          NoR 실행기로 돌아가기
        </motion.button>

        {/* NoR의 철학 */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          style={styles.card}
        >
          <h2 style={styles.cardTitle}>NoR의 철학</h2>
          <p style={styles.cardText}>
            NoR은 논문용 그래프를 쉽고 빠르게 작성할 수 있도록 설계된 Python 기반 미니 스크립트 언어입니다.
            NoSQL이 복잡한 데이터베이스를 단순하게 만든 것처럼, 저희는 복잡한 그래프 코드를 단순하게 만들고 싶었습니다.
            그래서 누구나 쉽게 쓸 수 있는 미니 스크립트 언어, NoR을 만들어보려고 합니다.
          </p>
        </motion.div>

        {/* 프로젝트 기간 */}
        <motion.div
          initial={{ opacity: 0, x: -100 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          style={styles.card}
        >
          <h2 style={styles.cardTitle}>프로젝트 기간</h2>
          <p style={styles.cardText}>
            2025.04 ~ 2025.06
          </p>
        </motion.div>

        {/* 기술 스택 */}
        <motion.div
          initial={{ opacity: 0, x: -100 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          style={styles.card}
        >
          <h2 style={styles.cardTitle}>기술 스택</h2>
          <div style={styles.techStack}>
            {[
              "Python", 
              "PySimpleGUI", 
              "Matplotlib", 
              "Seaborn", 
              "Lark-parser"
            ].map((tech, i) => (
              <motion.div
                key={tech}
                whileHover={{ scale: 1.1, rotate: 5 }}
                whileTap={{ scale: 0.95 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8 + i * 0.1 }}
                style={styles.techItem}
              >
                {tech}
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* 오픈소스 */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          style={styles.card}
        >
          <h2 style={styles.cardTitle}>오픈소스 프로젝트</h2>
          <p style={styles.cardText}>
            NoR은 matplotlib, seaborn, Lark 등 자유로운 라이선스를 가진 오픈소스 라이브러리를 기반으로 개발되었으며,
            PySimpleGUI는 LGPL 3.0을 따르므로 수정 시 해당 부분만 공개하면 전체 오픈소스 공개에 제약은 없습니다.
          </p>
          <motion.a
            href="https://github.com/your-repo"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            style={styles.githubButton}
          >
            GitHub에서 보기
          </motion.a>
        </motion.div>

        {/* 팀 소개 */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0 }}
          style={styles.card}
        >
          <h2 style={styles.cardTitle}>팀 소개</h2>
          <div style={styles.teamGrid}>
            {team.map((member, i) => (
              <motion.div
                key={member.name}
                whileHover={{ scale: 1.05, rotate: 1 }}
                whileTap={{ scale: 0.95 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.2 + i * 0.1 }}
                style={styles.teamCard}
              >
                <div style={styles.teamName}>{member.name}</div>
                <div style={styles.teamRole}>{member.role}</div>
                <div style={styles.teamDesc}>{member.desc}</div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

const styles = {
  outer: {
    minHeight: "100vh",
    width: "100%",
    position: "relative",
    overflow: "auto",
    display: "flex",
    alignItems: "flex-start",
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
    width: "100%",
    maxWidth: 2000,
    padding: "2rem",
    display: "flex",
    flexDirection: "column",
    gap: "2rem",
    marginTop: "2rem",
    marginBottom: "4rem",
  },
  title: {
    fontSize: "3rem",
    fontWeight: "900",
    color: "#fff",
    textAlign: "center",
    marginBottom: "2rem",
    textShadow: "0 4px 16px #38bdf855",
  },
  card: {
    background: "rgba(30, 41, 59, 0.8)",
    borderRadius: "20px",
    padding: "2rem",
    boxShadow: "0 4px 24px #0003",
    backdropFilter: "blur(10px)",
  },
  cardTitle: {
    fontSize: "1.8rem",
    fontWeight: "700",
    color: "#38bdf8",
    marginBottom: "1rem",
  },
  cardText: {
    fontSize: "1.1rem",
    color: "#fff",
    lineHeight: 1.6,
    opacity: 0.9,
  },
  techStack: {
    display: "flex",
    flexWrap: "wrap",
    gap: "1rem",
    marginTop: "1rem",
  },
  techItem: {
    background: "#38bdf8",
    color: "#0f172a",
    padding: "0.8rem 1.5rem",
    borderRadius: "10px",
    fontWeight: "600",
    fontSize: "1rem",
    boxShadow: "0 2px 8px #0002",
  },
  githubButton: {
    display: "inline-block",
    background: "#222",
    color: "#fff",
    padding: "0.8rem 1.5rem",
    borderRadius: "10px",
    fontWeight: "600",
    textDecoration: "none",
    marginTop: "1rem",
    boxShadow: "0 2px 8px #0002",
  },
  teamGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
    gap: "1.5rem",
    marginTop: "1rem",
  },
  teamCard: {
    background: "rgba(40, 40, 60, 0.8)",
    borderRadius: "16px",
    padding: "1.5rem",
    textAlign: "center",
    boxShadow: "0 2px 12px #0002",
  },
  teamName: {
    fontSize: "1.4rem",
    fontWeight: "700",
    color: "#fff",
    marginBottom: "0.5rem",
  },
  teamRole: {
    fontSize: "1.1rem",
    color: "#38bdf8",
    marginBottom: "0.5rem",
  },
  teamDesc: {
    fontSize: "0.9rem",
    color: "#fff",
    opacity: 0.8,
  },
  bgCircle: {
    position: "absolute",
    borderRadius: "50%",
    filter: "blur(2px)",
    zIndex: 0,
  },
  backButton: {
    margin: "0 auto 1.5rem auto",
    background: "#38bdf8",
    color: "#0f172a",
    border: "none",
    padding: "0.7rem 2rem",
    borderRadius: "10px",
    fontSize: "1rem",
    fontWeight: "bold",
    cursor: "pointer",
    transition: "all 0.3s ease",
    boxShadow: "0 2px 8px #0002",
    display: "block",
  },
  heroArea: {
    width: "100%",
    maxWidth: 700,
    margin: "0 auto 1rem auto",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: "1.2rem",
    position: "relative",
    zIndex: 3,
  },
  heroGraphArea: {
    position: "relative",
    width: 220,
    height: 200,
    margin: "0 auto",
    display: "flex",
    alignItems: "flex-end",
    justifyContent: "center",
  },
  sparkle: {
    position: "fixed",
    zIndex: 2,
    borderRadius: "50%",
    background: "#fff",
    opacity: 0.7,
    filter: "blur(1.5px)",
    pointerEvents: "none",
  },
  barChart: {
    // Add appropriate styles for the bar chart
  },
  bar: {
    // Add appropriate styles for the bar
  },
};

export default About; 