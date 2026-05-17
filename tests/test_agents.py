import pytest

from jarvis.agents.orchestrator import Orchestrator


def test_orchestrator_initialization():
    orch = Orchestrator()
    assert "planner" in orch.agents
    assert "coder" in orch.agents
    assert "browser" in orch.agents
    assert "memory" in orch.agents
    assert "research" in orch.agents
    assert "execution" in orch.agents


def test_agent_selection():
    orch = Orchestrator()
    agent = orch._select_agent("write a python script to sort files")
    assert agent.name == "coder"

    agent = orch._select_agent("open google and search for something")
    assert agent.name == "browser"

    agent = orch._select_agent("plan my week")
    assert agent.name == "planner"

    agent = orch._select_agent("remember my favorite color is blue")
    assert agent.name == "memory"

    agent = orch._select_agent("research the latest AI papers")
    assert agent.name == "research"

    agent = orch._select_agent("run ls -la")
    assert agent.name == "execution"
