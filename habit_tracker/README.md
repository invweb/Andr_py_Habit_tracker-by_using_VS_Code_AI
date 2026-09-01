# 🎯 Habit Tracker — BeeWare App

Простое приложение для отслеживания ежедневных привычек, написанное на **Python** с использованием **BeeWare (Toga)**.

## Возможности

- ✅ Добавление привычек
- ✅ Отметка выполнения на сегодня
- ✅ Подсчёт текущей серии (streak) 🔥
- ✅ Общее количество выполнений
- ✅ Удаление привычек
- ✅ Автосохранение данных (JSON)
- 🎨 Современный минималистичный интерфейс

## Установка

```bash
# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # на Windows: venv\Scripts\activate

# Установите зависимости
pip install toga toga-core toga-cocoa
```

## Запуск

```bash
cd habit_tracker
python -m src.habit_tracker
```

## Структура проекта

```
habit_tracker/
├── src/
│   └── habit_tracker/
│       ├── __init__.py        # Инициализация пакета
│       ├── __main__.py        # Точка входа
│       └── app.py             # Основной код приложения
├── briefcase.toml             # Конфигурация BeeWare
├── pyproject.toml             # Метаданные проекта
└── README.md
```

## Как это работает

### Класс `HabitData`
Управление данными привычек:
- `add(name)` — добавить привычку
- `remove(id)` — удалить привычку
- `toggle_today(id)` — отметить/снять выполнение
- `streak(id)` — подсчитать серию дней
- `total_completed(id)` — общее количество выполнений
- Данные сохраняются в `habits_data.json`

### Класс `HabitTrackerApp`
GUI на Toga:
- Список привычек с иконками статуса
- Поле ввода для добавления новых
- Кнопки выполнения и удаления
- Статистика выполнения за день

## Сборка для платформ

```bash
# Установка Briefcase
pip install briefcase

# Создание distributable для macOS
cd habit_tracker
briefcase create macos
briefcase build macos
briefcase run macos

# Для Linux
briefcase create linux
briefcase build linux
briefcase run linux

# Для Windows
briefcase create windows
briefcase build windows
briefcase run windows
```

## Технологии

- **Python 3.9+** — язык программирования
- **BeeWare / Toga** — кроссплатформенный GUI фреймворк
- **Travertino** — стилизация (входит в BeeWare)
- **JSON** — хранение данных

## Лицензия

MIT
