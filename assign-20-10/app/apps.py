import sys

from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        management_commands = {"check", "makemigrations", "migrate", "test"}
        if management_commands.intersection(sys.argv):
            return

        from .worker import start_worker

        start_worker()

