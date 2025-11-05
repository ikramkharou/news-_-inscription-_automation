# FastAPI REST API Documentation

This document provides comprehensive documentation for the Newsletter Subscription FastAPI REST API.


## Getting Started

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Start the API server:

**Option 1: Using uvicorn directly (Recommended)**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Option 2: Running app.py**
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to:
- View all available endpoints
- Test API calls directly from the browser
- See request/response schemas
- Understand expected parameters

## API Endpoints

### 1. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "message": "API is operational"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### 2. Get Supported Sites

Get a list of all supported news websites and their domain details.

**Endpoint:** `GET /sites`

**Response:**
```json
{
  "supported_sites": [
    "CNN",
    "Fox News",
    "The Atlantic",
    "The Verge",
    "Vox",
    "AP News",
    "National Review",
    "Axios",
    "PennLive",
    "The Guardian",
    "TechCrunch",
    "Quartz"
  ],
  "site_details": {
    "CNN": ["cnn.com", "edition.cnn.com"],
    "Fox News": ["foxnews.com", "fox.com"],
    "The Atlantic": ["theatlantic.com"],
    "The Verge": ["theverge.com"],
    "Vox": ["vox.com"],
    "AP News": ["apnews.com"],
    "National Review": ["nationalreview.com"],
    "Axios": ["axios.com"],
    "PennLive": ["pennlive.com"],
    "The Guardian": ["theguardian.com"],
    "TechCrunch": ["techcrunch.com"],
    "Quartz": ["qz.com"]
  }
}
```

**Example:**
```bash
curl http://localhost:8000/sites
```

---

### 3. Subscribe (Async - Background Processing)

Subscribe one or more email addresses to a news website newsletter. This endpoint returns immediately with a task ID, and processing happens in the background.

**Endpoint:** `POST /subscribe`

**Request Body:**
```json
{
  "url": "https://www.vox.com/newsletters",
  "emails": ["email1@example.com", "email2@example.com"],
  "headless": true
}
```

**Request Parameters:**
- `url` (string, required): The newsletter URL to subscribe to
- `emails` (array of strings, required): List of email addresses to subscribe
- `headless` (boolean, optional): Run browser in headless mode. Default: `true`

**Response:** (Status Code: 202 Accepted)
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Subscription task created for 2 email(s)",
  "status": "processing",
  "url": "https://www.vox.com/newsletters",
  "total_emails": 2
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.vox.com/newsletters",
    "emails": ["test@example.com"],
    "headless": true
  }'
```

**Note:** Use the returned `task_id` to check the subscription status using the `/subscribe/{task_id}` endpoint.

---

### 4. Check Subscription Status

Get the status of a subscription task that was created using the async `/subscribe` endpoint.

**Endpoint:** `GET /subscribe/{task_id}`

**Path Parameters:**
- `task_id` (string, required): The task ID returned from `/subscribe` endpoint

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "total": 2,
  "success": 2,
  "failed": 0,
  "errors": [],
  "url": "https://www.vox.com/newsletters"
}
```

**Status Values:**
- `processing`: Task is currently being processed
- `completed`: Task completed successfully
- `failed`: Task failed

**Response Fields:**
- `task_id`: The unique task identifier
- `status`: Current status of the task
- `total`: Total number of emails to process
- `success`: Number of successfully processed emails
- `failed`: Number of failed emails
- `errors`: Array of error messages (if any)
- `url`: The newsletter URL being processed

**Example:**
```bash
curl http://localhost:8000/subscribe/550e8400-e29b-41d4-a716-446655440000
```

**Error Response (404):**
```json
{
  "detail": "Task 550e8400-e29b-41d4-a716-446655440000 not found"
}
```

---

## Request/Response Models

### SubscribeRequest

Request model for subscription endpoints.

```json
{
  "url": "string",
  "emails": ["string"],
  "headless": true
}
```

**Validation:**
- `url`: Must be a supported website URL
- `emails`: Must contain at least one valid email address
- `headless`: Boolean (optional, default: `true`)

### SubscribeResponse

Response model for async subscription endpoint.

```json
{
  "task_id": "string",
  "message": "string",
  "status": "string",
  "url": "string",
  "total_emails": 0
}
```

### TaskStatusResponse

Response model for task status endpoint.

```json
{
  "task_id": "string",
  "status": "string",
  "total": 0,
  "success": 0,
  "failed": 0,
  "errors": ["string"],
  "url": "string"
}
```

### SitesResponse

Response model for supported sites endpoint.

```json
{
  "supported_sites": ["string"],
  "site_details": {
    "Site Name": ["domain.com"]
  }
}
```

---
