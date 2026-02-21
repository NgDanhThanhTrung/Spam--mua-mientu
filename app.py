# app.py
from fastapi import FastAPI
import asyncio
from main import run_spam

app = FastAPI(title="Telegram Spam Test - Render Free")

@app.get("/")
async def root():
    return {
        "status": "alive ✅",
        "usage": "Truy cập một trong các đường dẫn sau để gửi đúng 300 tin:\n"
                 "- /mientu\n"
                 "- /buatx\n"
                 "- /vecuop"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/mientu")
async def start_mientu():
    asyncio.create_task(run_spam("/mua mientu"))
    return {"status": "Đã khởi động gửi đúng 300 tin '/mua mientu' (nội dung khác nhau)"}

@app.get("/buatx")
async def start_buatx():
    asyncio.create_task(run_spam("/mua buatx"))
    return {"status": "Đã khởi động gửi đúng 300 tin '/mua buatx' (nội dung khác nhau)"}

@app.get("/vecuop")
async def start_vecuop():
    asyncio.create_task(run_spam("/mua vecuop"))
    return {"status": "Đã khởi động gửi đúng 300 tin '/mua vecuop' (nội dung khác nhau)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
