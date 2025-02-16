# AVITO TECH INTERNSHIP

## Содержание
1. [Технологии](#технологии)
2. [Инструкция к запуску](#инструкция-к-запуску)
3. [Прописанные ручки](#прописанные-ручки)

## Технологии
В этом проекте используются следующие технологии:
- Python
- FastAPI
- PostgreSQL
- async SQLAlchemy 
- pytest
- Docker
- Docker Compose

## Инструкция к запуску
Для запуска проекта выполните следующие шаги:

1. Установите [Docker](https://www.docker.com/get-started) и [Docker Compose](https://docs.docker.com/compose/install/).

2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/FIVe04/avito_internship_shop.git
   cd avito-tech-internship
   ```

3. Создайте файл `.env` в корневой папке проекта и добавьте следующие переменные окружения:
   ```dotenv
   DB_HOST=db
   DB_PORT=5432
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=avito_store

   TEST_DB_HOST=test_db
   TEST_DB_PORT=5432
   TEST_DB_USER=your_test_db_user
   TEST_DB_PASSWORD=your_test_db_password
   TEST_DB_NAME=avito_test

   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   INITIAL_COINS=1000
   ```

4. Запустите Docker Compose:
   ```bash
   docker-compose up --build
   ```

5. Приложение будет доступно по адресу [http://localhost:8080](http://localhost:8080).

6. Swagger будет доступен по адресу [http://localhost:8080/docs](http://localhost:8080/docs).

## Прописанные ручки
В проекте реализованы следующие API ручки:

### Auth
1. `POST /api/auth/`
   - **Описание**: Аутентификация пользователя и получение токена доступа.
   - **Аргументы**:
     - `form_data` (OAuth2PasswordRequestForm): Данные формы для аутентификации(username, password).

### Info
2. `GET /api/info/`
   - **Описание**: Получение информации о текущем пользователе.

### Purchase
3. `POST /api/buy/`
   - **Описание**: Покупка товара.
   - **Аргументы**:
     - `item` (str): Название товара.

### Transaction
4. `POST /api/sendCoin/`
   - **Описание**: Отправка монет другому пользователю.
   - **Аргументы**:
     - `transaction_info` (TransactionRequest)
       - Информация о транзакции (пользователь-получатель toUser и сумма amount).

```` ▋