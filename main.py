from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from fastapi import FastAPI

app = FastAPI()
#try/except
app.include_router(agent_router)
app.include_router(mission_router)