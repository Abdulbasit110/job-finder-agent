import os
from firecrawl import Firecrawl
from typing import List, Dict, Any
from agents import function_tool

@function_tool
def search_jobs_with_firecrawl(job_query: str, location: str = "", experience_level: str = "") -> Dict[str, Any]:
    """
    Search for jobs using Firecrawl to extract data from major job websites.
    
    Args:
        job_query (str): The job title or keywords to search for (e.g., "AI Engineer", "Machine Learning")
        location (str, optional): Location preference for the job search
        experience_level (str, optional): Experience level (e.g., "entry", "mid", "senior")
    
    Returns:
        Dict[str, Any]: Extracted job data from multiple job websites
    """
    
    # Get API key from environment variable
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        return {"error": "FIRECRAWL_API_KEY not found in environment variables"}
    
    # Initialize Firecrawl
    firecrawl = Firecrawl(api_key=api_key)
    
    # Major job websites to search
    job_websites = [
        "https://www.indeed.com/*",
        "https://www.glassdoor.com/Jobs/*",
        "https://www.linkedin.com/jobs/*",
    ]
    
    # Create search prompt
    search_context = f"job title: {job_query}"
    if location:
        search_context += f", location: {location}"
    if experience_level:
        search_context += f", experience level: {experience_level}"
    
    prompt = f"""
    Extract job listings related to {search_context}. 
    For each job found, extract:
    - Job title
    - Company name
    - Location (if available)
    - Salary range (if available)
    - Job description summary
    - Required skills and qualifications
    - Experience level required
    - Application URL or link
    - Date posted (if available)
    
    Focus on relevant, recent job postings that match the search criteria.
    """
    
    # Define schema for structured data extraction
    schema = {
        "type": "object",
        "properties": {
            "jobs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "company": {"type": "string"},
                        "location": {"type": "string"},
                        "salary_range": {"type": "string"},
                        "description_summary": {"type": "string"},
                        "required_skills": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "type" : { "type": "string"},
                        "experience_level": {"type": "string"},
                        "application_url": {"type": "string"},
                        "date_posted": {"type": "string"}
                    },
                    "required": ["title", "company"]
                }
            },
            "search_summary": {
                "type": "object",
                "properties": {
                    "total_jobs_found": {"type": "number"},
                    "search_query": {"type": "string"},
                    "websites_searched": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        },
        "required": ["jobs", "search_summary"]
    }
    
    try:
        # Perform extraction with web search enabled for broader coverage
        result = firecrawl.extract(
            urls=job_websites,
            prompt=prompt,
            schema=schema,
            enable_web_search=True
        )
        
        if result.success:
            return result.data
        else:
            return {"error": "Failed to extract job data", "details": result}
            
    except Exception as e:
        return {"error": f"An error occurred during job search: {str(e)}"}

@function_tool
def get_job_details_from_url(job_url: str) -> Dict[str, Any]:
    """
    Extract detailed information from a specific job posting URL.
    
    Args:
        job_url (str): URL of the specific job posting
        
    Returns:
        Dict[str, Any]: Detailed job information
    """
    
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        return {"error": "FIRECRAWL_API_KEY not found in environment variables"}
    
    firecrawl = Firecrawl(api_key=api_key)
    
    prompt = """
    Extract comprehensive details from this job posting:
    - Complete job title
    - Company name and description
    - Full job description
    - Detailed requirements and qualifications
    - Benefits and perks
    - Salary information
    - Location details (remote/hybrid/onsite)
    - Application process
    - Company culture information
    - Team size and structure (if available)
    """
    
    schema = {
        "type": "object",
        "properties": {
            "job_title": {"type": "string"},
            "company_name": {"type": "string"},
            "company_description": {"type": "string"},
            "full_description": {"type": "string"},
            "requirements": {
                "type": "array",
                "items": {"type": "string"}
            },
            "benefits": {
                "type": "array", 
                "items": {"type": "string"}
            },
            "salary_info": {"type": "string"},
            "location_details": {"type": "string"},
            "application_process": {"type": "string"},
            "company_culture": {"type": "string"},
            "team_info": {"type": "string"}
        },
        "required": ["job_title", "company_name", "full_description"]
    }
    
    try:
        result = firecrawl.extract(
            urls=[job_url],
            prompt=prompt,
            schema=schema
        )
        
        if result.success:
            return result.data
        else:
            return {"error": "Failed to extract job details", "details": result}
            
    except Exception as e:
        return {"error": f"An error occurred while extracting job details: {str(e)}"}
