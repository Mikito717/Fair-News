# --- backend/main.py ---
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from model import generate_response, check_ollama_model, model_manager, ModelBackend
import time
from typing import Optional

app = FastAPI()


class ArticleRequest(BaseModel):
    article: str
    backend: Optional[str] = None
    model_name: Optional[str] = None


class BackendSwitchRequest(BaseModel):
    backend: str  # "ollama" or "transformers"
    model_name: Optional[str] = None


@app.get("/api/v1/status")
def status():
    return {
        "status": "ok",
        "available_backends": model_manager.get_available_backends(),
        "current_backend": model_manager.backend.value if model_manager.backend else None,
        "available_ollama_models": model_manager.get_ollama_models(),
        "suggested_models": ["llama3.2", "llama3", "qwen2.5", "phi4"],
        "agents": ["liberal", "conservative", "neutral"],
        "ollama_available": check_ollama_model()
    }


@app.post("/api/v1/switch-backend")
def switch_backend(request: BackendSwitchRequest):
    """バックエンドを切り替える"""
    try:
        backend_enum = ModelBackend(request.backend)
        success = model_manager.switch_backend(
            backend_enum, request.model_name)

        if success:
            return {
                "success": True,
                "message": f"バックエンドを{request.backend}に切り替えました",
                "current_backend": model_manager.backend.value,
                "model_name": request.model_name
            }
        else:
            raise HTTPException(status_code=400, detail="バックエンドの切り替えに失敗しました")

    except ValueError:
        raise HTTPException(status_code=400, detail="無効なバックエンドです")


@app.post("/api/v1/judge")
def judge(request: ArticleRequest):
    start = time.time()
    article = request.article

    # リクエストでバックエンドが指定されている場合、一時的に切り替え
    if request.backend:
        try:
            backend_enum = ModelBackend(request.backend)
            if not model_manager.switch_backend(backend_enum, request.model_name):
                raise HTTPException(
                    status_code=400, detail="指定されたバックエンドに切り替えできませんでした")
        except ValueError:
            raise HTTPException(status_code=400, detail="無効なバックエンドです")

    # デフォルトバックエンドが設定されていない場合、自動で設定
    if model_manager.backend is None:
        if not model_manager.switch_backend(ModelBackend.OLLAMA, "llama3.2"):
            if not model_manager.switch_backend(ModelBackend.TRANSFORMERS):
                raise HTTPException(
                    status_code=500, detail="利用可能なバックエンドがありません")

    results = {}
    for agent in ["liberal", "conservative", "neutral"]:
        response_data = generate_response(agent, article, request.model_name)
        results[agent] = {
            "summary": response_data["summary"],
            "bias_score": response_data["bias_score"],
            "facts": []         # 仮
        }

    return {
        "results": results,
        "meta": {
            "execution_time": f"{time.time() - start:.2f}s",
            "backend": model_manager.backend.value if model_manager.backend else "unknown",
            "model_name": request.model_name or "default"
        }
    }
