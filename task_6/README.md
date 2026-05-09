# FastAPI Parser + PostgreSQL + Nginx

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
## 5. Запустить Nginx

```bash
docker run -d --name nginx_proxy --network parser-network -p 80:80 -v ${PWD}\nginx.conf:/etc/nginx/conf.d/default.conf:ro nginx
```

# Проверка

Swagger:

```text
http://localhost:80/docs
```

Парсинг сайта:

```http
POST http://localhost:80/parse
```

Body:

```json
{
  "url": "https://plati.market/cat/game-accounts/21940/"
}
```

Получение всех товаров:

```http
GET http://localhost:80/items
```