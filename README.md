## Ссылка на репозиторий

https://github.com/Ilia-Abrosimov/Auth_sprint_2

## Интеграция с другими сервисами

Для создания сети `auth_network`

```bash
docker network create auth_network
```

## Запуск в режиме prod

```bash
make start_auth
```

## Запуск в режиме dev

```bash
make start_auth_dev
```

## Миграции

При первом запуске проекта (создании БД) необходимо накатить миграции.
Из директрии с проектом необходимо выполнить следующее:

```bash
python -m flask db upgrade
```

Для создания новой миграции необходимо выполнить
```bash
python -m flask db migrate -m "<Migration messsage>"
```

## Запуск тестов в dev сборке

```bash
cd auth_flask_app && python -m pytest
```

## Создание суперпользователя
Для создания нового пользователя superuser можно воспользоваться cli-командой:

```bash
python -m flask create superuser example@mail.com password
```
## Вход через OAuth
Выполняется из dev сборки
````
http://127.0.0.1:50/api/v1/oauth/yandex/login
````

## JAEGER UI 
````
http://127.0.0.1:16686/
````

## Документация 
````
http://127.0.0.1:<port>/apidocs/
````

# Проектная работа 7 спринта

Упростите регистрацию и аутентификацию пользователей в Auth-сервисе, добавив вход через социальные сервисы. Список сервисов выбирайте исходя из целевой аудитории онлайн-кинотеатра — подумайте, какими социальными сервисами они пользуются. Например, использовать [OAuth от Github](https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps){target="_blank"} — не самая удачная идея. Ваши пользователи не разработчики и вряд ли имеют аккаунт на Github. А вот добавить Twitter, Facebook, VK, Google, Yandex или Mail будет хорошей идеей.

Вам не нужно делать фронтенд в этой задаче и реализовывать собственный сервер OAuth. Нужно реализовать протокол со стороны потребителя.

Информация по OAuth у разных поставщиков данных:

- [Twitter](https://developer.twitter.com/en/docs/authentication/overview){target="_blank"},
- [Facebook](https://developers.facebook.com/docs/facebook-login/){target="_blank"},
- [VK](https://vk.com/dev/access_token){target="_blank"},
- [Google](https://developers.google.com/identity/protocols/oauth2){target="_blank"},
- [Yandex](https://yandex.ru/dev/oauth/?turbo=true){target="_blank"},
- [Mail](https://api.mail.ru/docs/guides/oauth/){target="_blank"}.

## Дополнительное задание

Реализуйте возможность открепить аккаунт в соцсети от личного кабинета.

Решение залейте в репозиторий текущего спринта и отправьте на ревью.
