import logging
import threading
import time
from datetime import datetime, timezone

from django.db import close_old_connections

from .models import Transaction


logger = logging.getLogger(__name__)
PROCESSING_DELAY_SECONDS = 30
worker_started = False
worker_lock = threading.Lock()


def start_worker():
    global worker_started
    with worker_lock:
        if worker_started:
            return
        worker_started = True
        threading.Thread(target=process_transactions, daemon=True).start()


def process_transactions():
    while True:
        close_old_connections()
        transaction = Transaction.objects.filter(status="PROCESSING").first()
        if transaction is None:
            transaction = Transaction.objects.filter(status="PENDING").first()
            if transaction:
                Transaction.objects.filter(
                    transaction_id=transaction.transaction_id,
                    status="PENDING",
                ).update(status="PROCESSING")
                transaction.refresh_from_db()
        if transaction:
            try:
                time.sleep(PROCESSING_DELAY_SECONDS)
                transaction.status = "PROCESSED"
                transaction.processed_at = datetime.now(timezone.utc)
                transaction.save(update_fields=["status", "processed_at"])
            except Exception:
                logger.exception("Transaction processing failed")
        else:
            time.sleep(0.25)

