import json
from json.decoder import JSONDecodeError
from pprint import pprint
from typing import TypedDict
import csv
from datetime import datetime
from fnmatch import fnmatch


class Note(TypedDict):
    id: int
    title: str
    content: str
    timestamp: str


class Task(TypedDict):
    id: int
    title: str
    description: str
    done: bool
    priority: str
    due_date: str


class Contact(TypedDict):
    id: int
    name: str
    phone: str
    email: str


class Finance(TypedDict):
    id: int
    amount: float
    category: str
    date: str
    description: str


class Manager:
    def __init__(self, path):
        self.path = path
        open(path, 'a')

    def load_data(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except JSONDecodeError:
                data = []
            return data

    def save_data(self, data):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def show_all(self, data_to_show = None):
        data = self.load_data()
        if data_to_show:
            for item in data:
                print(*[f"{k}, {v}" for k, v in item.items() if k in data_to_show])
        else:
            for item in data:
                print(item)

    def get_item(self, key, key_value):
        data = self.load_data()
        for item in data:
            if item[key] == key_value:
                return item
        else:
            raise ValueError(f"Нет элемента с {key}={key_value}")

    def add_item(self, item):
        data = self.load_data()
        if data:
            item["id"] = data[-1]['id']+1

        data.append(item)
        self.save_data(data)

    def update_item(self, key, value, new_data: dict):
        data = self.load_data()
        for ind, item in enumerate(data, 0):
            if item[key] == value:
                for k, v in new_data.items():
                    item[k] = v
                break
        else:
            raise ValueError("Нет такого элемента")
        self.save_data(data)
        return 1

    def delete_item(self, key, value):
        data = self.load_data()
        for item in data:
            if item[key] == value:
                data.remove(item)
                break
        else:
            raise ValueError("Нет такого элемента")
        self.save_data(data)

    def export_csv(self, path):
        data = self.load_data()
        with open(path, 'w', encoding='utf-8', newline='') as f:
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

    def import_csv(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            writer = csv.DictReader(f)
            data = list(writer)
            self.save_data(data)

note_manager = Manager('notes.json')
task_manager = Manager('tasks.json')
contact_manager = Manager('contacts.json')
finance_manager = Manager('finance.json')


def note_func():
    while True:
        print(
            "\nВыберите действие:\n"
            "1. Создать новую заметку\n"
            "2. Просмотр списка заметок\n"
            "3. Просмотр подробностей заметки\n"
            "4. Редактирование заметки\n"
            "5. Удаление заметки\n"
            "6. Экспорт в csv\n"
            "7. Импорт из csv\n"
            "8. Выход в главное меню"
        )
        action = input("Действие: ")
        print("")
        match action:
            case "1":
                title = input("Введите заголовок: ")
                if not title:
                    print("Ошибка: заголовок- обязательное поле")
                    continue
                content = input("Введите содержимое заметки(или оставьте поле пустым): ")
                timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                note_manager.add_item({
                    "id": 0,  # В последствии замениться
                    "title": title,
                    "content": content,
                    "timestamp": timestamp
                })
            case "2":
                notes = note_manager.load_data()
                if not notes:
                    print("Нет заметок")
                    continue
                print("Список заметок:")
                for note in notes:
                    print(note['title'])

            case "3":
                title = input("Введите заголовок заметки: ")
                try:
                    note = note_manager.get_item("title", title)
                    print(*[
                        f"Заголовок: {note['title']}",
                        f"Содержание: {note['content']}",
                        f"Время создания: {note['timestamp']}"
                    ],sep='\n')
                except ValueError:
                    print("Нет заметки с таким заголовком")
            case "4":
                title = input("Введите заголовок заметки: ")

                new_title = input("Введите новый заголовок: ")
                if not title:
                    print("Ошибка: заголовок - обязательное поле")
                    continue
                content = input("Введите обновленное содержимое заметки(или оставьте поле пустым): ")
                data_to_update = {
                    "title": new_title,
                    "content": content
                }
                try:
                    note_manager.update_item('title', title, data_to_update)
                except ValueError:
                    print("Нет элемента с таким заголовком.")
            case "5":
                title = input("Введите заголовок заметки: ")
                try:
                    note_manager.delete_item('title', title)
                except ValueError:
                    print("Нет элемента с таким заголовком.")
            case "6":
                path = input("Укажи путь до файла: ")
                note_manager.export_csv(path)
            case "7":
                path = input("Укажи путь до файла: ")
                note_manager.import_csv(path)
            case "8":
                break
            case _:
                print("Неверная команда")


def task_func():
    print("\nУправление задачами")
    while True:
        print("\nВыберете действие\n"
              "1. Добавление новой задачи.\n"
              "2. Просмотр списка задач с отображением статуса, приоритета и срока.\n"
              "3. Отметка задачи как выполненной.\n"
              "4. Редактирование задачи.\n"
              "5. Удаление задачи.\n"
              "6. Импорт задач в формате CSV.\n"
              "7. Экспорт задач в формате CSV.\n"
              "8. Выход")
        action = input("Выберите действие: ")
        print("")

        match action:
            case "1":
                title = input("Введите заголовок: ")
                if not title:
                    print("Ошибка: заголовок - обязательное поле")
                    continue

                description = input("Введите подробное описание задачи: ")

                match input("Статус задачи. Выполнена(1) или нет(0 или любое другое значение))"):
                    case "1":
                        done = True
                    case _:
                        done = False

                priority = input("Приоритет задачи («Высокий», «Средний», «Низкий»): ")
                if priority.lower() not in ("высокий", "средний", "низкий"):
                    print("Ошибка! Неверное значение приоритета.")
                    continue

                due_date = input("Срок выполнения задачи в формате ДД-ММ-ГГГГ: ")
                try:
                    datetime.strptime(due_date, '%d-%m-%Y')
                except ValueError:
                    print("Ошибка! Неверный формат даты.")
                    continue

                item = {
                    "id": 0,
                    "title": title,
                    "description": description,
                    "done": done,
                    "priority": priority,
                    "due_date": due_date,
                }
                task_manager.add_item(item)
            case "2":
                all_tasks: list[Task] = task_manager.load_data()
                if not all_tasks:
                    print("Список задач пуст.")
                    continue
                print("Список задач:")
                for task in all_tasks:
                    print(*[
                        f'Название : {task["title"]}',
                        f'Статус : {task["done"]}',
                        f'Приоритет : {task["priority"]}',
                        f'Срок : {task["due_date"]}',
                        '___'
                    ],sep="\n")
            case "3":
                title = input("Введите заголовок задачи: ")
                try:
                    task_manager.update_item('title', title, {"done": True})
                except ValueError:
                    print("Ошибка!. Задача с таким заголовком не найдена.")
            case "4":
                title = input("Введите старый заголовок: ")

                new_title = input("Введите новый заголовок: ")
                if not new_title:
                    print("Ошибка: заголовок - обязательное поле")
                    continue

                description = input("Введите новое описание задачи: ")

                match input("Статус задачи. Выполнена(1) или нет(любое другое значение)): "):
                    case "1":
                        done = True
                    case _:
                        done = False

                priority = input("Приоритет задачи («Высокий», «Средний», «Низкий»).")
                if priority.lower() not in ("высокий", "средний", "низкий"):
                    print("Ошибка! Неверное значение приоритета.")
                    continue

                due_date = input("Срок выполнения задачи в формате ДД-ММ-ГГГГ: ")
                try:
                    datetime.strptime(due_date, '%d-%m-%Y')
                except ValueError:
                    print("Ошибка! Неверный формат даты.")
                    continue

                data_to_update = {
                    "title": new_title,
                    "description": description,
                    "done": done,
                    "priority": priority,
                    "due_date": due_date,
                }
                task_manager.update_item('title', title, data_to_update)
            case "5":
                title = input("Введите заголовок заметки: ")
                try:
                    task_manager.delete_item('title', title)
                except ValueError:
                    print("Нет элемента с таким заголовком.")
            case "6":
                path = input("Укажи путь до файла: ")
                task_manager.import_csv(path)
            case "7":
                path = input("Укажи путь до файла: ")
                task_manager.export_csv(path)
            case "8":
                break
            case _:
                print("Неверная команда")


