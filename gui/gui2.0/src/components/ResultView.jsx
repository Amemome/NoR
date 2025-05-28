import React from "react";
import DefaultGraphSVG from "./DefaultGraphSVG";

function ResultView() {
  return (
    <div style={styles.container}>
      <DefaultGraphSVG width={240} height={160} />
      <p style={styles.text}>아직 그래프가 없습니다. 명령어를 입력해 실행해보세요!</p>
    </div>
  );
}

const styles = {
  container: {
    height: "100%",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    opacity: 0.6,
  },
  text: {
    marginTop: "1rem",
    fontSize: "1rem",
    color: "#999",
  },
};

export default ResultView; 