from fastapi import APIRouter,HTTPException
from database.mission_db import MissionDB
from database.agent_db import AgentDB

router = APIRouter()
mission = MissionDB()
agent = AgentDB()

@router.post("/missions", status_code=201)
def create_missions(data: dict):
    mission.create_mission(data)
    return {"message": "mission added succesfully"}

@router.get("/missions")
def get_all_missions():
    return mission.get_all_missions()

@router.get("/missions/{id}")
def get_mission_by_id(id: int):
    if mission.get_mission_by_id(id):
        return mission.get_mission_by_id(id)
    raise HTTPException(status_code=404, detail="Mission not found")

@router.put("/missions/{id}/assign/{agent_id}")
def assign_mission(id: int, agent_id: int):
    selected_mission = mission.get_mission_by_id(id)
    selected_agent = agent.get_agent_by_id(agent_id)

    if not selected_mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if not selected_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if not selected_mission["status"] == "NEW":
        raise HTTPException(status_code=400,detail="Mission not available")
    if not selected_agent["is_active"]:
        raise HTTPException(status_code=400, detail="Agent is not active")
    if len(mission.get_open_missions_by_agent(agent_id)) >= 3:
        raise HTTPException(status_code=400, detail="agent has reached maximum missions")
    if selected_mission["risk_level"] == "CRITICAL" and selected_agent["agent_rank"] != "Commander":
        raise HTTPException(status_code=400, detail="Only commander can handle critical missions")
    
    mission.assign_mission(id, agent_id)
    return {"message": "mission assigned successfully"}

@router.put("/missions/{id}/start")
def mission_start(id):
    selected_mission = mission.get_mission_by_id(id)
    if not selected_mission:
        raise HTTPException(status_code=404,detail="Mission not found")
    if selected_mission["status"] != "ASSIGNED":
        raise HTTPException(status_code=400,detail="Status is not NEW")
     
    mission.update_mission_status(id, "IN_PROGRESS")
    return {"message": "mission has started"}

@router.put("/missions/{id}/complete")
def mission_complete(id: int):
    selected_mission = mission.get_mission_by_id(id)
    if not selected_mission:
        raise HTTPException(status_code=404,detail="Mission not found")
    if selected_mission["status"] != "IN_PROGRESS":
        raise HTTPException(status_code=400,detail="mission is not IN_PROGRESS")
     
    mission.update_mission_status(id, "COMPLETED")
    return {"message": "mission has been completed"}

@router.put("/missions/{id}/fail")
def mission_complete(id: int):
    selected_mission = mission.get_mission_by_id(id)
    if not selected_mission:
        raise HTTPException(status_code=404,detail="Mission not found")
    if selected_mission["status"] != "IN_PROGRESS":
        raise HTTPException(status_code=400,detail="mission is not IN_PROGRESS")
     
    mission.update_mission_status(id, "FAILED")
    return {"message": "mission failed"}

@router.put("/missions/{id}/cancel")
def mission_complete(id: int):
    selected_mission = mission.get_mission_by_id(id)
    if not selected_mission:
        raise HTTPException(status_code=404,detail="Mission not found")
    if selected_mission["status"] != "IN_PROGRESS":
        raise HTTPException(status_code=400,detail="mission is not IN_PROGRESS")
     
    mission.update_mission_status(id, "CANCELLED")
    return {"message": "mission has been cancelled"}