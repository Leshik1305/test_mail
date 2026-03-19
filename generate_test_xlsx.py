import os

import openpyxl


def create_test_file(filename="import_data/data.xlsx"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Рассылки"

    headers = ["external_id", "user_id", "email", "subject", "message"]
    sheet.append(headers)

    data = [
        ["001", 1, "test1@example.com", "Первое", "Первое письмо."],
        ["002", 2, "test2@example.com", "Второе", "Второе письмо."],
        ["003", 2, "test2@example.com", "Третье", "Третье письмо."],
        ["004", 3, "test3@example.com", "Четвертое", "Четвертое письмо."],
        ["004", 3, "test3@example.com", "Четвертое", "Четвертое письмо."],
    ]

    for row in data:
        sheet.append(row)

    wb.save(filename)


if __name__ == "__main__":
    create_test_file()
