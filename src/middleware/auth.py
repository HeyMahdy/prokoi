from typing import Callable, Awaitable
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from src.core.config import settings
from src.repositories.users import UserRepository
import pprint
class AuthMiddleware:
    def __init__(self, app, allow_paths: list[str] | None = None):
        self.app = app
        self.allow_paths = set(allow_paths or [])

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive=receive)
        path = scope.get("path") or "/"

        # Allowlist (e.g., open routes)
        if path in self.allow_paths:
            return await self.app(scope, receive, send)

        auth = request.headers.get("authorization", "")
        print(auth)
        if not auth.startswith("Bearer "):
            return await JSONResponse({"detail": "Not authenticated"}, status_code=401)(scope, receive, send)

        token = auth.removeprefix("Bearer ").strip()
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email = payload.get("sub")
            if not email:
                raise JWTError("Missing subject")
        except JWTError:
            return await JSONResponse({"detail": "Invalid token"}, status_code=401)(scope, receive, send)

        # Load user
        repo = UserRepository()
        user = await repo.find_user_by_email(email)
        if not user:
            return await JSONResponse({"(detail": "User not found"}, status_code=401)(scope, receive, send)

        # Attach user to request.state for downstream handlers
        scope.setdefault("state", {})
        request.state.user = user


        return await self.app(scope, receive, send)
