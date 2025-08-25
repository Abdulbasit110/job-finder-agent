import asyncio
import os
from dotenv import load_dotenv
from agents import Runner
from agent import create_job_finder_agent
from hooks import FullHooks

# Load environment variables from .env file
load_dotenv()

async def main():
    agent = create_job_finder_agent()
    result = await Runner.run(agent, "Find me a job in the field of AI and Machine Learning in the city of San Francisco with 5 years of experience.",hooks=FullHooks)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
