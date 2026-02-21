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
phone = os.getenv("PHONE")
target_id = int(os.getenv("TARGET_USER_ID"))

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Flag để dừng task
_stop_flag = False
_is_running = False

def stop_spam():
    global _stop_flag
    _stop_flag = True
    print("Yêu cầu dừng spam đã nhận. Task sẽ dừng sớm.")

def is_spamming():
    global _is_running
    return _is_running

async def run_spam(base_cmd: str):
    global _stop_flag, _is_running

    if _is_running:
        print("Task đang chạy → bỏ qua yêu cầu mới.")
        return

    _is_running = True
    _stop_flag = False
    print(f"Khởi động gửi 300 tin với lệnh: {base_cmd}")

    await client.connect()

    if not await client.is_user_authorized():
        print("Session chưa authorized.")
        if phone:
            try:
                await client.send_code_request(phone)
                print(f"Code gửi đến {phone}. Render không nhập code → tạo SESSION_STRING local.")
            except Exception as e:
                print(f"Lỗi yêu cầu code: {e}")
        else:
            print("Thiếu PHONE.")
        _is_running = False
        return

    print("Authorized → bắt đầu gửi")

    count = 0
    max_messages = 300  # cố định 300

    while count < max_messages:
        if _stop_flag:
            print(f"Dừng sớm tại tin {count}/{max_messages}")
            break

        try:
            message = f"{base_cmd} #{count+1} - {time.strftime('%H:%M:%S')}"

            await client.send_message(target_id, message)
            count += 1
            print(f"Gửi {count}/{max_messages}: {message}")

            await asyncio.sleep(random.uniform(1.2, 3.5))

        except FloodWaitError as e:
            print(f"Flood wait {e.seconds}s → chờ...")
            await asyncio.sleep(e.seconds + 15)
            if e.seconds > 3600:
                print("Flood quá dài (>1h) → dừng task.")
                break

        except Exception as e:
            print(f"Lỗi: {e}")
            if "peer" in str(e).lower():
                print("→ Chat thủ công 1 tin trước để kết nối peer.")
            break

    print(f"Hoàn thành: {count}/{max_messages} tin")
    _is_running = False
    _stop_flag = False
