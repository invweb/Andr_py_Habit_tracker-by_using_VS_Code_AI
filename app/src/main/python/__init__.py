"""
Habit Tracker Python Module for Android (Chaquopy)
"""
import json
import os
from datetime import datetime, date
from datetime import timedelta


class HabitData:
    """Хранение и управление данными привычек."""
    
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(__file__), "habits_data.json")
        self.habits = self._load()
    
    def _load(self):
        """Загрузка данных из JSON файла."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return {h["id"]: h for h in data}
            except (json.JSONDecodeError, KeyError):
                return {}
        return {}
    
    def save(self):
        """Сохранение данных в JSON файл."""
        habits_list = [
            {
                "id": h_id,
                "name": h["name"],
                "completed_dates": h.get("completed_dates", []),
                "created_at": h.get("created_at", datetime.now().isoformat()),
            }
            for h_id, h in self.habits.items()
        ]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(habits_list, f, ensure_ascii=False, indent=2)
    
    def add(self, name):
        """Добавить новую привычку."""
        h_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.habits[h_id] = {
            "name": name,
            "completed_dates": [],
            "created_at": datetime.now().isoformat(),
        }
        self.save()
        return h_id
    
    def remove(self, h_id):
        """Удалить привычку."""
        if h_id in self.habits:
            del self.habits[h_id]
            self.save()
    
    def toggle_today(self, h_id):
        """Отметить/снять выполнение на сегодня."""
        if h_id in self.habits:
            today = date.today().isoformat()
            if today in self.habits[h_id]["completed_dates"]:
                self.habits[h_id]["completed_dates"].remove(today)
            else:
                self.habits[h_id]["completed_dates"].append(today)
            self.save()
    
    def is_completed_today(self, h_id):
        """Проверить, выполнена ли привычка сегодня."""
        if h_id in self.habits:
            return date.today().isoformat() in self.habits[h_id].get("completed_dates", [])
        return False
    
    def streak(self, h_id):
        """Подсчитать текущую серию (стрик) дней."""
        if h_id not in self.habits:
            return 0
        dates = sorted(self.habits[h_id].get("completed_dates", []))
        if not dates:
            return 0
        today = date.today()
        yesterday = today - timedelta(days=1)
        try:
            last = datetime.fromisoformat(dates[-1]).date()
        except (ValueError, TypeError):
            return 0
        if last != today and last != yesterday:
            return 0
        count = 1
        for d in reversed(dates[:-1]):
            try:
                prev = datetime.fromisoformat(d).date()
            except (ValueError, TypeError):
                continue
            if prev == last - timedelta(days=1):
                count += 1
                last = prev
            else:
                break
        return count
    
    def total_completed(self, h_id):
        """Общее количество выполнений."""
        if h_id in self.habits:
            return len(self.habits[h_id].get("completed_dates", []))
        return 0
    
    def all(self):
        """Вернуть все привычки."""
        return self.habits


# Глобальный экземпляр
_habit_data = None


def get_habit_data():
    """Получить глобальный экземпляр HabitData."""
    global _habit_data
    if _habit_data is None:
        _habit_data = HabitData()
    return _habit_data
