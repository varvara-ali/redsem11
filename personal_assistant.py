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