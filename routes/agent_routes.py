from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB

router = APIRouter()
agent = AgentDB()

@router.post("/agents", status_code=201)
def create_agent(data: dict):
    if data["agent_rank"] not in ["Junior", "Senior", "Commander"]:
        raise HTTPException(status_code=400, detail="rank not allowed")
    if "name" not in data.keys():
        raise HTTPException(status_code=422,detail="missing name")
    if "agent_rank" not in data.keys():
        raise HTTPException(status_code=422,detail="missing rank")
    if "specialty" not in data.keys():
        raise HTTPException(status_code=422,detail="specialty")
    if not data:
        raise HTTPException(status_code=422, detail="no data")

    agent.create_agent(data)
    return {"message": "agent created successfully"}


@router.get("/agents", status_code=200)
def get_all_agents():
    return agent.get_all_agents()

@router.get("/agents/{id}", status_code=200)
def get_agent_by_id(id: int):
    if not type(id) == int:
        raise HTTPException(status_code=422, detail="not a number")
    if not agent.get_agent_by_id(id):
       raise HTTPException(status_code=404,detail="agent not found")
    return agent.get_agent_by_id(id)

@router.put("/agents/{id}")
def update_agent(id: int, data: dict):
    if not type(id) == int:
        raise HTTPException(status_code=422, detail="not a number")
    if not agent.update_agent(id, data):
        raise HTTPException(status_code=404, detail="Agent not found")
    if not data:
        raise HTTPException(status_code=422, detail="no data")
    return {"message": "agent updated successfully"}


@router.put("/agents/{id}/deactivate")
def deactivate_agent(id: int):
    selected_agent = agent.get_agent_by_id(id)
    if not type(id) == int:
        raise HTTPException(status_code=422, detail="not a number")
    if selected_agent["is_active"] == False:
        raise HTTPException(status_code=400, detail="Agent is not active")
    if not selected_agent:
        raise HTTPException(status_code=404,detail="Agent not found")
    
    agent.deactivate_agent(id)
    return {"message" : "agent deactivated successfully"}


@router.get("/agents/{id}/performance")
def get_agent_performance(id: int):
    if agent.get_performance(id):
        return agent.get_performance(id)
    raise HTTPException(status_code=404, detail="agent not found")


#check boolean sitch
#check get agent performance later/fix