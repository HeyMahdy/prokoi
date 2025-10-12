from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from src.core.config import settings
from src.repositories.users import UserRepository
from src.repositories.RolesRepository import RolesRepository


class RoleMiddleware:
    def __init__(self, app, allow_paths: list[str] | None = None, path_permissions: dict = None):
        self.app = app
        self.path_permissions = path_permissions or {}  # {"path": ["perm1", "perm2"]}
        self.allow_paths = allow_paths or []
        self.repo = RolesRepository()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive=receive)
        path = scope.get("path") or "/"

        # Check if path is allowed (no permission check needed)
        if path in self.allow_paths:
            return await self.app(scope, receive, send)

        # Check if path needs permission check
        required_permissions = self.path_permissions.get(path, [])
        if not required_permissions:
            # No permission check needed for this path
            return await self.app(scope, receive, send)

        try:
            print("this will be fycking users")

            user = request.scope.get("user")
            print(user)

            if not user:
                return await JSONResponse({"detail": "Not authenticated"}, status_code=401)(scope, receive, send)

            user_id = user["id"]
            result = await self.repo.is_permission(user_id, required_permissions)

            if result is True:
                return await self.app(scope, receive, send)
            else:
                return await JSONResponse({"detail": "Insufficient permissions"}, status_code=403)(scope, receive, send)
        except Exception as e:
            return await JSONResponse({"detail": "Error in permission middleware"}, status_code=500)(scope, receive,
                                                                                                     send)














