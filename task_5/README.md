# FastAPI Parser + PostgreSQL

# Запуск

## 1. Создать сеть

```bash
docker network create parser-network
```

## 2. Запустить PostgreSQL

```bash
docker run -d --name db_container --network parser-network -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=parser_db -p 5432:5432 postgres:16
```

## 3. Собрать приложение

```bash
docker build -t parser_app .
```

## 4. Запустить приложение

```bash
docker run -d --name parser_app --network parser-network -p 8000:8000 parser_app  
```

# Проверка

Swagger:

```text
http://localhost:8000/docs
```

Парсинг сайта:

```http
POST http://localhost:8000/parse
```

Body:

```json
{
  "url": "https://plati.market/cat/game-accounts/21940/"
}
```

Получение всех товаров:

```http
GET http://localhost:8000/items
```