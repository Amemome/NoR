import React, { useContext } from "react";
import { Button, Tooltip, Space, Dropdown } from "antd";
import { PlusOutlined, FileSearchOutlined, ExportOutlined, AppstoreOutlined } from "@ant-design/icons";
import { ThemeContext } from "./ThemeContext";

const exampleCommands = {
  "막대 그래프": `그래프생성 "2024년 월별 매출 분석"
제목은 "2024년 월별 매출 변화 추이"
x축은 "월"
y축은 "매출 (단위: 백만원)"
종류는 "막대"
색상은 "파랑"
글꼴은 "나눔고딕"
굵기는 3
크기는 800, 600
범례는 "오른쪽 위"
저장은 "매출분석.png"
그리기`,
  "선 그래프": `그래프생성 "주간 온도 변화"
제목은 "일주일간 온도 변화 추이"
x축은 "요일"
y축은 "온도 (°C)"
종류는 "선"
색상은 "빨강"
글꼴은 "나눔고딕"
굵기는 2
크기는 800, 600
범례는 "오른쪽 위"
저장은 "온도분석.png"
그리기`,
  "산점도": `그래프생성 "키와 몸무게 상관관계"
제목은 "키와 몸무게의 상관관계 분석"
x축은 "키 (cm)"
y축은 "몸무게 (kg)"
종류는 "산점도"
색상은 "초록"
글꼴은 "나눔고딕"
굵기는 2
크기는 800, 600
범례는 "오른쪽 위"
저장은 "상관관계분석.png"
그리기`
};

const templateCommands = {
  "학생 성적 분석": {
    "막대 그래프": `그래프생성 "학생별 성적 분석"
제목은 "학생별 과목 성적 비교"
x축은 "학생"
y축은 "점수"
종류는 "막대"
색상은 "파랑"
글꼴은 "나눔고딕"
굵기는 2
크기는 800, 600
범례는 "오른쪽 위"
저장은 "학생성적분석.png"
그리기`,
    "선 그래프": `그래프생성 "학생별 성적 추이"
제목은 "학생별 성적 변화 추이"
x축은 "시험"
y축은 "점수"
종류는 "선"
색상은 "빨강"
글꼴은 "나눔고딕"
굵기는 2
크기는 800, 600
범례는 "오른쪽 위"
저장은 "성적추이분석.png"
그리기`
  },
  "매출 분석": {
    "월별 매출": `그래프생성 "월별 매출 분석"
제목은 "2024년 월별 매출 현황"
x축은 "월"
y축은 "매출 (단위: 백만원)"
종류는 "막대"
색상은 "파랑"
글꼴은 "나눔고딕"
굵기는 2
크기는 800, 600
범례는 "오른쪽 위"
저장은 "월별매출분석.png"
그리기`,
    "제품별 매출": `그래프생성 "제품별 매출 분석"
제목은 "제품별 매출 비중"
x축은 "제품"
y축은 "매출 (단위: 백만원)"
종류는 "막대"
색상은 "초록"
글꼴은 "나눔고딕"
굵기는 2
크기는 800, 600
범례는 "오른쪽 위"
저장은 "제품별매출분석.png"
그리기`
  },
  "실험 데이터": {
    "산점도": `그래프생성 "실험 데이터 분석"
제목은 "실험 데이터 상관관계"
x축은 "변수 A"
y축은 "변수 B"
종류는 "산점도"
색상은 "보라"
글꼴은 "나눔고딕"
굵기는 2
크기는 800, 600
범례는 "오른쪽 위"
저장은 "실험데이터분석.png"
그리기`,
    "선 그래프": `그래프생성 "실험 결과 추이"
제목은 "실험 결과 변화 추이"
x축은 "시간"
y축은 "측정값"
종류는 "선"
색상은 "주황"
글꼴은 "나눔고딕"
굵기는 2
크기는 800, 600
범례는 "오른쪽 위"
저장은 "실험결과분석.png"
그리기`
  }
};

const menuItems = [
  {
    icon: <PlusOutlined />,
    label: "새 창",
    tooltip: "새 실행기를 엽니다",
  },
  {
    icon: <FileSearchOutlined />,
    label: "예시",
    tooltip: "예시 명령어를 불러옵니다",
    isDropdown: true,
    items: Object.keys(exampleCommands).map(key => ({
      key,
      label: key,
      onClick: () => {
        if (window.onExampleSelect) {
          window.onExampleSelect(exampleCommands[key]);
        }
      }
    }))
  },
  {
    icon: <ExportOutlined />,
    label: "내보내기",
    tooltip: "결과를 이미지로 저장합니다",
    onClick: () => {
      if (window.onExport) {
        window.onExport();
      }
    }
  },
  {
    icon: <AppstoreOutlined />,
    label: "템플릿",
    tooltip: "자주 사용하는 명령 템플릿 보기",
    isDropdown: true,
    items: Object.entries(templateCommands).map(([category, templates]) => ({
      key: category,
      label: category,
      children: Object.entries(templates).map(([name, code]) => ({
        key: `${category}-${name}`,
        label: name,
        onClick: () => {
          if (window.onExampleSelect) {
            window.onExampleSelect(code);
          }
        }
      }))
    }))
  },
];

function MenuBar() {
  const { dark } = useContext(ThemeContext);
  const buttonStyle = {
    fontSize: "1.08rem",
    fontWeight: 700,
    color: dark ? "#e6e6e6" : "#232733",
    fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
    transition: "all 0.18s cubic-bezier(.4,1.3,.6,1)",
    background: "none",
  };

  const renderButton = (item) => {
    const handleClick = item.label === "새 창"
      ? () => window.open(window.location.origin + "/editor", "_blank", "noopener,noreferrer")
      : item.onClick;

    const button = (
      <Button
        type="text"
        icon={item.icon}
        size="large"
        style={buttonStyle}
        onClick={handleClick}
        onMouseOver={e => {
          e.currentTarget.style.color = dark ? "#38bdf8" : "#1677ff";
          e.currentTarget.style.transform = "scale(1.1)";
          e.currentTarget.style.background = dark ? "#232733" : "#f0f6ff";
        }}
        onMouseOut={e => {
          e.currentTarget.style.color = dark ? "#e6e6e6" : "#232733";
          e.currentTarget.style.transform = "scale(1)";
          e.currentTarget.style.background = "none";
        }}
        onMouseDown={e => {
          e.currentTarget.style.transform = "scale(0.95)";
        }}
        onMouseUp={e => {
          e.currentTarget.style.transform = "scale(1.1)";
        }}
      >
        {item.label}
      </Button>
    );

    if (item.isDropdown) {
      return (
        <Dropdown
          menu={{ items: item.items }}
          placement="bottom"
          key={item.label}
        >
          {button}
        </Dropdown>
      );
    }

    return (
      <Tooltip title={item.tooltip} key={item.label} placement="bottom">
        {button}
      </Tooltip>
    );
  };

  return (
    <Space size="large">
      {menuItems.map(renderButton)}
    </Space>
  );
}

export default MenuBar; 