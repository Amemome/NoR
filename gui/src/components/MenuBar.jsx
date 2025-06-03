import React, { useContext, useState } from "react";
import { Button, Tooltip, Space, Dropdown, Modal } from "antd";
import { PlusOutlined, FileSearchOutlined, QuestionCircleOutlined } from "@ant-design/icons";
import { ThemeContext } from "./ThemeContext";

const exampleCommands = {
  "막대 그래프": `// 그래프 식별을 위한 고유한 이름을 설정합니다. 분석 대상과 기간을 명시합니다.
그래프생성 "쇼핑몰 카테고리별 매출 현황 (2024년 1분기)"

// 그래프 종류를 "막대" (또는 "막대그래프")로 지정합니다. 범주형 데이터의 크기를 비교합니다.
종류는 막대

// X축 (상품 카테고리)과 Y축 (해당 카테고리 매출액) 데이터를 입력합니다.
// X축 데이터는 주로 문자열(범주)로 구성됩니다.
데이터는 [
  ["프리미엄 의류", "최신형 가전", "유기농 식품", "전문 개발 서적", "천연 화장품"], // X: 상품 카테고리 (구체적인 이름 사용)
  [120, 250, 180, 80, 150]                 // Y: 1분기 매출액 (단위: 억 원)
]

// 그래프 상단에 표시될 전체 제목을 설정합니다. 그래프의 주요 내용을 명확히 전달합니다.
제목은 "2024년 1분기 주요 카테고리별 매출 실적 분석"

// (선택) 범례에 표시될 이 데이터 시리즈의 이름을 지정합니다. (단일 시리즈에서는 생략 가능)
라벨은 "1분기 매출액 (억 원)"

// (선택) 범례의 위치를 설정합니다. 막대와 겹치지 않는 곳을 선택합니다.
범례는 우상단

// X축의 이름(레이블)을 설정합니다.
x축의 이름은 "상품 카테고리"

// Y축의 이름(레이블)을 설정합니다. 단위 정보를 명확히 표기합니다.
y축의 이름은 "매출액 (단위: 억 원)"
// (선택) Y축 눈금의 범위나 간격을 데이터에 맞게 조절하여 가독성을 높입니다.
y축의 눈금은 [0, 50, 100, 150, 200, 250, 300] // 최대 매출액보다 약간 높게 설정

// 그려질 막대의 스타일을 설정합니다.
막대의 색은 "steelblue" // 차분하면서도 전문적인 느낌의 파란색 계열

막대의 너비는 0.6 // 막대 사이의 간격을 확보하기 위해 기본값(0.8)보다 약간 좁게 설정
막대의 투명도는 0.85 // 약간의 투명도를 주어 부드러운 느낌을 더함

// (선택) 그래프의 전체 배경색, 내부 배경색, 크기, 해상도 등을 설정합니다.
배경색은 "whitesmoke" // 아주 연한 회색 배경
내부 배경색은 "white"  // 그림 영역은 흰색으로 하여 막대 색상 강조
그래프 크기는 [9, 6] // 가로 9인치, 세로 6인치
해상도는 150

// 설정된 내용으로 그래프를 화면에 표시합니다.
그리기`,
  "선 그래프": `// 그래프 식별을 위한 고유한 이름을 설정합니다. 분석 대상과 기간을 명시하면 좋습니다.
그래프생성 "알파베리 품종 일별 생장 길이 추적 (2024년 7월)"

// 그래프 종류를 "선그래프"로 지정합니다. (또는 "선")
종류는 선그래프

// X축 (측정 경과일)과 Y축 (해당 일의 평균 생장 길이) 데이터를 입력합니다.
데이터는 [
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], // X: 경과일 (0일차부터 시작)
  [2.5, 2.8, 3.2, 3.7, 4.1, 4.6, 5.0, 5.3, 5.7, 6.1, 6.4, 6.6, 6.9, 7.1, 7.3]  // Y: 평균 생장 길이 (cm)
]

// 그래프 상단에 표시될 전체 제목을 설정합니다. 그래프의 핵심 내용을 요약합니다.
제목은 "알파베리 품종의 시간 경과에 따른 생장 길이 변화"

// (선택) 범례에 표시될 이 데이터 선의 이름을 지정합니다. 여러 선을 그릴 때 유용합니다.
라벨은 "알파베리 생장선"

// (선택) 범례의 위치를 설정합니다. (예: "좌상단", "우하단", "최적", "상중앙" 등)
범례는 좌상단

// (선택) 범례의 글꼴 크기를 조절할 수 있습니다. (NoR 언어 지원 확인 필요)
// 예: 범례의 글꼴크기는 10

// X축의 이름(레이블)을 설정합니다. 단위 정보를 포함하면 이해하기 쉽습니다.
x축의 이름은 "측정 경과일 (Day)"

// (선택) X축 눈금의 간격이나 표시될 값들을 직접 지정할 수 있습니다.
x축의 눈금은 [0, 2, 4, 6, 8, 10, 12, 14]

// (선택) X축 선 및 레이블의 색상을 변경할 수 있습니다.
// 예: x축의 색은 "darkgray"

// (선택) X축 레이블의 글꼴 크기를 조절할 수 있습니다. (NoR 언어 지원 확인 필요)
// 예: x축의 글꼴크기는 9

// Y축의 이름(레이블)을 설정합니다. 단위 정보를 포함합니다.
y축의 이름은 "평균 생장 길이 (cm)"

// (선택) Y축 눈금의 범위나 간격을 직접 지정할 수 있습니다. 데이터 범위를 고려하여 설정합니다.
y축의 눈금은 [0, 1, 2, 3, 4, 5, 6, 7, 8]

// (선택) Y축 선 및 레이블의 색상을 변경할 수 있습니다.
// 예: y축의 색은 "#555555" // 진한 회색 HEX 코드

// (선택) Y축 레이블의 글꼴 스타일을 변경할 수 있습니다. (NoR 언어 지원 확인 필요)
// 예: y축의 글꼴은 "나눔고딕" (지원하는 폰트는 문서에서 확인)

// 그려질 선의 스타일을 지정합니다.
선의 종류는 파선 // "실선", "점선", "파선", "점선파선" 또는 "-", ":", "--", "-."
선의 색은 "green" // "red", "blue", "orange" 등 다양한 색상 또는 HEX 코드
선의 굵기는 3   // 선의 두께를 숫자로 지정 (클수록 두꺼워짐)

// (선택) 선의 투명도를 조절할 수 있습니다. (0.0 ~ 1.0)
// 예: 선의 투명도는 0.8

// (선택) 그래프의 전체 배경색(figure)을 설정합니다.
배경색은 "white" // 또는 "lightyellow", "#f0f8ff" (AliceBlue) 등

// (선택) 그래프 그림 영역(axes)의 배경색을 설정합니다.
내부 배경색은 "#f9f9f9" // 매우 연한 회색으로 데이터 가독성 향상

// (선택) 그래프 그림의 가로, 세로 크기를 인치 단위로 설정합니다. (예: [가로, 세로])
그래프 크기는 [10, 6]

// (선택) 파일 저장 시 해상도(DPI)를 설정하여 이미지 품질을 조절합니다.
해상도는 200
// (선택) 그래프에 격자선(그리드)을 추가하여 값 읽기를 용이하게 합니다. (NoR 언어 지원 확인 필요)
// 예: 그래프의 그리드는 수직 // "수평", "수직", "양방향"
// 예: 그래프의 그리드색은 "lightgray"
// 예: 그래프의 그리드스타일은 점선

// 설정된 내용으로 그래프를 화면에 표시합니다.
그리기

`,
  "산점도": `// 그래프 식별을 위한 고유한 이름을 설정합니다. 분석 목적과 기간을 명시합니다.
그래프생성 "광고비 대비 트래픽 효율 분석 (2024년 상반기)"

// 그래프 종류를 "산점도"로 지정합니다. 두 변수 간의 관계를 파악하는 데 사용됩니다.
종류는 산점도

// 데이터 포인트를 나타내는 마커의 스타일을 설정합니다.
마커의 종류는 원 // 가장 기본적인 마커 모양입니다. (다른 옵션: "별", "사각형", "엑스" 등)
마커의 색은 "blue" // 시각적으로 주목도를 높이는 색상을 선택합니다.
마커의 투명도는 0.9 // 데이터 포인트가 겹치는 부분을 확인하려면 투명도를 낮게 설정하는편이 좋습니다. (0.0 ~ 1.0)


// (선택) 범례에 표시될 이 데이터 시리즈의 이름을 지정합니다. (단일 시리즈에서는 생략 가능)
라벨은 "캠페인 데이터"

// (선택) 범례의 위치를 설정합니다. 데이터 분포를 고려하여 가리지 않는 위치를 선택합니다.
범례는 좌상단 // "우상단", "최적" 등 가능

// X축 (광고 비용)과 Y축 (트래픽 증가량) 데이터를 입력합니다.
// 각 리스트는 동일한 개수의 데이터 포인트를 가져야 합니다.
데이터는 [
  [50, 75, 120, 60, 150, 90, 110, 80, 130, 100], // X: 광고 비용 (단위: 만 원)
  [300, 400, 650, 350, 750, 500, 600, 450, 700, 550]  // Y: 트래픽 증가량 (단위: 명)
]

// 그래프 상단에 표시될 전체 제목을 설정합니다. 분석 내용을 명확히 전달합니다.
제목은 "광고 캠페인 비용과 웹사이트 트래픽 증가량 관계"

// X축의 이름(레이블)을 설정합니다. 변수의 의미와 단위를 명확히 표기합니다.
x축의 이름은 "광고 비용 (단위: 만 원)"
// (선택) X축 눈금의 범위, 간격, 표시 형식 등을 조절할 수 있습니다.
// 예: x축의 눈금은 [0, 50, 100, 150, 200]
// (선택) X축의 글꼴, 색상 등을 변경하여 가독성을 높일 수 있습니다.
// 예: x축의 글꼴크기는 11
// 예: x축의 색은 "#333333" // 어두운 회색

// Y축의 이름(레이블)을 설정합니다. 변수의 의미와 단위를 명확히 표기합니다.
y축의 이름은 "일일 평균 트래픽 증가량 (명)"
// (선택) Y축 눈금의 범위, 간격 등을 데이터 분포에 맞게 조절합니다.
// 예: y축의 눈금은 [0, 200, 400, 600, 800]
// (선택) Y축 관련 시각적 속성을 변경할 수 있습니다.
// 예: y축의 글꼴은 "Arial" (문서에 명시된 폰트만 사용가능)

// (선택) 그래프 그림 영역(axes)의 배경색을 설정합니다. 데이터 포인트와의 대비를 고려합니다.
내부 배경색은 "#f0f0f0" // 연한 회색으로 데이터 포인트 강조

// (선택) 그래프 전체 그림(figure)의 배경색을 설정합니다.
// 예: 배경색은 "ivory"

// (선택) 그래프의 가로, 세로 크기를 설정합니다. (단위: 인치)
그래프 크기는 [9, 5.5] // 약간 넓은 형태로 설정

// (선택) 이미지 저장 시 해상도(DPI)를 설정합니다.
해상도는 200

// 설정된 내용으로 그래프를 화면에 표시합니다.
그리기
`
};

function MenuBar() {
  const { dark } = useContext(ThemeContext);
  const [isHelpModalVisible, setIsHelpModalVisible] = useState(false);

  const buttonStyle = {
    fontSize: "1.08rem",
    fontWeight: 700,
    color: dark ? "#e6e6e6" : "#232733",
    fontFamily: "'Fira Mono', 'Consolas', 'Menlo', 'monospace', 'Noto Sans KR', sans-serif",
    transition: "all 0.18s cubic-bezier(.4,1.3,.6,1)",
    background: "none",
  };

  const showHelpModal = () => {
    setIsHelpModalVisible(true);
  };

  const handleHelpModalClose = () => {
    setIsHelpModalVisible(false);
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
      icon: <QuestionCircleOutlined />,
      label: "도움말",
      tooltip: "NoR 언어 사용법을 확인합니다",
      onClick: showHelpModal
    }
  ];

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
    <>
      <Space size="large">
        {menuItems.map(renderButton)}
      </Space>
      <Modal
        title="NoR 사용법"
        open={isHelpModalVisible}
        onOk={handleHelpModalClose}
        onCancel={handleHelpModalClose}
        width={800}
        okText="확인"
        style={{ top: 20 }}
      >
        <div style={{ fontSize: '1.1rem', lineHeight: 1.6 }}>
          <h2 style={{ fontSize: '1.4rem', marginBottom: '1rem', color: '#1677ff' }}>NoR이란?</h2>
          <div style={{ 
            padding: '1.5rem', 
            background: '#f0f6ff', 
            borderRadius: '8px', 
            marginBottom: '1.5rem',
            border: '1px solid #d9e6ff'
          }}>
            <p style={{ fontSize: '1.1rem', color: '#232733' }}>
              NoR은 그래프를 쉽게 그릴 수 있게 도와주는 한국어 기반 스크립트 언어입니다.<br/>
              자연어처럼 작성된 명령어로 데이터를 시각화할 수 있습니다.
            </p>
          </div>

          <h2 style={{ fontSize: '1.4rem', marginBottom: '1rem', color: '#1677ff' }}>기본 사용법</h2>
          <h3 style={{ fontSize: '1.2rem', marginBottom: '0.8rem', color: '#1677ff' }}>그래프 생성과 데이터 입력</h3>
          <div style={{ 
            padding: '1.5rem', 
            background: '#f0f6ff', 
            borderRadius: '8px', 
            marginBottom: '1.5rem',
            border: '1px solid #d9e6ff'
          }}>
            <table style={{ width: '100%', marginBottom: '1rem', borderCollapse: 'collapse' }}>
              <tbody>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', width: '30%', color: '#1677ff', fontWeight: 'bold' }}>그래프 생성</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>그래프생성 "매출 그래프"</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', color: '#1677ff', fontWeight: 'bold' }}>데이터 입력</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>데이터는 [[1,2,3], [3,2,1]]</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', color: '#1677ff', fontWeight: 'bold' }}>그래프 출력</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>그리기</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', color: '#1677ff', fontWeight: 'bold' }}>그래프 저장</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>저장하기 "결과.png"</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h2 style={{ fontSize: '1.4rem', marginBottom: '1rem', color: '#1677ff' }}>그래프 속성 설정</h2>
          
          <h3 style={{ fontSize: '1.2rem', marginBottom: '0.8rem', color: '#1677ff' }}>그래프 종류</h3>
          <div style={{ 
            padding: '1.5rem', 
            background: '#f0f6ff', 
            borderRadius: '8px', 
            marginBottom: '1.5rem',
            border: '1px solid #d9e6ff'
          }}>
            <p style={{ fontSize: '1.1rem', color: '#232733' }}>
              종류는 막대그래프<br/>
              따옴표 불필요 (막대그래프, 선그래프 등)
            </p>
          </div>

          <h3 style={{ fontSize: '1.2rem', marginBottom: '0.8rem', color: '#1677ff' }}>제목</h3>
          <div style={{ 
            padding: '1.5rem', 
            background: '#f0f6ff', 
            borderRadius: '8px', 
            marginBottom: '1.5rem',
            border: '1px solid #d9e6ff'
          }}>
            <p style={{ fontSize: '1.1rem', color: '#232733' }}>
              제목은 "2024년 매출"<br/>
              따옴표 필요
            </p>
          </div>

          <h3 style={{ fontSize: '1.2rem', marginBottom: '0.8rem', color: '#1677ff' }}>크기</h3>
          <div style={{ 
            padding: '1.5rem', 
            background: '#f0f6ff', 
            borderRadius: '8px', 
            marginBottom: '1.5rem',
            border: '1px solid #d9e6ff'
          }}>
            <p style={{ fontSize: '1.1rem', color: '#232733' }}>
              그래프 크기는 [800, 600]<br/>
              벡터 형식 → 따옴표 불필요
            </p>
          </div>

          <h2 style={{ fontSize: '1.4rem', marginBottom: '1rem', color: '#1677ff' }}>스타일 설정</h2>
          
          <h3 style={{ fontSize: '1.2rem', marginBottom: '0.8rem', color: '#1677ff' }}>마커</h3>
          <div style={{ 
            padding: '1.5rem', 
            background: '#f0f6ff', 
            borderRadius: '8px', 
            marginBottom: '1.5rem',
            border: '1px solid #d9e6ff'
          }}>
            <table style={{ width: '100%', marginBottom: '1rem', borderCollapse: 'collapse' }}>
              <tbody>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', width: '20%', color: '#1677ff', fontWeight: 'bold' }}>종류</td>
                  <td style={{ padding: '0.8rem', width: '60%', color: '#232733' }}>마커의 종류는 o</td>
                  <td style={{ padding: '0.8rem', width: '20%', color: '#232733' }}>따옴표 불필요</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', color: '#1677ff', fontWeight: 'bold' }}>색상</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>마커의 색은 "파랑"</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>따옴표 필요</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', color: '#1677ff', fontWeight: 'bold' }}>크기</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>마커의 크기는 10</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>따옴표 불필요</td>
                </tr>
              </tbody>
            </table>
            <p style={{ fontSize: '1.1rem', color: '#232733' }}>사용 가능한 마커 종류: o, s, x, ^, v, * 등</p>
          </div>

          <h3 style={{ fontSize: '1.2rem', marginBottom: '0.8rem', color: '#1677ff' }}>선</h3>
          <div style={{ 
            padding: '1.5rem', 
            background: '#f0f6ff', 
            borderRadius: '8px', 
            marginBottom: '1.5rem',
            border: '1px solid #d9e6ff'
          }}>
            <table style={{ width: '100%', marginBottom: '1rem', borderCollapse: 'collapse' }}>
              <tbody>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', width: '20%', color: '#1677ff', fontWeight: 'bold' }}>종류</td>
                  <td style={{ padding: '0.8rem', width: '60%', color: '#232733' }}>선의 종류는 --</td>
                  <td style={{ padding: '0.8rem', width: '20%', color: '#232733' }}>따옴표 불필요</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', color: '#1677ff', fontWeight: 'bold' }}>색상</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>선의 색은 "빨강"</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>따옴표 필요</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', color: '#1677ff', fontWeight: 'bold' }}>굵기</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>선의 굵기는 2</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>따옴표 불필요</td>
                </tr>
              </tbody>
            </table>
            <p style={{ fontSize: '1.1rem', color: '#232733' }}>선 종류: -(실선), --(파선), :(점선), -.(점선-파선)</p>
          </div>

          <h2 style={{ fontSize: '1.4rem', marginBottom: '1rem', color: '#1677ff' }}>축 설정</h2>
          <div style={{ 
            padding: '1.5rem', 
            background: '#f0f6ff', 
            borderRadius: '8px', 
            marginBottom: '1.5rem',
            border: '1px solid #d9e6ff'
          }}>
            <table style={{ width: '100%', marginBottom: '1rem', borderCollapse: 'collapse' }}>
              <tbody>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', width: '20%', color: '#1677ff', fontWeight: 'bold' }}>이름</td>
                  <td style={{ padding: '0.8rem', width: '60%', color: '#232733' }}>x축의 이름은 "시간"</td>
                  <td style={{ padding: '0.8rem', width: '20%', color: '#232733' }}>따옴표 필요</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', color: '#1677ff', fontWeight: 'bold' }}>라벨</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>y축의 라벨은 "점수"</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>따옴표 필요</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', color: '#1677ff', fontWeight: 'bold' }}>색상</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>x축의 색은 "회색"</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>따옴표 필요</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h2 style={{ fontSize: '1.4rem', marginBottom: '1rem', color: '#1677ff' }}>기타 속성</h2>
          <div style={{ 
            padding: '1.5rem', 
            background: '#f0f6ff', 
            borderRadius: '8px', 
            marginBottom: '1.5rem',
            border: '1px solid #d9e6ff'
          }}>
            <table style={{ width: '100%', marginBottom: '1rem', borderCollapse: 'collapse' }}>
              <tbody>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', width: '20%', color: '#1677ff', fontWeight: 'bold' }}>배경</td>
                  <td style={{ padding: '0.8rem', width: '60%', color: '#232733' }}>배경은 "흰색"</td>
                  <td style={{ padding: '0.8rem', width: '20%', color: '#232733' }}>따옴표 필요</td>
                </tr>
                <tr style={{ borderBottom: '1px solid #d9e6ff' }}>
                  <td style={{ padding: '0.8rem', color: '#1677ff', fontWeight: 'bold' }}>범례 위치</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>범례는 우상단</td>
                  <td style={{ padding: '0.8rem', color: '#232733' }}>따옴표 불필요</td>
                </tr>
              </tbody>
            </table>
            <p style={{ fontSize: '1.1rem', color: '#232733' }}>사용 가능한 범례 위치: 우상단, 좌상단, 중앙, best 등</p>
          </div>

          <h2 style={{ fontSize: '1.4rem', marginBottom: '1rem', color: '#1677ff' }}>전체 예시</h2>
          <pre style={{ 
            background: '#f0f6ff', 
            padding: '1.5rem', 
            borderRadius: '8px',
            fontSize: '1.1rem',
            lineHeight: 1.6,
            marginBottom: '1.5rem',
            color: '#232733',
            border: '1px solid #d9e6ff'
          }}>
{`그래프생성 "예제그래프"
종류는 산점도그래프
마커의 종류는 o
마커의 색은 "파랑"
데이터는 [[1,2,3,4],[4,3,2,1]]
제목은 "산점도 예제"
x축의 이름은 "시간"
y축의 이름은 "값"
범례는 우상단
그리기`}
          </pre>

          <h2 style={{ fontSize: '1.4rem', marginBottom: '1rem', color: '#1677ff' }}>자주 묻는 질문 (FAQ)</h2>
          <div style={{ marginBottom: '1.5rem', padding: '1rem', background: '#f0f6ff', borderRadius: '8px', border: '1px solid #d9e6ff' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '0.8rem', color: '#1677ff' }}>문자열은 언제 따옴표가 필요한가요?</h3>
            <p style={{ fontSize: '1.1rem', color: '#232733' }}>→ "빨강", "제목", "우상단"처럼 글자로 된 값은 반드시 "..." 또는 '...'로 감싸야 함</p>
          </div>
          <div style={{ marginBottom: '1.5rem', padding: '1rem', background: '#f0f6ff', borderRadius: '8px', border: '1px solid #d9e6ff' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '0.8rem', color: '#1677ff' }}>마커나 선 종류는 따옴표 없이 써야 하나요?</h3>
            <p style={{ fontSize: '1.1rem', color: '#232733' }}>→ 맞음. o, x, --, :처럼 정해진 기호는 따옴표 없이 써야 함</p>
          </div>
          <div style={{ marginBottom: '1.5rem', padding: '1rem', background: '#f0f6ff', borderRadius: '8px', border: '1px solid #d9e6ff' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '0.8rem', color: '#1677ff' }}>데이터는 어떤 형식으로 써야 하나요?</h3>
            <p style={{ fontSize: '1.1rem', color: '#232733' }}>→ 반드시 [x값 리스트], [y값 리스트] 형태로 벡터 2개 입력해야 함</p>
          </div>
        </div>
      </Modal>
    </>
  );
}

export default MenuBar; 