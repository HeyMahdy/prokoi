from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.users import router as users_router
from src.core.database import db
from contextlib import asynccontextmanager
from src.api.roles import router as roles_router
from src.middleware.auth import AuthMiddleware
from src.middleware.roleMiddleware import RoleMiddleware

from src.api.skills import router as skills_router
from src.api.jobs import router as jobs_router
from src.api.resources import router as resources_router
from src.api.bookmarks import router as bookmarks_router
from src.api.roadmaps import router as roadmaps_router
from src.api.skill_verification_tests import router as skill_tests_router


# Add to your existing routers


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
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(skills_router)

app.include_router(users_router)

app.include_router(roles_router)

app.include_router(jobs_router)

app.include_router(resources_router)

app.include_router(bookmarks_router)

app.include_router(roadmaps_router)

app.include_router(skill_tests_router)


@app.get("/")
async def root():
    return {"message": "Prokoi API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)