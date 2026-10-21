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

```json
{
  "status": "HEALTHY",
  "current_time": "..."
}
