## Description
Authorization service is the third study module of Middle Python Developer course in Yandex Practicum.

The service is responsible for registration and authentication of users. Also, authentication is possible by OAuth (Google, Yandex).
The ASync-API service uses the Auth service to validate the user's token.

- JWT token for authentication;
- Redis is used to store invalid tokens;
- Use gevent to improve performance of Flask;
- Jaeger is used for request tracing along with requiest id from Nginx's;
- To optimize data storage, the OAuth account table is partitioned by provider name field.


## For integration with Async-API service

Create network in docker `auth_network`

```bash
docker network create auth_network
```

## Start in production mode

```bash
make start_auth
```

## Start in development mode

```bash
make start_auth_dev
```

## Migrations

At first time start need made migrations

```bash
python -m flask db upgrade
```

For create new migrations
```bash
python -m flask db migrate -m "<Migration messsage>"
```

## Testing in development mode

```bash
cd auth_flask_app && python -m pytest
```

## Create superuser

```bash
python -m flask create superuser example@mail.com password
```
## OAuth authorization and authentication
Made from development mode
````
http://127.0.0.1/api/v1/oauth/yandex/login
http://127.0.0.1/api/v1/oauth/google/login
````

## JAEGER UI 
````
http://127.0.0.1:16686/
````

## API specification
````
http://127.0.0.1:<port>/apidocs/
````

# Information about OAuth from different providers

- [Twitter](https://developer.twitter.com/en/docs/authentication/overview){target="_blank"},
- [Facebook](https://developers.facebook.com/docs/facebook-login/){target="_blank"},
- [VK](https://vk.com/dev/access_token){target="_blank"},
- [Google](https://developers.google.com/identity/protocols/oauth2){target="_blank"},
- [Yandex](https://yandex.ru/dev/oauth/?turbo=true){target="_blank"},
- [Mail](https://api.mail.ru/docs/guides/oauth/){target="_blank"}.

## TODO

Implement the ability to unlink your social network account from your personal account.
