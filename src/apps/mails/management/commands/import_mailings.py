import openpyxl
from django.core.management.base import BaseCommand, CommandError

from src.apps.mails.services import process_mailing_row


class Command(BaseCommand):
    help = "Импорт рассылок из файла XLSX и последующая отправка писем"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к файлу формата XLSX")

    def handle(self, *args, **options):
        file_path = options["file_path"]

        try:
            workbook = openpyxl.load_workbook(file_path, read_only=True)
            sheet = workbook.active
        except Exception as e:
            raise CommandError(f"Failed to read file: {e}")

        stats = {"processed": 0, "created": 0, "skipped": 0, "error": 0}

        rows = sheet.iter_rows(values_only=True)
        try:
            headers = next(rows)
        except StopIteration:
            raise CommandError("Файл пуст")

        expected_headers = ["external_id", "user_id", "email", "subject", "message"]
        if not all(h in headers for h in expected_headers):
            raise CommandError(f"Некорректные заголовки. Ожидались: {expected_headers}")

        self.stdout.write(
            self.style.SUCCESS(f"Запуск импорта из файла: {file_path}...")
        )

        for row_values in rows:
            if not any(row_values):
                continue

            stats["processed"] += 1
            data = dict(zip(headers, row_values))

            result = process_mailing_row(data)

            if result in stats:
                stats[result] += 1
            else:
                stats["error"] += 1

        self.stdout.write(self.style.SUCCESS("ОБРАБОТКА ЗАВЕРШЕНА"))
        self.stdout.write(f"Общее количество строк в файле: {stats['processed']}")
        self.stdout.write(
            self.style.SUCCESS(f"Количество созданных записей:  {stats['created']}")
        )
        self.stdout.write(
            self.style.WARNING(f"Количество пропущенных записей: {stats['skipped']}")
        )
        self.stdout.write(
            self.style.ERROR(f"Количество ошибочных строк: {stats['error']}")
        )
