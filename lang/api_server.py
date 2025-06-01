from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from lark import Lark
from semantic_analyzer import SemanticAnalyzer
import sys
import os
import uuid
from datetime import datetime
import matplotlib.pyplot as plt

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graph.graph import graph

app = FastAPI()

# 정적 파일 서빙을 위한 디렉토리 생성
os.makedirs("static", exist_ok=True)

# CORS 설정 수정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
    expose_headers=["*"]
)

# 정적 파일 서빙 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# Lark 파서 초기화
with open("nor.lark", "r", encoding="utf-8") as f:
    grammar = f.read()
parser = Lark(grammar, start="start")

# 요청 모델 정의
class CodeRequest(BaseModel):
    code: str
    filename: str = None
    format: str = "png"

@app.post("/api/execute")
async def execute_code(request: CodeRequest):
    try:
        # 코드 파싱
        tree = parser.parse(request.code)
        
        # 의미 분석
        analyzer = SemanticAnalyzer()
        result = analyzer.visit(tree)
        
        if analyzer.errors:
            return {
                "success": False,
                "errors": [str(error) for error in analyzer.errors]
            }

        # 그래프 생성 로직
        g = graph()
        graph_data = {
            '종류': '선그래프',  # 기본값
            'x': [1, 2, 3, 4, 5],  # 기본 데이터
            'y': [1, 2, 3, 4, 5],
            '옵션': {
                '제목': '테스트 그래프',
                'x축': {
                    '이름': 'X축',
                    '색': 'black'
                },
                'y축': {
                    '이름': 'Y축',
                    '색': 'black'
                },
                '출력': {
                    '파일로 저장': 'static/test.png',
                    '그래프 크기': [8, 6],
                    '해상도': 100
                }
            }
        }
        
        # 그래프 생성
        g.draw(graph_data)
        
        # 파일명 생성
        if not request.filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"graph_{timestamp}.{request.format}"
        else:
            filename = f"{request.filename}.{request.format}"
        
        # 파일 저장 경로
        filepath = os.path.join("static", filename)
        
        # 그래프 저장
        plt.savefig(filepath, format=request.format, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "success": True,
            "result": {
                "title": graph_data['옵션']['제목'],
                "xlabel": graph_data['옵션']['x축']['이름'],
                "ylabel": graph_data['옵션']['y축']['이름'],
                "data": graph_data['y'],
                "imageUrl": f"/static/{filename}",
                "filename": filename
            }
        }
    except Exception as e:
        return {
            "success": False,
            "errors": str(e)
        }

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("static", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)