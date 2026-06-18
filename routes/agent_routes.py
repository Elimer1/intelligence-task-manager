from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB

router = APIRouter()
agent = AgentDB()

@router.post("/agents")
def create_agent(data: dict):
    agent.create_agent(data)


@router.get("/agents", status_code=200)
def get_all_agents():
    agent.get_all_agents

@router.get("/agents/{id}", status_code=200)
def get_agent_by_id(id: int):

   if not agent.get_agent_by_id(id):
       raise HTTPException(status_code=404,detail="agent not found")
