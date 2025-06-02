import React from "react";
import DefaultGraphSVG from "./DefaultGraphSVG";

function ResultView({ result }) {
  if (!result || !result.imageUrl) {
    return (
      <div style={styles.container}>
        <DefaultGraphSVG width={240} height={160} />
        <p style={styles.text}>아직 그래프가 없습니다. 명령어를 입력해 실행해보세요!</p>
      </div>
    );
  }

  return (
    <div style={styles.resultContainer}>
      <div style={styles.graphContainer}>
        <img 
          src={result.imageUrl}
          alt={result.title || "그래프"}
          style={styles.graph}
        />
      </div>
      <div style={styles.infoContainer}>
        <h3 style={styles.title}>{result.title || "그래프"}</h3>
        <div style={styles.details}>
          {result.xlabel && <p><strong>X축:</strong> {result.xlabel}</p>}
          {result.ylabel && <p><strong>Y축:</strong> {result.ylabel}</p>}
          {result.data && (
            <>
              <p><strong>데이터:</strong></p>
              <pre style={styles.data}>
                {JSON.stringify(result.data, null, 2)}
              </pre>
            </>
          )}
        </div>
      </div>
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
  resultContainer: {
    height: "100%",
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
    padding: "1rem",
  },
  graphContainer: {
    flex: 1,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#232733",
    borderRadius: "8px",
    padding: "1rem",
  },
  graph: {
    maxWidth: "100%",
    maxHeight: "100%",
    objectFit: "contain",
  },
  infoContainer: {
    background: "#232733",
    borderRadius: "8px",
    padding: "1rem",
  },
  title: {
    margin: 0,
    color: "#38bdf8",
    fontSize: "1.2rem",
  },
  details: {
    marginTop: "1rem",
    color: "#e6e6e6",
  },
  data: {
    background: "#181c24",
    padding: "0.5rem",
    borderRadius: "4px",
    overflow: "auto",
    maxHeight: "200px",
  },
};

export default ResultView; 