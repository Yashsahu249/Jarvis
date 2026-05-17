import asyncio
from fastapi import APIRouter, HTTPException
from loguru import logger
from app.models.schemas import AgentInfo, AgentTask
from app.services.agent_service import agent_service

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("", response_model=list[AgentInfo])
async def list_agents():
    agents = agent_service.list_agents()
    return [AgentInfo(**a) for a in agents]


@router.get("/{agent_id}", response_model=AgentInfo)
async def get_agent(agent_id: str):
    agent = agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    return AgentInfo(**agent)


@router.post("/{agent_id}/tasks", response_model=AgentTask)
async def assign_task(agent_id: str, task_data: dict):
    if not agent_service.get_agent(agent_id):
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

    task_type = task_data.get("type", "general")
    description = task_data.get("description", "")
    input_data = task_data.get("input", {})

    task = agent_service.create_task(agent_id, task_type, description, input_data)

    asyncio.create_task(agent_service.execute_task(task["id"]))

    return AgentTask(**task)


@router.get("/{agent_id}/tasks", response_model=list[AgentTask])
async def get_agent_tasks(agent_id: str):
    if not agent_service.get_agent(agent_id):
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

    tasks = agent_service.get_tasks(agent_id)
    return [AgentTask(**t) for t in tasks]


@router.get("/{agent_id}/memory")
async def get_agent_memory(agent_id: str):
    if not agent_service.get_agent(agent_id):
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

    memory = agent_service.get_agent_memory(agent_id)
    return {"agent_id": agent_id, "memory": memory}
