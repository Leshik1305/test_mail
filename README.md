 <b> JetLend Email Service (Test Task)</b>

Сервис на Django для парсинга данных из XLSX-файлов и эмуляции рассылки e-mail сообщений с поддержкой системы повторных попыток (Retry) и защиты от параллельного запуска.

<b> Стек технологий</b>
• <b>Python 3.12</b>
• <b>Django 5.x</b> + Django Rest Framework
• <b>PostgreSQL</b> (в качестве основной БД)
• <b>Poetry</b> (управление зависимостями)
• <b>Docker &amp; Docker Compose</b> (контейнеризация)
• <b>Pytest</b> (тестирование)

---

<b> Установка и запуск (через Docker)</b>

<b>1. Подготовка окружения</b>
Переименуйте файл настроек <code>.env.example</code> в <code>.env</code> и заполните переменные среды (настройки БД, секретные ключи):

<pre><code class="language-bash">cp .env.example .env</code></pre>

<b>2. Запуск проекта</b>
Запустите контейнеры приложения (автоматически применятся миграции и поднимется сервер):

<pre><code class="language-bash">docker-compose up --build</code></pre>

Сервис станет доступным по адресу: <b>&lt;a href=&quot;http://localhost:8000</b>">http://localhost:8000**</a>

---

<b> Локальная разработка (без Docker)</b>

Если у вас установлен менеджер зависимостей <b>Poetry</b>, выполните следующие шаги:

<b>1. Установка зависимостей</b>
<pre><code class="language-bash">poetry install</code></pre>

<b>2. Активация виртуального окружения</b>
<pre><code class="language-bash">poetry shell</code></pre>

<b>3. Выполнение миграций БД</b>
Убедитесь, что у вас запущена локальная база данных PostgreSQL, затем выполните:
<pre><code class="language-bash">python manage.py migrate</code></pre>

 <b>4. Запуск сервера разработки</b>
<pre><code class="language-bash">python manage.py runserver</code></pre>
Проект запустится по адресу: <b>&lt;a href=&quot;http://127.0.0.1:8000</b>">http://127.0.0.1:8000**</a>

---

 <b> Использование команд (Management Commands)</b>

В проекте реализованы две ключевые команды для обработки данных.

 <b>1. Парсинг XLSX</b>
Импортирует список адресатов из файла Excel в базу данных:
<pre><code class="language-bash">python manage.py import_xlsx import_data/data.xlsx</code></pre>
<b>2. Эмуляция отправки e-mail</b>
Запускает процесс &quot;отправки&quot; писем из очереди. 
• <b>Особенности</b>: использует <code>select_for_update(skip_locked=True)</code> для безопасной работы в несколько потоков, поддерживает рандомные задержки и систему Retry (до 3 попыток).
<pre><code class="language-bash">python manage.py run_mailing</code></pre>

---

<b> Тестирование</b>

Для запуска тестов (используется <code>pytest</code> с плагинами <code>pytest-django</code> и <code>pytest-mock</code>):

<pre><code class="language-bash">pytest src/apps/mails/tests.py</code></pre>

---
