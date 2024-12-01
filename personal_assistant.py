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