from routes.agent_routes import router as agent_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(agent_router)