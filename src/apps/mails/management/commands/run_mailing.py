from django.core.management.base import BaseCommand

from src.apps.mails.services import MailingService


class Command(BaseCommand):
    help = "Запускает процесс эмуляции рассылки писем из базы данных"

    def handle(self, *args, **options):

        service = MailingService()

        stats = service.send_pending_mails()

        for key, value in stats.items():
            label = key.value if hasattr(key, "value") else key
            self.stdout.write(f"{label}: {value}")
