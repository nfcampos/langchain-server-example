"""
Adapted from https://langchain.readthedocs.io/en/latest/getting_started/agents.html
"""

from langchain.agents import load_tools
from langchain.agents import ZeroShotAgent
from langchain.llms import OpenAI

from .patch_langchain import AgentExecutorWithContext


def create_agent(**kawrgs):
    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    agent = ZeroShotAgent.from_llm_and_tools(llm, tools)
    return AgentExecutorWithContext.from_agent_and_tools(
        agent, tools, verbose=True, **kawrgs
    )
