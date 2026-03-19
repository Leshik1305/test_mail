import time
from random import randint

from django.db import transaction

from .models import Mailing


def send_email(mailing: Mailing):
    """Эмуляция отправки письма с задержкой."""
    time.sleep(randint(5, 20))
    print(f"Send EMAIL to {mailing.email}")


def process_mailing_row(data: dict) -> str:
    """Обрабатывает одну строку данных."""
    external_id = str(data.get("external_id"))

    mailing = Mailing.objects.filter(external_id=external_id).first()

    if mailing and mailing.status == Mailing.Status.SENT:
        return "skipped"

    if not mailing:
        try:
            with transaction.atomic():
                mailing = Mailing.objects.create(
                    external_id=external_id,
                    user_id=data.get("user_id"),
                    email=data.get("email"),
                    subject=data.get("subject"),
                    message=data.get("message"),
                )
        except Exception as e:
            print(f"Ошибка при создании {external_id}: {e}")
            return "error"

    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            send_email(mailing)
            mailing.status = Mailing.Status.SENT
            mailing.save(update_fields=["status", "updated_at"])
            return "created"

        except Exception as e:
            print(f"Попытка отправки {attempt + 1} {external_id} провалена: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))
            else:
                mailing.status = Mailing.Status.ERROR
                mailing.save(update_fields=["status", "updated_at"])
                return "error"
