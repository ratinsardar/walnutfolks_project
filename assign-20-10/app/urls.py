from django.urls import path

from . import views


urlpatterns = [
    path("", views.health_check, name="health-check"),
    path("trigger", views.trigger_page, name="trigger-page"),
    path("health", views.health_page, name="health-page"),
    path("status", views.status_page, name="status-page"),
    path("v1/webhooks/transactions", views.receive_transaction_webhook, name="transaction-webhook"),
    path("v1/transactions/<str:transaction_id>", views.get_transaction, name="transaction-status"),
]

