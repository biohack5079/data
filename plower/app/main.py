# ~/data/plower/app/main.py

import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()

# 環境変数からAPIキーを取得
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    # 実際にはサーバー起動時にチェックする
    print("FATAL: GEMINI_API_KEY is not set in the .env file.") 

# Geminiクライアントの初期化
client = genai.Client(api_key=GEMINI_API_KEY)
app = FastAPI()

# ⚠️ CORS設定: フロントエンドのポートと合わせてください
# ローカルで開発する場合、許可するオリジンを設定します。
origins = [
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:8000", # FastAPIのポート
    "http://localhost:5500", # Live ServerなどのHTML実行環境のポート
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 開発中は * でも良いが、本番では上記リストに絞るべき
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストボディの型定義
class GeminiRequest(BaseModel):
    model: str = "gemini-1.5-flash" # デフォルトモデル
    prompt: str
    temperature: float = 0.1
    
# ヘルスチェックエンドポイント
@app.get("/")
def read_root():
    return {"message": "Plower Gemini Proxy is running"}

# Gemini APIを中継するプロキシエンドポイント
@app.post("/api/gemini_proxy")
async def gemini_proxy(request_data: GeminiRequest):
    """
    フロントエンドからのプロンプトを受け取り、Gemini APIに安全にリクエストを送信する。
    """
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server API Key is not configured."
        )

    try:
        # Gemini APIの呼び出し
        response = client.models.generate_content(
            model=request_data.model,
            contents=request_data.prompt,
            config=genai.types.GenerateContentConfig(
                temperature=request_data.temperature
            )
        )
        # 返却するレスポンスを整形
        return {"response": response.text}
        
    except Exception as e:
        error_detail = str(e)
        # より詳細なエラーをロギングし、クライアントには汎用的なエラーを返す
        print(f"Gemini API Call Error: {error_detail}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during AI generation. Please check the server logs."
        )

# バックエンド実行コマンド (plowerフォルダ内)
# $ cd app
# $ uvicorn main:app --reload --port 8000