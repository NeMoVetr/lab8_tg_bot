# Telegram-бот для курсовой работы

### 1. Поиск информации в интернете
- Бот умеет искать информацию по запросу пользователя

### 2. Поиск по доменной зоне
- Реализована функция поиска из документов, загруженных ранее (`БД lancedb`) на основе сайта банка ВТБ

### 3. Общение с пользователем
- Интерактивное меню с кнопками
- Обработка текстовых команд
- Поддержка inline-режима


## Структура проекта

```
lab8_tg_bot/
├── .env                 # Файл с переменными окружения (токен бота и т.д.)
├── lancebd              # Векторная база данных
├── pyproject.toml       # Зависимости и настройки проекта
├── bot/                 # Основной код бота
│   ├── __main__.py      # Точка входа
│   ├── config/          # Конфигурации
│   ├── factory/         # Фабрики для создания компонентов
│   ├── handlers/        # Обработчики сообщений
│   ├── keyboards/       # Клавиатуры
│   └── middlewares/     # Промежуточное ПО
```

## Запуск бота

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` с переменными окружения:
```
BOT_TOKEN=ваш_токен_от_BotFather
VECTOR_DB_PATH=путь_к_векторной_базе_данных
OPENAI_API_KEY=ваш_api_ключ_open_ai
TAVILY_API_KEY=ваш_api_ключ_tavily
```

3. Запустите бота:
```bash
uv run python -m bot
```


## Доступные команды

- `/start` - Начало работы с ботом
- `/search_web` - Поиск в интернете
- `/search_docs` - Поиск в документах
- `/ask` - Свободный вопрос ИИ
- `/rag` - RAG (интернет+векторная БД +ИИ)

## Дополнительная информация

Используется библиотека aiogram 3.x и асинхронное программирование (включая asyncio) для обеспечения эффективной обработки запросов.

Для улучшения производительности в проекте используются:
- uvloop (для Linux/macOS) - ускорение асинхронных операций
- orjson - быстрая обработка JSON
- UV - современный пакетный менеджер Python, написанный на Rust, обеспечивающий более быструю установку зависимостей
