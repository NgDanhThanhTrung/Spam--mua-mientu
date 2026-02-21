# main.py
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
import asyncio
import os
import random
import time
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")
phone = os.getenv("PHONE")                  # dự phòng nếu session cần login lại
target_id = int(os.getenv("TARGET_USER_ID"))

client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def run_spam(base_cmd: str):
    print(f"Khởi động task gửi 300 tin với lệnh: {base_cmd}")

    await client.connect()

    if not await client.is_user_authorized():
        print("Session chưa authorized.")
        if phone:
            try:
                await client.send_code_request(phone)
                print(f"Code đã được gửi đến {phone}. Render không thể nhập code → tạo SESSION_STRING local và redeploy.")
            except Exception as e:
                print(f"Lỗi khi yêu cầu code: {e}")
        else:
            print("Thiếu PHONE trong biến môi trường → không thể yêu cầu code.")
        return

    print("Đã authorized → bắt đầu gửi 300 tin")

    count = 0
    max_messages = 300  # CỐ ĐỊNH 300 TIN

    while count < max_messages:
        try:
            # Tạo nội dung khác nhau mỗi lần
            message = f"{base_cmd} #{count+1} - {time.strftime('%H:%M:%S')}"

            await client.send_message(target_id, message)
            count += 1
            print(f"Gửi {count}/{max_messages}: {message}")

            # Delay random để giảm rủi ro flood
            await asyncio.sleep(random.uniform(1.2, 3.5))

        except FloodWaitError as e:
            print(f"Flood wait {e.seconds} giây → đang chờ...")
            await asyncio.sleep(e.seconds + 15)
            if e.seconds > 3600:
                print("Flood wait quá dài (>1 giờ) → dừng task để an toàn.")
                break

        except Exception as e:
            print(f"Lỗi: {e}")
            if "peer" in str(e).lower() or "invalid" in str(e).lower():
                print("→ Có thể acc nhận chưa kết nối peer. Chat thủ công 1 tin từ acc gửi sang acc nhận trước.")
            break

    print(f"Hoàn thành task: {count}/{max_messages} tin đã gửi.")
