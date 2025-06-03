import { message } from 'antd';

const API_BASE_URL = 'http://localhost:8000';  // 백엔드 서버 주소

/**
 * 코드를 실행하고 결과를 반환하는 함수
 * @param {string} code - 실행할 코드
 * @returns {Promise<{imageUrl: string, log: string[]}>} 실행 결과
 */
export const executeCode = async (code) => {
  try {
    
    const response = await fetch(`${API_BASE_URL}/api/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });

    const data = await response.json();
    console.log('API 응답 데이터:', data); // 디버깅용 로그

    if (!response.ok || !data.success) {
      const errorMsg = '코드 실행 중 알 수 없는 오류가 발생했습니다.';
      const error = new Error(errorMsg)

      if (data.log) {
        error.log = data.log; 
      } else if (data.logs) {
        error.log = data.logs; 
      }

      throw error;
    }

    return data;
  } catch (error) {
    console.error('API 오류:', error); // 디버깅용 로그
    message.error(error.message);
    throw error;
  }
};

/**
 * 그래프를 이미지로 내보내는 함수
 * @param {string} code - 그래프 생성 코드
 * @returns {Promise<string>} 이미지 URL
 */
export const exportGraph = async (code) => {
  try {
    console.log('내보내기 요청:', code); // 디버깅용 로그
    
    const response = await fetch(`${API_BASE_URL}/api/export`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || '그래프 내보내기 중 오류가 발생했습니다.');
    }

    if (!data.success) {
      throw new Error(data.errors || '그래프 내보내기 중 오류가 발생했습니다.');
    }

    return `${API_BASE_URL}${data.result.imageUrl}`;
  } catch (error) {
    console.error('내보내기 오류:', error); // 디버깅용 로그
    message.error(error.message);
    throw error;
  }
}; 