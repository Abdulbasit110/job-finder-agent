from agents import Agent
from tools import search_jobs_with_firecrawl, get_job_details_from_url
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, List

load_dotenv()

class JobSearchResult(BaseModel):
    title: str
    company: str
    location: str
    salary_range: Optional[str] = ""
    skills: Optional[List[str]] = []
    application_url: Optional[str] = ""
    description: Optional[str] = ""
    date_posted: Optional[str] = ""
    experience_level: Optional[str] = ""
    source: Optional[str] = ""
    type: Optional[str] = ""

def create_job_finder_agent():
    """Create and return a Job Finder agent."""
    agent = Agent(
        name="Job Finder",
        instructions="""You are a helpful assistant that finds jobs for people. 
        You can search for jobs across major job websites using Firecrawl to extract relevant job postings.
        
        When a user asks for job recommendations:
        1. Use the search_jobs_with_firecrawl function to find relevant jobs
        2. If they want more details about a specific job, use get_job_details_from_url
        3. Present the results in a clear, organized manner
        4. Focus on matching their specific requirements (location, experience level, etc.) 
        """,
        tools=[search_jobs_with_firecrawl, get_job_details_from_url],
        output_type=List[JobSearchResult]
    )
    return agent
