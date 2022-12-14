# Проектная работа 5 спринта

Ссылка на репозиторий https://github.com/Ilia-Abrosimov/Async_API_sprint_2

В папке **tasks** ваша команда найдёт задачи, которые необходимо выполнить во втором спринте модуля "Сервис Async API".

Как и в прошлом спринте, мы оценили задачи в стори поинтах.

Вы можете разбить эти задачи на более маленькие, например, распределять между участниками команды не большие куски задания, а маленькие подзадачи. В таком случае не забудьте зафиксировать изменения в issues в репозитории.

**От каждого разработчика ожидается выполнение минимум 40% от общего числа стори поинтов в спринте.**

Запуск всех сервисов:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
```

Вход в контейнер админки

```bash
docker-compose exec admin-panel bash
```

Загрузка данных из sqlite в postgres

```bash
cd sql_to_postgres && python load_data.py
```

Добавление индексов в ES

```bash
make init_dbs
```

Запуск тестов:

```bash
make start_tests
```

Шаблоны необходимых файлов переменных окружения:
- `template.env` для запуска сервисов;
- `tests/functional/template.tests.env` для запуска тестов.
