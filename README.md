## Установка
```bash
pip install fastapi uvicorn sqlalchemy
uvicorn main:app --reload
```
- positive: ["хорош", "люблю", "отлич", "нрав", "прекрас", "супер", "класс", "рекоменд", "шикар", "удивит"]
- negative: ["плохо", "ненавиж", "ужас", "отврат", "кошмар", "разочар", "бесполез", "дерьм", "слаб", "глуп"]
- curl -X 'POST' \
  'http://127.0.0.1:8000/reviews' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Ваше резюме отлтичное и мне нравится"
}'
{
  "id": 7,
  "text": "Ваше резюме отлтичное и мне нравится",
  "sentiment": "positive",
  "created_at": "2025-07-29T14:02:00.959075"
}

- curl -X 'GET' \
  'http://127.0.0.1:8000/reviews?sentiment=negative' \
  -H 'accept: application/json'

[
  {
    "id": 5,
    "text": "Ваше резюме глупое слабое",
    "sentiment": "negative",
    "created_at": "2025-07-29T13:57:56.771505"
  }
]
