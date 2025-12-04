
from src.notification.connection_manager import WebSocket,manager 
from src.notification.streams import consumer_group , get_pending_notification , listen_for_notifications
import asyncio
from src.notification.streams import publish_message
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter


router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.websocket("/WebSocket/{user_id}/WS_CONNECTION", name="WebSocket Connection")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    # Connect the WebSocket using our connection manager.
    await manager.connect(websocket, str((user_id)))

    

    # Create the consumer group (if it doesn't exist) for the user's stream.
    try:
        await consumer_group(user_id)
        
    except Exception as e:
        print(e)
        await websocket.close()
        return

    # Fetch and deliver any pending notifications.
    try:
        pending = await get_pending_notification(user_id)
        if pending:
            for msg_id, data in pending:
                message = data.get("message")
                if message:
                    # Send a JSON payload with the message and its unique message_id.
                    await websocket.send_json({"message_id": msg_id, "message": message})
        # Do not automatically acknowledge notifications here.
    except Exception as e:
        print("Error processing pending notifications for user %s: %s", user_id, e)

    # Start a background task for listening to real-time notifications.
    listener_task = asyncio.create_task(listen_for_notifications(user_id, websocket))

    try:
        while True:
            data = await websocket.receive_text()
            # Echo back or handle client messages.
            await publish_message(user_id, f"[Echo] {data}")
    except WebSocketDisconnect as e:
        print("WebSocket disconnected: %s", e)
    except Exception as e:
        print("Unexpected error on WebSocket connection: %s", e)
    finally:
        await manager.disconnect(websocket, str(user_id))
        listener_task.cancel()

