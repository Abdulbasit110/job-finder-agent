from agents import Agent, Tool, RunHooks
from typing import  Any

class FullHooks(RunHooks):
    async def on_agent_start(self, agent: Agent) -> None:
        print(f"\n=== AGENT START === {agent.name}")

    async def on_agent_end(self, agent: Agent, output: Any) -> None:
        print(f"=== AGENT END === {agent.name}")

    async def on_llm_start(self, agent: Agent, prompt: str) -> None:
        print(f"[LLM START] agent={agent.name}")
        print("---- prompt to model ----")
        print(prompt)
        print("-------------------------")

    async def on_llm_end(self, agent: Agent, response: str) -> None:
        print("\n[LLM END]")
        print("---- model full response ----")

    async def on_tool_start(self, agent: Agent, tool: Tool) -> None:
        print(f"\n[TOOL START] {tool.name}")
        print("args:", tool)

    async def on_tool_end(self, agent: Agent, tool: Tool, result: Any) -> None:
        print(f"[TOOL END] {tool}")
