from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB

router = APIRouter()
agent = AgentDB()

@router.post("/agents", status_code=201)
def create_agent(data: dict):
    agent.create_agent(data)
    return {"message": "agent created successfully"}


@router.get("/agents", status_code=200)
def get_all_agents():
    return agent.get_all_agents()

@router.get("/agents/{id}", status_code=200)
def get_agent_by_id(id: int):

    if not agent.get_agent_by_id(id):
       raise HTTPException(status_code=404,detail="agent not found")
    return agent.get_agent_by_id(id)

@router.put("/agents/{id}")
def update_agent(id: int, data: dict):
    if not agent.update_agent(id, data):
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {"message": "agent updated successfully"}


@router.put("/agents/{id}/deactivate")
def deactivate_agent(id: int):
    selected_agent = agent.get_agent_by_id(id)
    if selected_agent["is_active"] == False:
        raise HTTPException(status_code=400, detail="Agent is not active")
    if not selected_agent:
        raise HTTPException(status_code=404,detail="Agent not found")
    
    agent.deactivate_agent(id)
    return {"message" : "agent deactivated successfully"}


@router.get("/agents/{id}/performance")
def get_agent_performance(id: int):
    return agent.get_agent_performance(id)


#check boolean sitch
#check get agent performance later/fix