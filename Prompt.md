````markdown
Ты — Senior Fullstack Developer. Твоя задача — реализовать полноценное тестовое задание: Backend-сервис для лендинга разработчика с AI-интеграцией и аккуратным Frontend-ом.

Работай итеративно, но сначала создай полную структуру проекта. Код должен быть production-ready, чистым, с строгой типизацией и без "магии".

### 🛠 ТЕХНОЛОГИЧЕСКИЙ СТЕК

**Backend:** Python 3.10+, FastAPI, SQLAlchemy 2.0 (async), aiosqlite, httpx (для AI), pydantic-settings.
**Frontend:** React 18+, Vite, TypeScript, Tailwind CSS (для идеальной верстки и чистоты), React Hook Form + Zod (для валидации).
**AI:** Yandex Cloud Foundation Models API (YandexGPT).

### 🔐 ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ (.env)

Создай файл `.env` в корне backend и frontend (если нужно). Для backend используй следующие реальные ключи (не меняй их):

```env
# Yandex GPT Credentials
YANDEX_FOLDER_ID=b1ge01onkmheu7tiv0od
YANDEX_API_KEY=your_api_key_here
YANDEX_GPT_MODEL_URI=yandexgpt

# App Settings
APP_ENV=development
RATE_LIMIT_MAX_REQUESTS=3
RATE_LIMIT_WINDOW_MINUTES=60

# Email (Mock mode for test task)
EMAIL_MOCK_MODE=true
```
````

---

### 🏗 BACKEND ТРЕБОВАНИЯ (Архитектура и Логика)

**1. Структура (Слоистая архитектура):**

```text
backend/
├── app/
│   ├── api/            # Роутеры (Controllers)
│   ├── core/           # Конфиг, безопасность, exceptions, middleware
│   ├── repositories/   # Работа с SQLite (CRUD)
│   ├── schemas/        # Pydantic модели (Request/Response)
│   ├── services/       # Бизнес-логика (Contact, AI, Email, RateLimit)
│   └── main.py         # Точка входа, CORS, Global Error Handler
├── logs/               # Папка для логов
├── data/               # Папка для SQLite и rate_limit.json
├── .env
└── requirements.txt
```

**2. Эндпоинты:**

- `POST /api/contact`: Прием заявки. Валидация (имя, телефон, email, комментарий).
- `GET /api/health`: Проверка статуса.
- `GET /api/metrics`: Статистика (всего заявок, успешных AI, fallback AI).

**3. AI-Интеграция (YandexGPT) - КРИТИЧНО:**

- Используй `httpx.AsyncClient` для запросов.
- **Эндпоинт Yandex:** `https://llm.api.cloud.yandex.net/foundationModels/v1/completion`
- **Headers:** `Authorization: Api-Key {YANDEX_API_KEY}`
- **Body формат:**
    ```json
    {
    	"modelUri": "gpt://{YANDEX_FOLDER_ID}/{YANDEX_GPT_MODEL_URI}",
    	"completionOptions": {
    		"stream": false,
    		"temperature": 0.3,
    		"maxTokens": 1000
    	},
    	"messages": [
    		{
    			"role": "system",
    			"text": "Ты ассистент разработчика. Проанализируй текст заявки и верни СТРОГО JSON без markdown: {\"sentiment\": \"positive/negative/neutral\", \"category\": \"frontend/backend/design/consulting\", \"draft_reply\": \"текст ответа\"}"
    		},
    		{ "role": "user", "text": "{comment}" }
    	]
    }
    ```
- **Graceful Fallback:** Оберни запрос в `try/except` и `asyncio.wait_for(timeout=10)`. Если ошибка/таймаут — логируй и возвращай дефолтные значения. Сервис не должен падать!

**4. Инфраструктура:**

- **Rate Limiting:** Реализуй через чтение/запись JSON файла (`data/rate_limits.json`). Ключ — IP, значение — список timestamp'ов.
- **Логирование:** Настрой `logging` с `RotatingFileHandler`. Пиши в `logs/app.log`. Логируй каждый запрос (method, path, status, time).
- **Email:** Сделай `EmailService`. Так как это тестовое, реализуй `MockEmailService`, который просто красиво логирует "отправленные" письма в `logs/emails.log` и в консоль, но имеет интерфейс для реальной отправки.
- **Глобальный Error Handler:** Перехватывай все исключения, логируй traceback, отдавай клиенту чистый JSON `{"detail": "..."}`.

---

### 🎨 FRONTEND ТРЕБОВАНИЯ (АКЦЕНТ НА ЧИСТОТУ И АККУРАТНОСТЬ)

Мне нужен **идеально чистый, современный и аккуратный** одностраничник. Никакого "колхозного" CSS.
**Стек:** React + TS + Vite + Tailwind CSS.

**1. Архитектура фронтенда:**

```text
frontend/src/
├── assets/         # Иконки, шрифты
├── components/     # UI компоненты (Button, Input, Card)
├── features/       # Фичи (ContactForm, HeroSection, AIChat)
├── hooks/          # Кастомные хуки (useContactForm, useTheme)
├── services/       # API клиент (axios/fetch wrapper)
├── types/          # Глобальные TS типы
└── App.tsx
```

**2. Дизайн и UX (Минимализм, Dark/Light mode, Developer Portfolio style):**

- Используй Tailwind. Цветовая палитра: строгая, современная (например, slate/zinc для фона, accent color — синий или изумрудный).
- **Секции:**
    1. **Hero:** Краткое приветствие, имя, роль.
    2. **Contact Form:** Аккуратная форма. Поля: Имя, Телефон, Email, Комментарий.
    3. **AI Status:** Небольшой блок, показывающий, что форма обрабатывается AI (анимация загрузки, затем показ сгенерированного черновика ответа или тональности).

**3. Код и Качество (СТРОГО):**

- **TypeScript:** Строгая типизация. Никаких `any`. Используй `zod` для валидации схем форм.
- **Хуки:** Вынеси логику формы в кастомный хук `useContactForm`. Компонент должен быть "тупым" (presentational).
- **Состояния:** Обязательно обработай состояния: `idle`, `loading`, `success`, `error`. Покажи спиннер при отправке, красивое toast-уведомление или inline-сообщение об успехе/ошибке.
- **API Клиент:** Настрой `fetch` или `axios` с базовым URL и обработкой ошибок.

---

### 📝 ЧТО НУЖНО СДЕЛАТЬ ПРЯМО СЕЙЧАС (ПЛАН ДЕЙСТВИЙ)

1. **Шаг 1:** Создай структуру папок и файл `.env` с указанными ключами.
2. **Шаг 2:** Напиши Backend: `main.py`, конфиги, модели БД, репозитории.
3. **Шаг 3:** Напиши Backend Services: RateLimit, Email (Mock), AI (YandexGPT с fallback).
4. **Шаг 4:** Напиши Backend API роутеры и подключи их.
5. **Шаг 5:** Инициализируй Frontend (Vite + TS + Tailwind). Настрой конфиги.
6. **Шаг 6:** Напиши чистый, аккуратный Frontend код (компоненты, хуки, стили).
7. **Шаг 7:** Напиши подробный `README.md` по требованиям тестового (включая раздел "Что сделано с помощью AI", где укажи, что архитектура и boilerplate сгенерированы Claude Code, а YandexGPT интеграция и UI-стили доработаны вручную).

Начинай с Шага 1 и Шага 2. Пиши код сразу целиком, без сокращений вроде `# ... остальной код`. Жду код!

```

```
