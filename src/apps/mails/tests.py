import pytest
from django.core.management import CommandError, call_command

from src.apps.mails.models import Mailing, MailingStatKey, ParseStatKey

pytestmark = pytest.mark.django_db


def test_run_mailing_command(mocker, capsys):
    """Проверка запуска рассылки через мок сервис"""
    mock_send = mocker.patch(
        "src.apps.mails.services.MailingService.send_pending_mails"
    )
    mock_send.return_value = {MailingStatKey.SENT: 5, MailingStatKey.FAILED: 1}

    call_command("run_mailing")

    captured = capsys.readouterr()

    assert f"{MailingStatKey.SENT.value}: 5" in captured.out
    assert f"{MailingStatKey.FAILED.value}: 1" in captured.out
    mock_send.assert_called_once()


def test_import_xlsx_file_not_found():
    """Ошибка при отсутствии файла"""
    with pytest.raises(CommandError) as excinfo:
        call_command("import_xlsx", "non_existent.xlsx")
    assert "не найден" in str(excinfo.value)


def test_import_xlsx_success(mocker, capsys):
    """Успешный импорт с моками"""
    mocker.patch("os.path.exists", return_value=True)
    mock_import = mocker.patch(
        "src.apps.mails.services.XLSXParserService.import_from_xlsx"
    )
    mock_import.return_value = {
        ParseStatKey.PROCESSED: 10,
        ParseStatKey.CREATED: 8,
        ParseStatKey.SKIPPED: 2,
        ParseStatKey.ERRORS: 0,
    }

    call_command("import_xlsx", "dummy.xlsx")

    captured = capsys.readouterr()
    assert f"{ParseStatKey.PROCESSED.value}: 10" in captured.out
    assert f"{ParseStatKey.CREATED.value}: 8" in captured.out
    mock_import.assert_called_once_with("dummy.xlsx")


def test_run_mailing_integration(mocker, capsys):
    """Проверка работы команды с реальной базой данных"""
    mocker.patch("time.sleep", return_value=None)
    mocker.patch("random.random", return_value=1.0)

    Mailing.objects.create(
        external_id="pytest_1",
        email="pytest@example.com",
        status=Mailing.Status.PENDING,
    )

    call_command("run_mailing")

    mailing = Mailing.objects.get(external_id="pytest_1")
    assert mailing.status == Mailing.Status.SENT

    captured = capsys.readouterr()
    assert f"{MailingStatKey.SENT.value}: 1" in captured.out
