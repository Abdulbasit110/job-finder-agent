from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
from agents import Runner
from agent import create_job_finder_agent
from hooks import FullHooks

# Initialize FastAPI app
app = FastAPI(
    title="JobGPT API",
    description="Simple API for finding jobs using AI agent with Firecrawl integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class JobSearchRequest(BaseModel):
    query: str
    location: Optional[str] = ""
    experience_level: Optional[str] = ""

class JobSearchResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class AgentStatusResponse(BaseModel):
    status: str
    agent_name: str
    available_tools: list

# Global agent instance
job_agent = None

@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup"""
    global job_agent
    job_agent = create_job_finder_agent()
    print("Job Finder Agent initialized successfully!")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "JobGPT API - Simple Job Search with AI", 
        "version": "1.0.0",
        "endpoints": {
            "/search-jobs": "POST - Search for jobs with AI agent",
            "/job-details": "POST - Get details from job URL",
            "/agent-status": "GET - Get agent status",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent_ready": job_agent is not None}

@app.get("/agent-status", response_model=AgentStatusResponse)
async def get_agent_status():
    """Get the current status of the job finder agent"""
    if not job_agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    return AgentStatusResponse(
        status="ready",
        agent_name=job_agent.name,
        available_tools=["search_jobs_with_firecrawl", "get_job_details_from_url"]
    )

@app.post("/search-jobs", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest):
    """
    Search for jobs using the AI agent
    
    - **query**: Job title or keywords (required)
    - **location**: Location preference (optional)  
    - **experience_level**: Experience level (optional)
    """
    if not job_agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        # Create the search message for the agent
        search_message = f"Find me jobs for: {request.query}"
        
        if request.location:
            search_message += f" in {request.location}"
            
        if request.experience_level:
            search_message += f" for {request.experience_level} level"
        
        # Run the agent
        print(f"🔍 Searching jobs with query: {search_message}")
        result = await Runner.run(job_agent, search_message , hooks=FullHooks)
        
        return JobSearchResponse(
            success=True,
            message="Job search completed successfully",
            data={
                "agent_response": result.final_output,
                "search_query": request.query,
                "location": request.location,
                "experience_level": request.experience_level
            }
        )
        
    except Exception as e:
        print(f"❌ Error during job search: {str(e)}")
        return JobSearchResponse(
            success=False,
            message="Job search failed",
            error=str(e)
        )

@app.post("/job-details")
async def get_job_details(job_url: str):
    """
    Get detailed information about a specific job posting
    
    - **job_url**: URL of the job posting
    """
    if not job_agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        # Create message for getting job details
        details_message = f"Get detailed information about this job posting: {job_url}"
        
        print(f"📋 Getting job details for: {job_url}")
        result = await Runner.run(job_agent, details_message,hooks=FullHooks)
        
        return JobSearchResponse(
            success=True,
            message="Job details retrieved successfully",
            data={
                "agent_response": result.final_output,
                "job_url": job_url
            }
        )
        
    except Exception as e:
        print(f"❌ Error getting job details: {str(e)}")
        return JobSearchResponse(
            success=False,
            message="Failed to get job details",
            error=str(e)
        )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
