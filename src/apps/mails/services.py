import random
import time

import openpyxl
from django.db import transaction

from src.apps.mails.models import Mailing, MailingStatKey, ParseStatKey


class XLSXParserService:
    """Сервис парсингаю"""

    def __init__(self):
        self.stats = {key: 0 for key in ParseStatKey}

    def import_from_xlsx(self, file_path):
        try:
            workbook = openpyxl.load_workbook(file_path, read_only=True)
            sheet = workbook.active
        except Exception as e:
            raise ValueError(f"Не удалось прочитать файл: {e}")

        rows = sheet.iter_rows(values_only=True)

        try:
            headers = next(rows)
        except StopIteration:
            raise ValueError("Файл пуст")

        expected_headers = ["external_id", "user_id", "email", "subject", "message"]

        if list(headers[:5]) != expected_headers:
            raise ValueError(f"Некорректные заголовки.")

        try:
            for row in rows:
                self.stats[ParseStatKey.PROCESSED] += 1

                if not row or len(row) < 5 or not row[0] or not row[2]:
                    self.stats[ParseStatKey.ERRORS] += 1
                    continue

                ext_id, u_id, email, subject, message = row[:5]

                try:
                    obj, created = Mailing.objects.get_or_create(
                        external_id=str(ext_id),
                        defaults={
                            "user_id": str(u_id),
                            "email": email,
                            "subject": subject,
                            "message": message,
                        },
                    )

                    if created:
                        self.stats[ParseStatKey.CREATED] += 1
                    else:
                        self.stats[ParseStatKey.SKIPPED] += 1

                except Exception:
                    self.stats[ParseStatKey.ERRORS] += 1
        finally:
            workbook.close()

        return self.stats


class MailingService:
    """Сервис отправки с Retry и задержками"""

    MAX_RETRIES = 3

    def send_pending_mails(self):
        """Отправка писем с защитой от параллельного запуска, рандомной задержкой и системой повторных попыток."""

        stats = {
            MailingStatKey.SENT: 0,
            MailingStatKey.FAILED: 0,
        }

        print("Запуск рассылки...")
        while True:
            with transaction.atomic():
                mailing = (
                    Mailing.objects.select_for_update(skip_locked=True)
                    .filter(status=Mailing.Status.PENDING)
                    .order_by("updated_at")
                    .first()
                )

                if not mailing:
                    print("Нет писем для отправки.")
                    break

                time.sleep(random.randint(5, 20))
                # Эмуляция результата (90% успех, 10% ошибка)
                is_success = random.random() > 0.1

                if is_success:
                    mailing.status = Mailing.Status.SENT
                    stats[MailingStatKey.SENT] += 1
                    print(f"OK: Письмо на {mailing.email} успешно 'отправлено'.")

                else:
                    mailing.retry_count += 1
                    if mailing.retry_count >= self.MAX_RETRIES:
                        mailing.status = Mailing.Status.ERROR
                        stats[MailingStatKey.FAILED] += 1
                        print(
                            f"{mailing.email} переведен в ERROR после {mailing.retry_count} попыток."
                        )

                mailing.save()
        print(f"Рассылка завершена")
        return stats
