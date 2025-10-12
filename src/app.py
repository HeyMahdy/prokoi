from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.users import router as users_router
from src.api.organizations import router as organizations_router
from src.api.teams import router as teams_router
from src.api.team_members import router as team_members_router
from src.core.database import db
from contextlib import asynccontextmanager
from src.api.roles import router as roles_router
from src.middleware.auth import AuthMiddleware
from src.middleware.roleMiddleware import RoleMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await db.create_pool()
    yield
    await db.close()



app = FastAPI(lifespan=lifespan)



# CORS middleware
app.add_middleware(
    AuthMiddleware,
    allow_paths=[
        "/users/signup",
        "/users/login",
        "/docs",
        "/openapi.json",
        "/",
    ],
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)
app.include_router(organizations_router)
app.include_router(teams_router)
app.include_router(team_members_router)
app.include_router(roles_router)


@app.get("/")
async def root():
    return {"message": "Prokoi API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)