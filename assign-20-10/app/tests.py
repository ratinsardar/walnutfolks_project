import json

from django.test import TestCase


class TransactionApiTests(TestCase):
    payload = {
        "transaction_id": "txn_test_123",
        "source_account": "acc_user_1",
        "destination_account": "acc_merchant_1",
        "amount": 1500,
        "currency": "INR",
    }

    def test_health_check(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "HEALTHY")

    def test_webhook_is_accepted_and_duplicate_is_ignored(self):
        first = self.client.post("/v1/webhooks/transactions", data=json.dumps(self.payload), content_type="application/json")
        duplicate = self.client.post("/v1/webhooks/transactions", data=json.dumps(self.payload), content_type="application/json")
        transaction = self.client.get("/v1/transactions/txn_test_123")
        self.assertEqual(first.status_code, 202)
        self.assertEqual(duplicate.status_code, 202)
        self.assertEqual(transaction.status_code, 200)
        self.assertEqual(len(transaction.json()), 1)
        self.assertEqual(transaction.json()[0]["status"], "PROCESSING")

    def test_trigger_page(self):
        response = self.client.get("/trigger")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Transaction Webhook Tester")

    def test_health_and_status_pages(self):
        health_page = self.client.get("/health")
        status_page = self.client.get("/status")
        self.assertEqual(health_page.status_code, 200)
        self.assertEqual(status_page.status_code, 200)
        self.assertContains(health_page, "Health Check")
        self.assertContains(status_page, "Transaction Status")

