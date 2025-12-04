import os

def get_stream_key(user_id: int) -> str:
    env = os.getenv("APP_ENV", "local")
    app = "notiq"
    stream_prefix = "notifications"
    return f"{env}:{app}:{stream_prefix}:{user_id}"

def get_group_name() -> str:
    env = os.getenv("APP_ENV", "local")
    app = "notiq"
    group_prefix = "notification_group"
    return f"{env}:{app}:{group_prefix}"