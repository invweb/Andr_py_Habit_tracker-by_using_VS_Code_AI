"""
Habit Tracker — приложение для отслеживания привычек.
Написано на Python с использованием BeeWare (Toga).
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, CENTER, BOLD
import json
import os
from datetime import datetime, date


class HabitData:
    """Хранение и управление данными привычек."""

    def __init__(self, filepath="habits_data.json"):
        self.filepath = filepath
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
        # Проверяем, выполнена ли сегодня или вчера
        today = date.today()
        yesterday = today.__sub__(timedelta(days=1))
        try:
            last = datetime.fromisoformat(dates[-1]).date()
        except (ValueError, TypeError):
            return 0
        if last != today and last != yesterday:
            return 0
        # Считаем серию назад
        count = 1
        for d in reversed(dates[:-1]):
            try:
                prev = datetime.fromisoformat(d).date()
            except (ValueError, TypeError):
                continue
            if prev == last.__sub__(timedelta(days=1)):
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


from datetime import timedelta


class HabitTrackerApp(toga.App):
    """Главное приложение трекера привычек."""

    def startup(self):
        """Инициализация приложения."""
        # Данные
        self.data = HabitData()

        # Главная панель
        main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=20,
                align=CENTER,
            )
        )

        # Заголовок
        title = toga.Label(
            "🎯 Habit Tracker",
            style=Pack(
                font_size=24,
                font_weight=BOLD,
                padding=(0, 0, 10, 0),
                align=CENTER,
            )
        )

        # Подзаголовок
        subtitle = toga.Label(
            f"{date.today().strftime('%d.%m.%Y')}",
            style=Pack(
                font_size=14,
                color="gray",
                padding=(0, 0, 20, 0),
                align=CENTER,
            )
        )

        # Поле ввода + кнопка добавления
        input_box = toga.Box(
            style=Pack(
                direction=ROW,
            )
        )
        self.habit_input = toga.TextInput(
            placeholder="Название привычки...",
            style=Pack(
                flex=1,
                padding_right=10,
            )
        )
        add_button = toga.Button(
            "➕ Добавить",
            on_press=self.add_habit,
            style=Pack(
                width=120,
            )
        )
        input_box.add(self.habit_input)
        input_box.add(add_button)

        # Список привычек
        self.habit_list = toga.List(
            on_select=self.on_habit_selected,
            style=Pack(
                flex=1,
            )
        )

        # Панель статистики
        self.stats_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding_top=10,
            )
        )
        self.stats_label = toga.Label(
            "Добавьте первую привычку!",
            style=Pack(
                align=CENTER,
                font_size=13,
                color="gray",
            )
        )

        # Сборка главного окна
        main_box.add(title)
        main_box.add(subtitle)
        main_box.add(input_box)
        main_box.add(self.habit_list)
        main_box.add(self.stats_box)
        self.stats_box.add(self.stats_label)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.size = (500, 600)
        self.main_window.show()

        # Обновить список
        self.refresh_list()

    def add_habit(self, widget):
        """Добавить привычку по нажатию кнопки."""
        name = self.habit_input.value.strip()
        if not name:
            self.main_window.info_dialog(
                "Внимание",
                "Введите название привычки!"
            )
            return
        if name in [h["name"] for h in self.data.all().values()]:
            self.main_window.info_dialog(
                "Внимание",
                f"Привычка '{name}' уже существует!"
            )
            return
        self.data.add(name)
        self.habit_input.value = ""
        self.refresh_list()
        self.main_window.info_dialog(
            "Готово",
            f"Привычка '{name}' добавлена!"
        )

    def refresh_list(self):
        """Обновить список привычек в UI."""
        self.habit_list.items = []
        habits = self.data.all()
        if not habits:
            self.stats_label.text = "Добавьте первую привычку!"
            return

        count = 0
        total_done = 0
        for h_id, h in habits.items():
            done = self.data.is_completed_today(h_id)
            st = self.data.streak(h_id)
            tot = self.data.total_completed(h_id)
            if done:
                total_done += 1
            count += 1

            # Элемент списка
            row_box = toga.Box(
                style=Pack(
                    direction=ROW,
                    padding=8,
                    align=LEFT,
                )
            )

            # Иконка статуса
            status_icon = toga.Label(
                "✅" if done else "⬜",
                style=Pack(width=40, font_size=18),
            )

            # Название
            name_label = toga.Label(
                h["name"],
                style=Pack(
                    flex=1,
                    font_size=15,
                    color="#888" if done else "black",
                )
            )

            # Бейдж серии
            if st > 0:
                streak_label = toga.Label(
                    f"🔥 {st}",
                    style=Pack(
                        font_size=13,
                        color="orange",
                        padding=(0, 0, 5, 0),
                    )
                )
            else:
                streak_label = toga.Label(
                    "",
                    style=Pack(width=40),
                )

            # Общее количество
            total_label = toga.Label(
                f"Всего: {tot}",
                style=Pack(
                    font_size=12,
                    color="gray",
                    padding=(0, 0, 10, 0),
                )
            )

            # Кнопка выполнения
            toggle_btn = toga.Button(
                "✅" if done else "✔",
                on_press=lambda e, hid=h_id: self.toggle_habit(hid),
                style=Pack(width=50),
            )

            # Кнопка удаления
            del_btn = toga.Button(
                "🗑",
                on_press=lambda e, hid=h_id: self.remove_habit(hid),
                style=Pack(width=40),
            )

            row_box.add(status_icon)
            row_box.add(name_label)
            row_box.add(streak_label)
            row_box.add(total_label)
            row_box.add(toggle_btn)
            row_box.add(del_btn)

            # Сохраняем ID привычки в data
            row_box.on_press = lambda e, hid=h_id: self.on_habit_selected(e, hid=h_id)
            row_box._value = h_id

            self.habit_list.add_item(row_box)

        # Обновить статистику
        today_total = len(habits)
        self.stats_label.text = (
            f"Сегодня: {total_done}/{count} выполнено"
            + (f" | Общий стрик: 🔥" if any(self.data.streak(h) > 0 for h in habits) else "")
        )

    def toggle_habit(self, h_id):
        """Отметить/снять выполнение привычки."""
        self.data.toggle_today(h_id)
        self.refresh_list()

    def remove_habit(self, widget, h_id):
        """Удалить привычку."""
        name = self.data.all()[h_id]["name"]
        ok = self.main_window.confirm_dialog(
            "Удаление",
            f"Удалить привычку '{name}'?"
        )
        if ok:
            self.data.remove(h_id)
            self.refresh_list()

    def on_habit_selected(self, widget, widget_item=None, hid=None):
        """Обработка выбора элемента списка."""
        pass


def main():
    return HabitTrackerApp(formal_name="Habit Tracker")
