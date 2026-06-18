from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_routes import router as reports_router
from fastapi import FastAPI

app = FastAPI()
#try/except
app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(reports_router)