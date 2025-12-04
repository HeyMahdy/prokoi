import logging
import time
import asyncio
from typing import Any, Dict, List, Tuple
from fastapi import status

from src.notification.client import get_redis_client

from src.notification.helpers import get_group_name , get_stream_key





GROUP_NAME : str = get_group_name()
MAX_STREAM_LENGTH :int = 1000
XREAD_TIMEOUT : int = 5000
XREAD_COUNT : int = 1
ERROR_SLEEP_SEC: float = 1
redis_client = get_redis_client()

async def publish_message(user_id:int , message:str):
    stream_key : str = get_stream_key(user_id)
    payload : Dict[str,Any] = {"message": message, "timestamp": str(time.time())}
    try:
        msg_id = await redis_client.xadd(
            stream_key,
            payload,
            maxlen=MAX_STREAM_LENGTH,
            approximate=True,

        )
        return msg_id

    except Exception as e:
        print(e)

async def consumer_group(user_id:int):
    stream_key : str = get_stream_key(user_id)
    try:
        await redis_client.xgroup_create(
            stream_key,GROUP_NAME,id="0-0",mkstream=True
        )
    except Exception as e:
        if "BUSYGROUP" in str(e):
            print("Consumer group already exists for stream")
        else:
            print(e)



async def get_pending_notification(user_id:int):
    stream_key : str = get_stream_key(user_id)
    consumer_name = str(user_id)
    notification : List[Tuple[str, Dict[str, Any]]] = []
    try:
        pending_resp = await redis_client.xreadgroup(GROUP_NAME,consumer_name,{stream_key: "0"},
            count=100,
            block=0)
        if pending_resp:
            for _stream, messages in pending_resp:
                notification.extend(messages)
    except Exception as exc:
        print("Error reading pending notifications from %s: %s", stream_key, exc)
    return notification

    
async def listen_for_notifications(user_id:int, websocket) -> None:
    """
    Continuously listen for new notifications from the user's Redis stream and deliver them.
    """
    stream_key: str = get_stream_key(user_id)
    consumer_name = str(user_id)

    while True:
        try:
            new_resp = await redis_client.xreadgroup(
                GROUP_NAME,
                consumer_name,
                {stream_key: ">"},
                count=XREAD_COUNT,
                block=XREAD_TIMEOUT
            )
            if new_resp:
                for _stream, messages in new_resp:
                    for msg_id, data in messages:
                        message = data.get("message")
                        if message:
                            await websocket.send_json({"message_id": msg_id, "message": message})
            else:
                await asyncio.sleep(ERROR_SLEEP_SEC)
        except Exception as exc:
            print("Error listening for notifications on stream %s: %s", stream_key, exc)
            await asyncio.sleep(ERROR_SLEEP_SEC)

async def acknowledge_notifications(user_id: int, message_ids: List[str]) -> None:
    """
    Acknowledge (XACK) messages so that they are not redelivered.
    """
    stream_key: str = get_stream_key(user_id)
    print("this is the key")
    print(stream_key)
    try:
        if message_ids:
            await redis_client.xack(stream_key, GROUP_NAME, *message_ids)
    except Exception as exc:
        print("Error acknowledging messages on stream %s: %s", stream_key, exc)
        raise RuntimeError(f"Error acknowledging messages on stream {stream_key}: {exc}")  
        