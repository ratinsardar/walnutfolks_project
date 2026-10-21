# Transaction Webhook Service

Django service that acknowledges payment webhooks immediately and processes transactions in the background.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open the transaction trigger page at `http://127.0.0.1:8000/trigger`.

## API endpoints

- `GET /` returns the health status.
- `POST /v1/webhooks/transactions` accepts a transaction and returns `202 Accepted`.
- `GET /v1/transactions/{transaction_id}` returns the transaction status.
- `GET /trigger` provides a browser page for submitting test transactions.
- `GET /health` provides a browser page for checking the health endpoint.
- `GET /status` provides a browser page for checking a transaction status.

Example request:

```json
{
  "transaction_id": "txn_abc123def456",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500,
  "currency": "INR"
}
```

The worker stores the transaction in SQLite, waits 30 seconds to simulate an external payment processor, and changes the status to `PROCESSED`. The unique transaction ID prevents duplicate processing.

## Test

```bash
python manage.py test
```

## Docker

```bash
docker build -t transaction-webhook-service .
docker run -p 8000:8000 transaction-webhook-service
```

Mount persistent storage for `transactions.db` when deploying. The included Dockerfile runs the Django ASGI application with Uvicorn.

