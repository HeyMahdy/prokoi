from fastapi import HTTPException, Request, Depends
from src.repositories.RolesRepository import RolesRepository

rolesRepo = RolesRepository()


def require_permissions(permissions: list[str]):
    """Create a dependency that checks user permissions"""

    async def check_permissions(request: Request):
        user = getattr(request.state, "user", None)
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        has_permission = await rolesRepo.is_permission(user["id"], permissions)
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        return user

    return check_permissions