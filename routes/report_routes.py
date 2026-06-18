from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB

router = APIRouter()
agent = AgentDB()
mission = MissionDB()

@router.get("/reports/summary")
def get_summary():
    summary_dict = {}
    summary_dict["active_agents_count"] = agent.count_active_agents()
    summary_dict["total_missions"] = mission.count_all_missions()
    summary_dict["open_missions"] = mission.count_by_status("IN PROGRESS") + mission.count_by_status("NEW") + mission.count_by_status("ASSIGNED")
    summary_dict["completed_missions"] = mission.count_by_status("COMPLETED")
    summary_dict["failed_missions"] = mission.count_by_status("FAILED")
    summary_dict["cancelled_missions"] = mission.count_by_status("CANCELLED")
    return summary_dict

@router.get("/reports/missions-by-status")
def get_missions_by_status():
    status_dict = {}
    status_dict["open"] = mission.count_by_status("IN PROGRESS") + mission.count_by_status("NEW") + mission.count_by_status("ASSIGNED")
    status_dict["in_progress"] = mission.count_by_status("IN PROGRESS")
    status_dict["completed"] = mission.count_by_status("COMPLETED")
    status_dict["failed"] = mission.count_by_status("FAILED")
    status_dict["cancelled"] = mission.count_by_status("CANCELLED")
    return status_dict

@router.get("/reports/top-agent")
def get_top_agent():
    return agent.get_agent_by_id(mission.get_top_agent())
    