https://github.com/Tersaramor/Auth_sprint_2/
<h1>Microservice Online Theater</h1>

![img.png](.github/service_diagram.png)

<h2 align="center">Техничское описание проекта</h2>
Проект построен на основе микросервисной архитектуре. Имеет 4 ключевых сервиса:

1) ***Admin-panel*** (Django + Postgres):

Сервис предназначен для контент-менеджеров, предназначен для управления сущностями кинотеатра: Фильмы, Актеры

Прикрыта nginx, доступна по http://127.0.0.1:80. Админка http://127.0.0.1/admin/. API http://127.0.0.1/api/v1/*

2) ***ETL сервис*** (python + Postgres(*Admin-panel*) + Elasticsearch + Redis):

ETL для перекачки фильмов из базы контента в индексы эластика для последующей удобной отдачи фильмов пользователям (нечеткий поиск с поддержкой множества локалей).

3) ***Search API*** (Fastapi + Elasticsearch (*ETL сервис*) + Redis):

Сервис для отдачи фильмов пользователям. Использует redis для кэширования частых запросов. Авторизация проходит по grpc каналу с сервисом авторизации.

Прикрыта nginx, доступна по http://127.0.0.1:8000. Сваггер http://127.0.0.1:8000/api/openapi. API http://127.0.0.1:8000/api/v1/*


4) ***Auth service***:
   1) **API auth** (Flask + gevent):

      Сервис является HTTP/1.1 <-> HTTP/2.0 прокси для GRPC Auth. Предоставляет REST API для фронтенд клиентов (личный кабинет, PIP ABAC).

      Прикрыта nginx, доступна по http://127.0.0.1:5000. Сваггер http://127.0.0.1:5000/api/openapi. API http://127.0.0.1:5000/api/v1/*

   2) **GRPC auth** (python + GRPC + uvloop + Postgres + Redis):

      Сервис отвечает за данные клиентов, аутентификацию и авторизацию клиентов (JWT+OAUTH), работу с системой политик ABAC (PIP+PAP) и проверкой авторизации пользователей из сторонних сервисов на основе ABAC (PDP).

      Используется модель access + refresh токенов. Redis используется для кэширования проверок доступов пользователя и сохранения данных об актуальных refresh токенах пользователя.

      Также отвечает за распространение авто сгенерированного protoc и различных констант для ABAC PEP клиентов для python в виде PyPi пакета (https://pypi.org/project/grpc-auth-service/).

      ABAC система вдохновлена https://github.com/kolotaev/vakt, сильно пропатчена для удобства взаимодействия и сериализаци данных, использования асинхронных баз и прчоего.

      В прод режиме недоступна вне композ сети. В дев лоступно по 127.0.0.1:50051. Взаимодействие из Postamn коллекции.

<h2 align="center">Запуск проекта</h2>

`make init` Собирает все сервисы (admin panel, etl, search сервис фильмов, auth сервис) без дополнительных действий.

.env.merged собирается из файлов отдельных проектов одной командой, по дефолту нужны порты: 80, 8000, 5432, 15432, 9200, 9300, 5601, 5000, 16686.

Для просмотра логов отдельного сервиса: `docker logs -f <service_name>`

Для сервисов-приложений в dev версии композа проброшены volumes и включен reload.

Трассировка в Jaeger (http://127.0.0.1:16686/)

<h2 align="center">Тестирование сервисов </h2>

`make test_fastapi` (функциональные тесты сервиса выдачи контента)

`make test_auth` (функциональные тесты сервиса авторизации)

<h2> Особенности организации кода </h2>

Для ускорения разработки сервисы собраны в монорепе, каждая папка в корне является отдельным проектом со своими зависимостями и манифестами.
