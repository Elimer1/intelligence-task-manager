## PROJECT BACKROUND AND PURPOSE

An intelligence unit called ShadowNet needs an agent and a task management system
This project will build that agent and task management system by connecting to MYSQL, building tables, and using OOP to manage the data

## FOLDER STRUCTURE

intelligence-task-manager/
├── database/
│ ├── db_connection.py
│ ├── agent_db.py
│ └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore

## AGENTS TABLE STRUCTURE

    **Field**     |       **Type**          | **Comments**

id | INT, AUTO_INCREMENT, PK | Unique identifier
name | VARCHAR |Agent Name
specialty | VARCHAR |
is_active | BOOLEAN | DEFAULT:True
completed_missions| INT |DEFAULT:0
failed_missions | INT |DEFAULT:0
agent_rank | ENUM/VARCHAR |Junior / Senior / Commander only

## MISSIONS TABLE STRUCTURE

    **Field**     |       **Type**          | **Comments**

id | INT, AUTO_INCREMENT, PK | Unique identifier
title | VARCHAR |Mission Title
description | TEXT|Detailed description
location | VARCHAR |
difficulty| INT |1–10 only
importance| INT |1–10 only
status | VARCHAR|Default: NEW
risk_level| VARCHAR | Auto-calculated — not from user
assigned_agent_id | INT |NULL until assigned

## DB CLASSES EXPLANATION

## connection

The DB_connection class is in charge of SQL connection and creating the database and tables

get_connection- Returns an active connection to MySQL with checks for the connection
create_database- Creates Intelligence_db if it does not exist.
create_tables- Creates both tables if they do not exist.

## agent

The AgentDB is responsible for all SQL operations on the agents table

create_agent- Creates a new agent and returns the agent object
get_all_agents- Returns a list of all agents
get_agent_by_id- Returns one agent by ID or None
update_agent- Updates the agent info
deactivate_agent- Sets agent status to inactive
increment_completed- Updates the number of completed missions
increment_failed- Updates the number of failed missions
get_agent_performance- Returns agent performance by completed, failed, total, and success_rate
count_active_agents- Returns the number of active agents

## mission

The MissionDB is responsible for all SQL operations on the missions table

create_mission- Creates a new mission and returns the entire object
get_all_missions- Returns all missions
get_mission_by_id- Returns one mission by ID, or None
assign_mission- Assigns a mission to an agent
update_mission_status- updates status of any mission for any status change
get_open_missions_by_agent- Returns ASSIGNED/IN_PROGRESS missions of an agent
count_all_missions- Counts total missions
count_by_status- Counts missions by a specific status
count_open_missions- Counts open missions
count_critical_missions- Counts CRITICAL missions
get_top_agent- Returns the agent with the highest completed_missions

## SYSTEM RULES

1. Rank must be Junior / Senior / Commander — any other value throws an error.
2. Difficulty and importance must be between 1 and 10 — otherwise an error.
3. Risk_level is calculated automatically when creating a mission — the user does not submit it.
4. An agent with is_active=False cannot accept missions.
5. An agent cannot have more than 3 open missions (ASSIGNED / IN_PROGRESS) at the same time.
6. If risk_level=CRITICAL — only an agent with the Commander rank can accept the mission.
7. Only a mission with the status NEW can be assigned. After assignment: status=ASSIGNED.
8. Only a mission with the status ASSIGNED can be started. After: status=IN_PROGRESS.
9. Only a mission with the status IN_PROGRESS can be finished and changed to failed or completed status
10. Only a mission with the status NEW or ASSIGNED can be canceled — otherwise an error.

## RUN INSTRUCTIONS

docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
