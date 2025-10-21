
DOMAIN = "choremate"

CONF_PERSONS = "persons"          # [{"name":"Mama","lines":2}, ...]
DEFAULT_PERSONS = [
    {"name": "Mama", "lines": 2},
    {"name": "Lina", "lines": 2},
    {"name": "Alysha", "lines": 2},
]

DAYS = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]

STORE_KEY = "choremate_db"
STORE_VERSION = 1

# Services
SVC_ASSIGN_NOW = "assign_now"
SVC_ADD_TASK   = "add_task"
SVC_REMOVE_TASK= "remove_task"
SVC_LIST_TASKS = "list_tasks"

# Dispatcher signal
SIGNAL_UPDATED = "choremate_updated"
