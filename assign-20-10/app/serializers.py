from django.core.exceptions import ValidationError


def parse_transaction_payload(payload):
    required = [
        "transaction_id",
        "source_account",
        "destination_account",
        "amount",
        "currency",
    ]
    missing = [field for field in required if field not in payload]
    if missing:
        raise ValidationError(f"Missing fields: {', '.join(missing)}")
    if (
        not payload["transaction_id"]
        or not payload["source_account"]
        or not payload["destination_account"]
    ):
        raise ValidationError("Account and transaction identifiers cannot be empty")
    try:
        amount = float(payload["amount"])
    except (TypeError, ValueError):
        raise ValidationError("Amount must be a number")
    if amount <= 0:
        raise ValidationError("Amount must be greater than zero")
    currency = str(payload["currency"]).upper()
    if len(currency) != 3:
        raise ValidationError("Currency must contain three characters")
    return {
        "transaction_id": str(payload["transaction_id"]),
        "source_account": str(payload["source_account"]),
        "destination_account": str(payload["destination_account"]),
        "amount": amount,
        "currency": currency,
    }

