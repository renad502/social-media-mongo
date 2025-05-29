import httpx
from typing import List
from app.core.config import ONESIGNAL_API_KEY, ONESIGNAL_APP_ID

ONESIGNAL_API_URL = "https://onesignal.com/api/v1/notifications"

async def send_notification_via_onesignal(user_ids: List[str], heading: str, content: str, data: dict = None):
    headers = {
        "Authorization": f"Basic {ONESIGNAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "include_external_user_ids": user_ids,
        "headings": {"en": heading},
        "contents": {"en": content},
        "data": data or {},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(ONESIGNAL_API_URL, json=payload, headers=headers)
        if response.status_code != 200:
            print("OneSignal error:", response.status_code, response.text)
        else:
            print("Notification sent via OneSignal")
