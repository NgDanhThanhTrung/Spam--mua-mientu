# app.py - Giữ Render sống + trigger spam
from fastapi import FastAPI
import asyncio
import os
from main import run_spam

app = FastAPI(title="Telegram Test - Render Free")

@app.get("/")
async def root():
    return {"status": "alive ✅", "note": "Truy cập /start-spam để bắt đầu"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/start-spam")
async def start_spam():
    asyncio.create_task(run_spam())  # Chạy nền, không block
    return {"status": "Đã khởi động gửi /mua mientu (background)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
