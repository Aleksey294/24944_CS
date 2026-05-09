# FastAPI Parser + PostgreSQL + Nginx + RuIP

# Запуск

```bash
docker compose up --build
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