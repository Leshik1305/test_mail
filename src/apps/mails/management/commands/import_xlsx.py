import os

from django.core.management.base import BaseCommand, CommandError

from src.apps.mails.models import ParseStatKey
from src.apps.mails.services import XLSXParserService


class Command(BaseCommand):
    help = "Импорт данных для рассылки из XLSX файла"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к .xlsx файлу")

    def handle(self, *args, **options):
        file_path = options["file_path"]

        if not os.path.exists(file_path):
            raise CommandError(f"Файл по пути '{file_path}' не найден.")

        parser_service = XLSXParserService()

        stats = parser_service.import_from_xlsx(file_path)

        for key in ParseStatKey:
            val = stats.get(key, 0)
            label = key.value if hasattr(key, "value") else key
            self.stdout.write(f"{label}: {val}")
