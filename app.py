from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
import asyncio
import logging
from email_utils import EmailProcessor, is_valid_email
from factory.scraper_factory import ScraperFactory
from config import logger, SUPPORTED_SITES

# Initialize FastAPI app
app = FastAPI(
    title="Newsletter Subscription API",
    description="API for subscribing emails to various news websites",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processor
email_processor = EmailProcessor()
scraper_factory = ScraperFactory()

# Store task results (in production, use Redis or database)
task_results = {}


# Request/Response Models
class SubscribeRequest(BaseModel):
    url: str = Field(..., description="Website URL to subscribe to")
    emails: List[EmailStr] = Field(..., description="List of email addresses to subscribe")
    headless: bool = Field(default=True, description="Run browser in headless mode")
    
    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("URL must be a non-empty string")
        if not scraper_factory.is_supported_url(v):
            supported = scraper_factory.get_supported_sites_list()
            raise ValueError(f"Unsupported website URL. Supported sites: {supported}")
        return v
    
    @field_validator('emails')
    @classmethod
    def validate_emails(cls, v):
        if not v or len(v) == 0:
            raise ValueError("At least one email address is required")
        for email in v:
            if not is_valid_email(str(email)):
                raise ValueError(f"Invalid email address: {email}")
        return v


class SubscribeResponse(BaseModel):
    task_id: str
    message: str
    status: str
    url: str
    total_emails: int


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    total: int
    success: int
    failed: int
    errors: List[str]
    url: str


class SitesResponse(BaseModel):
    supported_sites: List[str]
    site_details: dict


class HealthResponse(BaseModel):
    status: str
    message: str


# Background task to process emails
async def process_subscription_task(task_id: str, url: str, emails: List[str], headless: bool):
    """Process email subscriptions in the background"""
    try:
        results = await email_processor.process_emails(url, emails, headless=headless)
        task_results[task_id] = {
            "status": "completed",
            **results,
            "url": url
        }
    except Exception as e:
        task_results[task_id] = {
            "status": "failed",
            "total": len(emails),
            "success": 0,
            "failed": len(emails),
            "errors": [str(e)],
            "url": url
        }


# API Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - API information"""
    return {
        "status": "healthy",
        "message": "Newsletter Subscription API is running"
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is operational"
    }

# Get list of all supported news websites
@app.get("/sites", response_model=SitesResponse)
async def get_supported_sites():
    """Get list of all supported news websites"""
    sites_list = list(SUPPORTED_SITES.keys())
    return {
        "supported_sites": sites_list,
        "site_details": SUPPORTED_SITES
    }

# Subscribe to a newsletter
@app.post("/subscribe", response_model=SubscribeResponse, status_code=202)
async def subscribe(
    request: SubscribeRequest,
    background_tasks: BackgroundTasks
):

    # Generate task ID
    import uuid
    task_id = str(uuid.uuid4())
    
    # Convert EmailStr to string for processing
    emails_list = [str(email) for email in request.emails]
    
    # Add background task
    background_tasks.add_task(
        process_subscription_task,
        task_id,
        request.url,
        emails_list,
        request.headless
    )
    
    # Initialize task status
    task_results[task_id] = {
        "status": "processing",
        "total": len(emails_list),
        "success": 0,
        "failed": 0,
        "errors": [],
        "url": request.url
    }
    
    logger.info(f"Created subscription task {task_id} for {len(emails_list)} email(s) at {request.url}")
    
    return {
        "task_id": task_id,
        "message": f"Subscription task created for {len(emails_list)} email(s)",
        "status": "processing",
        "url": request.url,
        "total_emails": len(emails_list)
    }

# Get subscription status

@app.get("/subscribe/{task_id}", response_model=TaskStatusResponse)
async def get_subscription_status(task_id: str):
   # Get subscription status
    if task_id not in task_results:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    result = task_results[task_id]
    return {
        "task_id": task_id,
        "status": result["status"],
        "total": result["total"],
        "success": result["success"],
        "failed": result["failed"],
        "errors": result.get("errors", []),
        "url": result.get("url", "")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

