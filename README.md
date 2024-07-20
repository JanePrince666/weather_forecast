Веб приложение на Django, позволяющее пользователю вводить название города и получать прогноз погоды на ближайшее время ( 1 час)

Данные о погоде получаются с помощью API сервиса Open-Meteo

Координаты для Open-Meteo получаются с помощью API сервиса Nominatim

Вывод данных о погоде в удобно читаемом формате с использованием HTML/CSS

Приложение помещено в Docker контейнер для легкого развертывания

Через html hеализовано автодополнение при вводе названия города (города добавляются в базу данных при запросе пользователями)

При повторном посещении сайта предлагается посмотреть погоду в городе, который пользователь уже просматривал ранее (хранится в cookies браузера)

Ведется история поисков для каждого пользователя в базе данных PostgresSQL

Реализовано API, показывающее статистику поисков (сколько раз вводили какой город) по адресу http://localhost:8000/api/search-history/ (данные не обнуляются при перезагрузке контейнера)

# Используемые технологии

Python 3.11

Django для создания веб приложения

PostgresSQL для хранения данных

Docker для упаковки приложения в контейнер

HTML/CSS для отображения данных

Библиотека Requests для работы с API Open-Meteo и Nominatim

Для работы с базой данных PostgreSQL в Django используется библиотека psycopg2.

# Инструкция по развертыванию приложения из Docker

Следуйте шагам ниже, чтобы настроить и запустить приложение.

1. Убедитесь, что Docker и Docker Compose установлены

Перед началом убедитесь, что у вас установлены Docker и Docker Compose.
Если они не установлены, следуйте инструкциям на официальных сайтах Docker и Docker Compose для их установки.

2. Клонируйте репозиторий

Сначала клонируйте репозиторий с приложением на ваш локальный компьютер.

3. Перейдите в директорию проекта

Откройте терминал и перейдите в директорию вашего проекта:

```bash
cd /путь/к/вашему/проекту
```

4. Постройте контейнеры

Запустите команду для сборки контейнеров с помощью Docker Compose:
```bash
docker-compose build
```

5. Запустите контейнеры

После успешной сборки запустите контейнеры:
```bash
docker-compose up
```

6. Проверьте работу приложения


После запуска контейнеров ваше приложение должно быть доступно по адресу http://localhost:8000.
Для проверки работы API перейдите по ссылке в браузере  http://localhost:8000/api/search-history/

7. Остановка контейнеров
   
Чтобы остановить запущенные контейнеры, нажмите Ctrl + C в терминале, где выполняется docker-compose up, или выполните команду:
```bash
docker-compose down
```
