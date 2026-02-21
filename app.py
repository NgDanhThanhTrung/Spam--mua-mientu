# app.py
from fastapi import FastAPI, Path
import asyncio
from main import run_spam, stop_spam, is_spamming

app = FastAPI(title="Telegram Spam Test - Render Free")

@app.get("/")
async def root():
    status = "đang spam" if is_spamming() else "nghỉ"
    return {
        "status": "alive ✅",
        "current": status,
        "usage": "Truy cập /{command} để gửi 300 tin dạng '/command' (ví dụ: /mua-ban-hang, /abc-xyz)\n"
                 "Dùng /stop để dừng ngay lập tức nếu đang chạy"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/{command}")
async def start_spam(command: str = Path(..., description="Cụm lệnh, hỗ trợ dấu gạch ngang như mua-ban-hang")):
    full_cmd = f"/{command.replace('-', ' ')}"  # thay - bằng khoảng trắng → "/mua ban hang"
    asyncio.create_task(run_spam(full_cmd))
    return {"status": f"Đã khởi động gửi đúng 300 tin '{full_cmd}' (nội dung khác nhau mỗi lần)"}

@app.get("/stop")
async def stop():
    stop_spam()
    return {"status": "Đã yêu cầu dừng spam. Task sẽ dừng trong vài giây."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
