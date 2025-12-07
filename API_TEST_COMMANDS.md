# API Test Commands

This document contains curl commands (and PowerShell equivalents) to test the Newsletter Subscription API.

## Server

The API runs on `http://localhost:8000` by default.

## Endpoints

### 1. Health Check

**PowerShell:**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health -Method GET | Select-Object -ExpandProperty Content
```

**curl (if available):**
```bash
curl -X GET http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "API is operational"
}
```

### 2. Root Endpoint

**PowerShell:**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/ -Method GET | Select-Object -ExpandProperty Content
```

**curl:**
```bash
curl -X GET http://localhost:8000/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Newsletter Subscription API is running"
}
```

### 3. Get Supported Sites



**curl:**
```bash
curl -X GET http://localhost:8000/sites
```

**Expected Response:**
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
    ...
  }
}
```

### 4. Subscribe to Newsletter

**PowerShell:**
```powershell
$body = @{
    url = "https://www.vox.com/newsletters"
    emails = @("test@example.com")
    headless = $true
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8000/subscribe -Method POST -Body $body -ContentType "application/json" | Select-Object -ExpandProperty Content
```

**curl:**
```bash
curl -X POST http://localhost:8000/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.vox.com/newsletters",
    "emails": ["test@example.com"],
    "headless": true
  }'
```

**Expected Response:**
```json
{
  "task_id": "4fe5e200-fdb8-4613-a883-5db53aeb3cbf",
  "message": "Subscription task created for 1 email(s)",
  "status": "processing",
  "url": "https://www.vox.com/newsletters",
  "total_emails": 1
}
```

### 5. Check Subscription Status

**PowerShell:**
```powershell
$taskId = "YOUR_TASK_ID_HERE"
Invoke-WebRequest -Uri "http://localhost:8000/subscribe/$taskId" -Method GET | Select-Object -ExpandProperty Content
```

**curl:**
```bash
curl -X GET http://localhost:8000/subscribe/YOUR_TASK_ID_HERE
```

**Expected Response (Processing):**
```json
{
  "task_id": "4fe5e200-fdb8-4613-a883-5db53aeb3cbf",
  "status": "processing",
  "total": 1,
  "success": 0,
  "failed": 0,
  "errors": [],
  "url": "https://www.vox.com/newsletters"
}
```

**Expected Response (Completed):**
```json
{
  "task_id": "4fe5e200-fdb8-4613-a883-5db53aeb3cbf",
  "status": "completed",
  "total": 1,
  "success": 1,
  "failed": 0,
  "errors": [],
  "url": "https://www.vox.com/newsletters"
}
```

## Example: Complete Workflow

**PowerShell Script:**
```powershell
# 1. Check health
Invoke-WebRequest -Uri http://localhost:8000/health -Method GET | Select-Object -ExpandProperty Content

# 2. Get supported sites
Invoke-WebRequest -Uri http://localhost:8000/sites -Method GET | Select-Object -ExpandProperty Content

# 3. Subscribe
$body = @{
    url = "https://www.vox.com/newsletters"
    emails = @("test@example.com", "test2@example.com")
    headless = $true
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri http://localhost:8000/subscribe -Method POST -Body $body -ContentType "application/json"
$taskId = ($response.Content | ConvertFrom-Json).task_id
Write-Host "Task ID: $taskId"

# 4. Check status
Start-Sleep -Seconds 3
Invoke-WebRequest -Uri "http://localhost:8000/subscribe/$taskId" -Method GET | Select-Object -ExpandProperty Content
```

## Test Results

✅ **Health Check** - Working
✅ **Root Endpoint** - Working  
✅ **Get Supported Sites** - Working
✅ **Subscribe** - Working (Returns task ID)
✅ **Check Task Status** - Working

All endpoints are functional!

