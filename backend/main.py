### --- backend/main.py ---
from fastapi import FastAPI, Request
from pydantic import BaseModel
from model import generate_response
import time

app = FastAPI()

class ArticleRequest(BaseModel):
    article: str

@app.get("/api/v1/status")
def status():
    return {
        "status": "ok",
        "available_models": ["Phi-4-mini-instruct"],
        "agents": ["liberal", "conservative", "neutral"]
    }

@app.post("/api/v1/judge")
def judge(request: ArticleRequest):
    start = time.time()
    article = request.article
    results = {}
    for agent in ["liberal", "conservative", "neutral"]:
        summary = generate_response(agent, article)
        # bias_scoreとfactsはここでは仮に設定（将来追加）
        results[agent] = {
            "summary": summary,
            "bias_score": 0.5,  # 仮
            "facts": []         # 仮
        }
    return {
        "results": results,
        "meta": {
            "execution_time": f"{time.time() - start:.2f}s",
            "model_version": "Phi-4-mini-instruct"
        }
    }