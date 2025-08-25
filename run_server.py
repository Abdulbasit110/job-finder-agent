#!/usr/bin/env python3
"""
Simple script to run the Job Finder Agent FastAPI server
"""

import uvicorn
from api import app

if __name__ == "__main__":
    print("🚀 Starting Job Finder Agent API Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation available at: http://localhost:8000/docs")
    print("🔍 Ready to search for jobs!")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )
