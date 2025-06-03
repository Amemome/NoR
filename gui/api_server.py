from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sys
import os
import uuid
from datetime import datetime
import matplotlib.pyplot as plt
from lang.nor import NoR

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

# 요청 모델 정의
class CodeRequest(BaseModel):
    code: str
    filename: str = None
    format: str = "png"

@app.post("/api/execute")
async def execute_code(request: CodeRequest):
    try:
        nor = NoR(debug_mode=True, server_mode=True)

        result = nor.run(request.code)

        options = nor.get_graph_props()
        filename = f"{options['이름']}.png"
        
        return {
            "success": True,
            "result": {
                "title": options['옵션']['제목'],
                "xlabel": options['옵션']['x축']['이름'],
                "ylabel": options['옵션']['y축']['이름'],
                "data": [options['x'], options['y']],
                "imageUrl": f"/static/{filename}",
                "filename": filename
            },
            "log": result
        }
    except Exception as e:
        return {
            "success": False,
            "result": {},
            "log": result
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