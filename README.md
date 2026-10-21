# Transaction Webhook Service

A Django service that receives payment transaction webhooks, acknowledges them immediately, and processes them in the background.

## Live Application

Base URL:

https://walnutfolks-project-1.onrender.com

Browser pages:

- Trigger webhook: https://walnutfolks-project-1.onrender.com/trigger
- Health check: https://walnutfolks-project-1.onrender.com/health
- Transaction status: https://walnutfolks-project-1.onrender.com/status

## How to Test

### 1. Check Health

Open:

https://walnutfolks-project-1.onrender.com/health

Click `Check health`.

Expected response:
{
  "status": "HEALTHY",
  "current_time": "..."
}
## Brief Explanation of Technical Choices

Django was selected because it provides a reliable structure for building APIs, handling requests, validating data, and working with databases.

SQLite was used as a simple persistent database for storing transaction details, statuses, and timestamps without requiring additional database setup during development.

A background worker processes transactions separately from the webhook request. This allows the webhook endpoint to return `202 Accepted` quickly while the 30-second processing delay happens in the background.

The `transaction_id` field is unique, which prevents duplicate webhooks from creating or processing the same transaction more than once.

Docker was used to package the application with its dependencies and make deployment easier on Render.

The application is deployed using Django with Uvicorn as the ASGI server.

```json
{
  "status": "HEALTHY",
  "current_time": "..."
}
