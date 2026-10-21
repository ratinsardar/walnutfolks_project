# Transaction Webhook Service

A Django service that receives transaction webhooks from external payment processors, acknowledges them immediately, and processes transactions in the background.

## Live Application

Base URL:

https://walnutfolks-project-1.onrender.com

Browser pages:

- Trigger webhook: https://walnutfolks-project-1.onrender.com/trigger
- Health check: https://walnutfolks-project-1.onrender.com/health
- Transaction status: https://walnutfolks-project-1.onrender.com/status

## How to Test

### Health check

Open:

https://walnutfolks-project-1.onrender.com/health

Click `Check health`. The response should contain:

```json
{
  "status": "HEALTHY",
  "current_time": "..."
}
```

### Trigger a transaction

Open:

https://walnutfolks-project-1.onrender.com/trigger

Enter a unique transaction ID, such as:

```text
txn_company_test_001
```

Enter the account details, amount, and currency, then click `Trigger Webhook`.

The response should show:

```text
HTTP 202
```

The transaction is processed in the background with a 30-second delay.

### Check transaction status

Open:

https://walnutfolks-project-1.onrender.com/status

Enter the same transaction ID. The status should initially be `PROCESSING` and should become `PROCESSED` after approximately 30 seconds.

The response also includes `created_at` and `processed_at` timestamps.

## API Endpoints

### Health check

```http
GET /
```

Example:

```text
https://walnutfolks-project-1.onrender.com/
```

### Receive transaction webhook

```http
POST /v1/webhooks/transactions
Content-Type: application/json
```

Request body:

```json
{
  "transaction_id": "txn_abc123def456",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500,
  "currency": "INR"
}
```

Expected response status: `202 Accepted`.

### Get transaction status

```http
GET /v1/transactions/{transaction_id}
```

Example:

```text
https://walnutfolks-project-1.onrender.com/v1/transactions/txn_abc123def456
```

Example response:

```json
[
  {
    "transaction_id": "txn_abc123def456",
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 1500.0,
    "currency": "INR",
    "status": "PROCESSED",
    "created_at": "2026-10-21T10:00:00Z",
    "processed_at": "2026-10-21T10:00:30Z"
  }
]
```

## Duplicate Webhook Test

Send the same webhook more than once using the same `transaction_id`. Each request is acknowledged, but only one transaction record is created and processed. The unique transaction ID prevents duplicate processing.

## Run Locally

Create a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies and create the database:

```bash
pip install -r requirements.txt
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

Local pages:

```text
http://127.0.0.1:8000/trigger
http://127.0.0.1:8000/health
http://127.0.0.1:8000/status
```

Run the tests:

```bash
python manage.py test
```

## Technical Choices

Django was selected because it provides a clear structure for building APIs, validating requests, managing database models, and serving browser pages.

SQLite stores transaction details, statuses, and timestamps without requiring additional database setup during development.

A background worker processes transactions separately from the webhook request. This allows the webhook endpoint to return `202 Accepted` quickly while the simulated 30-second processing delay runs in the background.

The `transaction_id` field is unique, which prevents duplicate webhook requests from creating or processing the same transaction more than once.

Docker packages the application and its dependencies for deployment on Render. Uvicorn runs the Django application as an ASGI service.

## Project Structure

```text
assign-20-10/
├── app/
│   ├── migrations/
│   ├── apps.py
│   ├── asgi.py
│   ├── models.py
│   ├── serializers.py
│   ├── settings.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── worker.py
├── templates/
│   ├── health.html
│   ├── status.html
│   └── trigger.html
├── Dockerfile
├── manage.py
├── requirements.txt
└── README.md
```

