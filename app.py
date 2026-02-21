# app.py
from fastapi import FastAPI
import asyncio
from main import run_spam, stop_spam, is_spamming  # import thêm các hàm/biến từ main

app = FastAPI(title="Telegram Spam Test - Render Free")

# Biến toàn cục để theo dõi trạng thái (có thể dùng class hoặc dict nếu phức tạp hơn)
@app.get("/")
async def root():
    status = "đang spam" if is_spamming() else "nghỉ"
    return {
        "status": "alive ✅",
        "current": status,
        "usage": "Truy cập: /mientu | /buatx | /vecuop để gửi 300 tin\n/stop để dừng ngay lập tức"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/mientu")
async def start_mientu():
    asyncio.create_task(run_spam("/mua mientu"))
    return {"status": "Đã khởi động gửi 300 tin '/mua mientu'"}

@app.get("/buatx")
async def start_buatx():
    asyncio.create_task(run_spam("/mua buatx"))
    return {"status": "Đã khởi động gửi 300 tin '/mua buatx'"}

@app.get("/vecuop")
async def start_vecuop():
    asyncio.create_task(run_spam("/mua vecuop"))
    return {"status": "Đã khởi động gửi 300 tin '/mua vecuop'"}

@app.get("/stop")
async def stop():
    stop_spam()  # gọi hàm dừng
    return {"status": "Đã yêu cầu dừng spam. Task sẽ dừng trong vài giây (sau delay hiện tại)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
