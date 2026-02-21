# main.py - Gửi /mua mientu bằng Telethon
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError, SessionPasswordNeededError
import asyncio
import os
import random
from dotenv import load_dotenv

load_dotenv()

# Lấy từ Environment Variables trên Render
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")  # Chuỗi dài (ưu tiên)
phone = os.getenv("PHONE")                    # SĐT (+84...) - dự phòng nếu session cần
target_id = int(os.getenv("TARGET_USER_ID"))

client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def run_spam():
    print("Kết nối Telegram...")

    await client.connect()

    if not await client.is_user_authorized():
        print("Session chưa authorized → cần login lần đầu.")
        if not phone:
            print("❌ Thiếu PHONE trong env! Không thể gửi code.")
            return

        try:
            await client.send_code_request(phone)
            print(f"Code đã gửi đến {phone}. Nhưng Render không interactive → kiểm tra Telegram app để lấy code, rồi redeploy với code nếu cần.")
            # Lưu ý: Render không cho nhập code → bạn phải xử lý manual lần đầu (hoặc dùng local để tạo session)
            # Nếu bạn muốn tự động hơn → chuyển sang bot token thay vì user account.
            return  # Dừng nếu cần code
        except Exception as e:
            print(f"Lỗi gửi code: {e}")
            return

    print("✅ Đã authorized → bắt đầu gửi tin nhắn")

    count = 0
    max_messages = 300  # Chỉnh số lượng test

    print("🚀 Bắt đầu gửi /mua mientu...")

    while count < max_messages:
        try:
            await client.send_message(target_id, "/mua mientu")
            count += 1
            print(f"✅ Gửi {count}: /mua mientu → ID {target_id}")

            # Delay random 1.2-3.0s để an toàn
            await asyncio.sleep(random.uniform(1.2, 3.0))

        except FloodWaitError as e:
            print(f"⏳ Flood wait {e.seconds}s → chờ...")
            await asyncio.sleep(e.seconds + 15)
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            if "peer" in str(e).lower():
                print("→ Chat thủ công 1 tin từ acc gửi sang acc nhận để kết nối peer.")
            break

    print(f"🏁 Hoàn thành: {count} tin nhắn")
