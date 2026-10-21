import json
from datetime import datetime, timezone

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Transaction
from .serializers import parse_transaction_payload


def health_check(_request):
    return JsonResponse(
        {
            "status": "HEALTHY",
            "current_time": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }
    )


@csrf_exempt
def receive_transaction_webhook(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    try:
        transaction_data = parse_transaction_payload(json.loads(request.body))
    except (json.JSONDecodeError, ValidationError) as error:
        return JsonResponse({"detail": str(error)}, status=400)
    Transaction.objects.get_or_create(
        transaction_id=transaction_data["transaction_id"],
        defaults={**transaction_data, "status": "PROCESSING"},
    )
    return JsonResponse(
        {
            "status": "ACCEPTED",
            "transaction_id": transaction_data["transaction_id"],
        },
        status=202,
    )


def transaction_data(transaction):
    return {
        "transaction_id": transaction.transaction_id,
        "source_account": transaction.source_account,
        "destination_account": transaction.destination_account,
        "amount": float(transaction.amount),
        "currency": transaction.currency,
        "status": transaction.status,
        "created_at": transaction.created_at.isoformat().replace("+00:00", "Z"),
        "processed_at": (
            transaction.processed_at.isoformat().replace("+00:00", "Z")
            if transaction.processed_at
            else None
        ),
    }


def get_transaction(request, transaction_id):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        return JsonResponse({"detail": "Transaction not found"}, status=404)
    return JsonResponse([transaction_data(transaction)], safe=False)


def trigger_page(request):
    return render(request, "trigger.html")


def health_page(request):
    return render(request, "health.html")


def status_page(request):
    return render(request, "status.html")

