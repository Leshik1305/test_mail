from enum import Enum

from django.db import models

from src.core.models import TimeStampedModel


class ParseStatKey(Enum):
    PROCESSED = "Количество обработанных строк"
    CREATED = "Количество созданных записей"
    SKIPPED = "Количество пропущенных записей"
    ERRORS = "Количество ошибочных строк"


class MailingStatKey(Enum):
    SENT = "Успешно отправлено"
    FAILED = "Ошибок отправки"


class Mailing(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        ERROR = "error", "Error"

    external_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="ID",
    )
    user_id = models.CharField(
        max_length=255,
        verbose_name="ID пользователя",
    )
    email = models.EmailField(verbose_name="E-mail получателя")
    subject = models.CharField(
        max_length=255,
        verbose_name="Тема письма",
    )
    message = models.TextField(verbose_name="Текст письма")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Статус",
    )
    retry_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество попыток",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"{self.external_id} - {self.email}"
