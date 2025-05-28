from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from semantic_analyzer import SemanticAnalyzer
from lark import Lark
import os

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 기본 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 문법 파일 로드
with open('nor.lark', 'r', encoding='utf-8') as f:
    grammar = f.read()
parser = Lark(grammar)

class CodeRequest(BaseModel):
    code: str

@app.post("/api/execute")
async def execute_code(request: CodeRequest):
    try:
        # 파싱
        parse_tree = parser.parse(request.code)
        
        # 의미 분석
        analyzer = SemanticAnalyzer()
        analyzer.visit(parse_tree)
        
        if analyzer.errors:
            return {
                "success": False,
                "errors": [str(error) for error in analyzer.errors]
            }
            
        # TODO: 실제 실행 로직 구현
        # 현재는 더미 데이터 반환
        return {
            "success": True,
            "result": {
                "chart": "bar",
                "x": "카테고리",
                "y": ["값"],
                "data": [
                    ["카테고리", "값"],
                    ["A", 10],
                    ["B", 15],
                    ["C", 7]
                ],
                "title": "범주별 값 비교",
                "xlabel": "카테고리",
                "ylabel": "값",
                "save": "bar_chart.png"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)