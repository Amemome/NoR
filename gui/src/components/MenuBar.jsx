import React, { useContext, useState } from "react";
import { Button, Tooltip, Space, Dropdown, Modal } from "antd";
import { PlusOutlined, FileSearchOutlined, QuestionCircleOutlined } from "@ant-design/icons";
import { ThemeContext } from "./ThemeContext";

const exampleCommands = {
  "막대 그래프": `그래프생성 "2024년 월별 매출 분석"
종류는 막대그래프
제목은 "2024년 월별 매출 변화 추이"
x축의 이름은 "월"
y축의 이름은 "매출 (단위: 백만원)"
색상은 파랑
글꼴은 "나눔고딕"
굵기는 3
그래프 크기는 [800, 600]
범례는 우상단

데이터는 [[1,2,3,4,5,6,7,8,9,10,11,12], [100,120,150,130,160,180,200,190,170,160,140,130]]

저장하기 "매출분석.png"
그리기`,
  "선 그래프": `그래프생성 "주간 온도 변화"
종류는 선그래프
제목은 "일주일간 온도 변화 추이"
x축의 이름은 "요일"
y축의 이름은 "온도 (°C)"
색상은 빨강
글꼴은 "나눔고딕"
굵기는 2
그래프 크기는 [800, 600]
범례는 우상단

데이터는 [[1,2,3,4,5,6,7], [20,22,21,23,25,24,22]]

저장하기 "온도분석.png"
그리기`,
  "산점도": `그래프생성 "키와 몸무게 상관관계"
종류는 산점도그래프
제목은 "키와 몸무게의 상관관계 분석"
x축의 이름은 "키 (cm)"
y축의 이름은 "몸무게 (kg)"
색상은 초록
글꼴은 "나눔고딕"
굵기는 2
그래프 크기는 [800, 600]
범례는 우상단
마커의 종류는 o
마커의 색은 파랑

데이터는 [[160,165,170,175,180,185,190], [55,60,65,70,75,80,85]]

저장하기 "상관관계분석.png"
그리기`
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