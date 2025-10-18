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
from src.api.workspaces import router as workspaces_router
from src.api.projects import router as projects_router
from src.api.organization_requests import router as organization_requests_router
from src.api.issue_types import router as issue_types_router
from src.api.issues import router as issues_router
from src.api.analytics import router as analytics_router
from src.api.labels import router as labels_router
from src.api.sprints import router as sprints_router
from src.api.skills import router as skills_router
from src.api.issue_skills import router as issue_skills_router

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


app.include_router(users_router)
app.include_router(organizations_router)
app.include_router(teams_router)
app.include_router(team_members_router)
app.include_router(roles_router)

# Add to your existing routers
app.include_router(workspaces_router)

app.include_router(projects_router)

# Add to your existing routers
app.include_router(organization_requests_router)
app.include_router(issue_types_router)
app.include_router(issues_router)
app.include_router(analytics_router)
app.include_router(labels_router)
app.include_router(sprints_router)
app.include_router(skills_router)
app.include_router(issue_skills_router)
@app.get("/")
async def root():
    return {"message": "Prokoi API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)