"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Loader2, Search, MapPin, Briefcase, Clock } from "lucide-react"

interface Job {
  id: string
  title: string
  company: string
  location: string
  experienceLevel: string
  salary: string
  description: string
  postedDate: string
  type: string
  applyUrl?: string,
  skills?: string[]
  experience_level?: string
  source?: string
}

interface JobSearchResult {
  title: string
  company: string
  location: string
  salary_range?: string
  skills?: string[]
  application_url?: string
  description?: string
  date_posted?: string
  experience_level?: string
  source?: string
  type?: string
}

interface APIResponse {
  success: boolean
  message: string
  data?: {
    agent_response: JobSearchResult[]
    search_query: string
    location: string
    experience_level: string
  }
  error?: string
}

export default function JobGPTApp() {
  const [jobTitle, setJobTitle] = useState("")
  const [location, setLocation] = useState("")
  const [experienceLevel, setExperienceLevel] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [jobs, setJobs] = useState<Job[]>([])
  const [hasSearched, setHasSearched] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [rawAgentResponse, setRawAgentResponse] = useState<string>("")

  // Function to convert JobSearchResult array to Job objects for UI
  const convertToUIJobs = (jobResults: JobSearchResult[]): Job[] => {
    return jobResults.map((job, index) => ({
      id: `job-${index + 1}`,
      title: job.title || "Job Position",
      company: job.company || "Company Name",
      location: job.location || "Location not specified",
      experienceLevel: job.experience_level || "Not specified",
      salary: job.salary_range || "Salary not specified",
      description: job.description || "Description not available",
      postedDate: job.date_posted || "Date not available",
      type: job.type || "Not specified",
      applyUrl: job.application_url,
      source: job.source || "Not specified",
      skills: job.skills || []
    }))
  }

  const handleSearch = async () => {
    if (!jobTitle.trim()) return

    setIsLoading(true)
    setHasSearched(true)
    setError(null)
    setJobs([])
    setRawAgentResponse("")

    try {
      const response = await fetch('http://localhost:8000/search-jobs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: jobTitle.trim(),
          location: location.trim(),
          experience_level: experienceLevel
        })
      })

      const data: APIResponse = await response.json()

      if (data.success && data.data && Array.isArray(data.data.agent_response)) {
        setRawAgentResponse(JSON.stringify(data.data.agent_response, null, 2))
        const uiJobs = convertToUIJobs(data.data.agent_response)
        setJobs(uiJobs)
      } else {
        setError(data.error || 'Failed to search for jobs')
      }
    } catch (err) {
      console.error('Search error:', err)
      setError('Failed to connect to the server. Make sure the backend is running on http://localhost:8000')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-center">
            <h1 className="text-4xl font-bold text-primary font-[family-name:var(--font-space-grotesk)]">JobGPT</h1>
          </div>
          <p className="text-center text-muted-foreground mt-2 font-[family-name:var(--font-dm-sans)]">
            AI-powered job search made simple
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12 max-w-4xl">
        {/* Search Form */}
        <Card className="mb-8 shadow-lg border-0 bg-card/80 backdrop-blur-sm">
          <CardHeader className="text-center pb-6">
            <CardTitle className="text-2xl font-[family-name:var(--font-space-grotesk)]">
              Find Your Perfect Job
            </CardTitle>
            <CardDescription className="text-lg font-[family-name:var(--font-dm-sans)]">
              Enter your preferences and let AI find the best opportunities for you
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <label
                  htmlFor="job-title"
                  className="text-sm font-medium text-foreground font-[family-name:var(--font-dm-sans)]"
                >
                  Job Title
                </label>
                <div className="relative">
                  <Briefcase className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                  <Input
                    id="job-title"
                    placeholder="e.g. Software Engineer"
                    value={jobTitle}
                    onChange={(e) => setJobTitle(e.target.value)}
                    className="pl-10 h-12 border-border focus:ring-primary"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label
                  htmlFor="location"
                  className="text-sm font-medium text-foreground font-[family-name:var(--font-dm-sans)]"
                >
                  Location
                </label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                  <Input
                    id="location"
                    placeholder="e.g. San Francisco, CA"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="pl-10 h-12 border-border focus:ring-primary"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label
                  htmlFor="experience"
                  className="text-sm font-medium text-foreground font-[family-name:var(--font-dm-sans)]"
                >
                  Experience Level
                </label>
                <Select value={experienceLevel} onValueChange={setExperienceLevel}>
                  <SelectTrigger className="h-12 border-border focus:ring-primary">
                    <SelectValue placeholder="Select level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="entry">Entry Level</SelectItem>
                    <SelectItem value="mid">Mid Level</SelectItem>
                    <SelectItem value="senior">Senior Level</SelectItem>
                    <SelectItem value="lead">Lead/Principal</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="flex justify-center pt-4">
              <Button
                onClick={handleSearch}
                disabled={isLoading || !jobTitle.trim()}
                className="px-8 py-3 h-12 text-lg font-medium bg-primary hover:bg-primary/90 text-primary-foreground font-[family-name:var(--font-dm-sans)]"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Searching...
                  </>
                ) : (
                  <>
                    <Search className="mr-2 h-5 w-5" />
                    Search Jobs
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Error State */}
        {error && (
          <Card className="border-destructive/50 bg-destructive/5">
            <CardContent className="p-6">
              <div className="flex items-center gap-3 text-destructive">
                <div className="rounded-full bg-destructive/10 p-2">
                  <Search className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="font-semibold">Search Failed</h3>
                  <p className="text-sm text-muted-foreground">{error}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="flex flex-col items-center justify-center py-16">
            <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
            <p className="text-lg text-muted-foreground font-[family-name:var(--font-dm-sans)]">
              Finding the best jobs for you...
            </p>
          </div>
        )}

        {/* Results */}
        {!isLoading && !error && hasSearched && jobs.length > 0 && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-foreground font-[family-name:var(--font-space-grotesk)]">
                Found {jobs.length} Jobs
              </h2>
            </div>

            <div className="grid gap-6">
              {jobs.map((job) => (
                <Card key={job.id} className="hover:shadow-lg transition-shadow duration-200 border-border bg-card">
                  <CardContent className="p-6">
                    <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                      <div className="flex-1 space-y-3">
                        <div>
                          <h3 className="text-xl font-bold text-foreground font-[family-name:var(--font-space-grotesk)] mb-1">
                            {job.title}
                          </h3>
                          <p className="text-lg text-primary font-medium font-[family-name:var(--font-dm-sans)]">
                            {job.company}
                          </p>
                        </div>

                        <div className="flex flex-wrap gap-4 text-sm text-muted-foreground font-[family-name:var(--font-dm-sans)]">
                          <div className="flex items-center gap-1">
                            <MapPin className="h-4 w-4" />
                            {job.location}
                          </div>
                          <div className="flex items-center gap-1">
                            <Briefcase className="h-4 w-4" />
                            {job.experienceLevel}
                          </div>
                          <div className="flex items-center gap-1">
                            <Clock className="h-4 w-4" />
                            {job.postedDate}
                          </div>
                          {job.source && (
                            <div className="flex items-center gap-1">
                              <span className="text-xs">Source: </span>
                              {job.source}
                            </div>
                          )}
                        </div>

                        <p className="text-foreground font-[family-name:var(--font-dm-sans)] leading-relaxed">
                          {job.description}
                        </p>

                        {job.skills && job.skills.length > 0 && (
                          <div className="space-y-2">
                            <p className="text-sm font-medium text-muted-foreground">Required Skills:</p>
                            <div className="flex flex-wrap gap-2">
                              {job.skills.map((skill, index) => (
                                <Badge key={index} variant="outline" className="text-xs">
                                  {skill}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        )}

                        <div className="flex items-center gap-3">
                          <Badge variant="secondary" className="bg-accent/10 text-accent hover:bg-accent/20">
                            {job.type}
                          </Badge>
                          <span className="text-lg font-semibold text-primary font-[family-name:var(--font-dm-sans)]">
                            {job.salary}
                          </span>
                        </div>
                      </div>

                      <div className="flex flex-col gap-2 md:ml-6">
                        {job.applyUrl ? (
                          <Button 
                            asChild 
                            className="bg-primary hover:bg-primary/90 text-primary-foreground font-[family-name:var(--font-dm-sans)]"
                          >
                            <a href={job.applyUrl} target="_blank" rel="noopener noreferrer">
                              Apply Now
                            </a>
                          </Button>
                        ) : (
                          <Button 
                            disabled 
                            className="bg-primary hover:bg-primary/90 text-primary-foreground font-[family-name:var(--font-dm-sans)]"
                          >
                            Apply Now
                          </Button>
                        )}
                        <Button
                          variant="outline"
                          className="border-border hover:bg-accent/10 font-[family-name:var(--font-dm-sans)] bg-transparent"
                        >
                          Save Job
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* No Results */}
        {!isLoading && !error && hasSearched && jobs.length === 0 && (
          <div className="text-center py-16">
            <div className="mb-4">
              <Search className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
            </div>
            <h3 className="text-xl font-semibold text-foreground mb-2 font-[family-name:var(--font-space-grotesk)]">
              No jobs found
            </h3>
            <p className="text-muted-foreground font-[family-name:var(--font-dm-sans)]">
              Try adjusting your search criteria or check back later for new opportunities.
            </p>
          </div>
        )}
      </main>
    </div>
  )
}
