from django.db import models

from src.core.models import TimeStampedModel


class Mailing(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        ERROR = "error", "Error"

    external_id = models.CharField(
        max_length=255, unique=True, db_index=True, verbose_name="ID"
    )
    user_id = models.CharField(max_length=255, verbose_name="ID пользователя")
    email = models.EmailField(verbose_name="E-mail получателя")
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Текст письма")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Статус",
    )

    def __str__(self):
        return f"{self.external_id} - {self.email}"
