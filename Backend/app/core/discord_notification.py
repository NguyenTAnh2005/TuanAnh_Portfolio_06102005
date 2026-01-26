import httpx
from app.core.config import settings
from datetime import datetime, timezone, timedelta

# lấy thời gian UTC hiện tại
# utc_now = datetime.now(timezone.utc)
# Cài đặt múi giờ GMT+7
# gmt_plus_7 = timezone(timedelta(hours=7))

async def send_discord_alert(title:str, description: str, color: int = 3066993 ):
    """
    Send a notification message to a Discord channel using a webhook.
    """
    url = settings.DISCORD_WEB_HOOK
    if not url:
        print("🚨 Không tìm thấy đường dẫn DISCORD_WEB_HOOK, kiểm tra .env hoặc config pydantic setting file!")
        return
    payload = {
        "embeds":[
            {
                "title" : title,
                "description": description,
                "color" : color,
                "footer": {"text" : "Portfolio System - Admin Guard!"},
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        ]
    }
    async with httpx.AsyncClient() as Client:
        try:
            response = await Client.post(url, json = payload)
            if response.status_code != 204:
                print(f"❌ Lỗi gửi Discord: {response.status_code}")
        except Exception as e:
            print(f"❌ Lỗi kết nối Discord: {e}")