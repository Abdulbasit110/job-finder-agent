# 🤖 JobGPT - AI-Powered Job Search Agent

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-15.2.4-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://www.typescriptlang.org/)

> An intelligent job search application that uses AI agents and web scraping to find relevant job opportunities across major job boards.

## 🌟 Features

- **🤖 AI-Powered Search**: Uses OpenAI agents to understand job requirements and search intelligently
- **🌐 Multi-Platform Scraping**: Searches across Indeed, Glassdoor, and other major job boards using Firecrawl
- **⚡ Real-Time Results**: Fast API responses with structured job data
- **🎨 Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS
- **🔍 Smart Filtering**: Filter by location, experience level, and job type
- **📱 Mobile-Friendly**: Fully responsive design that works on all devices
- **🚀 Easy Deployment**: Simple setup with clear instructions

## 🏗️ Architecture

```
JobGPT/
├── 🐍 Backend (Python FastAPI)
│   ├── api.py              # FastAPI server and endpoints
│   ├── agent.py            # AI agent configuration
│   ├── tools.py            # Firecrawl job search tools
│   ├── hooks.py            # Agent execution hooks
│   └── run_server.py       # Server startup script
└── 🌐 Frontend (Next.js)
    └── jobgpt/
        ├── app/
        │   └── page.tsx    # Main job search interface
        └── components/     # UI components (shadcn/ui)
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **OpenAI API Key**
- **Firecrawl API Key**

### 1. Clone the Repository

```bash
git clone <repository-url>
cd job-finder-agent
```

### 2. Backend Setup

```bash
# Install Python dependencies using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Optional Configuration
PYTHONPATH=.
```

#### 🔑 Getting API Keys

**OpenAI API Key:**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Go to API Keys section
4. Generate a new API key

**Firecrawl API Key:**
1. Visit [Firecrawl.dev](https://firecrawl.dev/)
2. Sign up for an account
3. Navigate to your dashboard
4. Copy your API key

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd jobgpt

# Install dependencies
npm install

# Or using pnpm (recommended)
pnpm install
```

### 5. Start the Application

**Terminal 1 - Backend:**
```bash
# From project root
python run_server.py
```

**Terminal 2 - Frontend:**
```bash
# From jobgpt directory
npm run dev
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Usage Guide

### Web Interface

1. **Open your browser** to http://localhost:3000
2. **Enter job criteria**:
   - Job Title (required): e.g., "Python Developer", "AI Engineer"
   - Location (optional): e.g., "San Francisco", "Remote"
   - Experience Level (optional): Entry, Mid, Senior, Lead
3. **Click "Search Jobs"**
4. **View results** with detailed job information including:
   - Company name and job title
   - Location and salary information
   - Required skills as badges
   - Job source (Indeed, Glassdoor, etc.)
   - Direct apply links

### API Usage

You can also use the API directly:

```bash
# Health check
curl http://localhost:8000/health

# Search for jobs
curl -X POST "http://localhost:8000/search-jobs" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Software Engineer",
       "location": "New York",
       "experience_level": "mid"
     }'
```

### Command Line Usage

For direct agent interaction:

```bash
python main.py
```

## 🔧 API Reference

### Endpoints

#### `POST /search-jobs`
Search for jobs using the AI agent.

**Request Body:**
```json
{
  "query": "string (required)",
  "location": "string (optional)",
  "experience_level": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Job search completed successfully",
  "data": {
    "agent_response": [
      {
        "title": "Software Engineer",
        "company": "TechCorp",
        "location": "San Francisco, CA",
        "salary_range": "$120,000 - $150,000",
        "skills": ["Python", "React", "SQL"],
        "application_url": "https://...",
        "description": "Job description...",
        "experience_level": "Mid",
        "source": "Indeed"
      }
    ],
    "search_query": "Software Engineer",
    "location": "San Francisco",
    "experience_level": "mid"
  }
}
```

#### `GET /health`
Health check endpoint.

#### `GET /agent-status`
Get agent status and available tools.

## 🛠️ Development

### Project Structure

```
job-finder-agent/
├── 📁 Backend Components
│   ├── agent.py           # AI agent with JobSearchResult schema
│   ├── api.py             # FastAPI server with CORS
│   ├── tools.py           # Firecrawl integration tools
│   ├── hooks.py           # Agent execution hooks
│   ├── main.py            # CLI interface
│   └── run_server.py      # Server startup
├── 📁 Frontend (jobgpt/)
│   ├── app/
│   │   ├── page.tsx       # Main search interface
│   │   ├── layout.tsx     # App layout
│   │   └── globals.css    # Global styles
│   ├── components/
│   │   └── ui/            # shadcn/ui components
│   └── lib/
│       └── utils.ts       # Utility functions
└── 📁 Configuration
    ├── pyproject.toml     # Python dependencies
    ├── package.json       # Node.js dependencies
    └── .env               # Environment variables
```

### Key Technologies

**Backend:**
- **FastAPI**: High-performance Python web framework
- **OpenAI Agents SDK**: AI agent framework
- **Firecrawl**: Web scraping service for job boards
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

**Frontend:**
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Modern UI component library
- **Lucide React**: Icon library

### Adding New Job Sources

To add new job boards to search:

1. **Update `tools.py`**:
   ```python
   job_websites = [
       "https://www.indeed.com/*",
       "https://www.glassdoor.com/Jobs/*",
       "https://jobs.lever.co/*",        # Add new source
       "https://your-new-site.com/*"    # Add another
   ]
   ```

2. **Test the integration**:
   ```bash
   python main.py
   ```

### Customizing the Agent

Modify `agent.py` to change agent behavior:

```python
def create_job_finder_agent():
    agent = Agent(
        name="Job Finder",
        instructions="""Your custom instructions here...""",
        tools=[search_jobs_with_firecrawl, get_job_details_from_url],
        output_type=List[JobSearchResult]
    )
    return agent
```

## 🚨 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python version
python --version  # Should be 3.12+

# Install dependencies
uv sync

# Check environment variables
python -c "import os; print(os.getenv('OPENAI_API_KEY', 'Not set'))"
```

**Frontend build errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+
```

**CORS errors:**
- Ensure backend is running on port 8000
- Frontend should run on port 3000
- CORS is configured for both in `api.py`

**API Key issues:**
- Verify API keys are valid
- Check `.env` file is in the root directory
- Restart the backend after adding keys

### Debug Mode

Run with debug logging:

```bash
# Backend with debug logs
python run_server.py --log-level debug

# Frontend with verbose output
npm run dev -- --verbose
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#🚨-troubleshooting) section
2. Review the [API Documentation](http://localhost:8000/docs) when running
3. Open an issue with detailed information about your problem

## 🎯 Roadmap

- [ ] Add more job board integrations
- [ ] Implement job filtering and sorting
- [ ] Add job application tracking
- [ ] Email notifications for new jobs
- [ ] User authentication and profiles
- [ ] Advanced search with Boolean operators
- [ ] Job recommendation engine
- [ ] Mobile app development

---

**Made with ❤️ using OpenAI Agents, Firecrawl, FastApi and Next.js By Abdul Basit**
