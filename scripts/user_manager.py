import json
import os

PERMISSION_FILE = "data/permissions.json"


def load_permissions():

    if not os.path.exists(PERMISSION_FILE):
        return {}

    with open(PERMISSION_FILE, "r") as file:
        return json.load(file)


def save_permissions(data):

    with open(PERMISSION_FILE, "w") as file:
        json.dump(data, file, indent=4)


def assign_permissions(username, permissions):

    data = load_permissions()

    data[username] = permissions

    save_permissions(data)


def get_permissions(username):

    data = load_permissions()

    return data.get(username, [])


def has_permission(username, permission):

    permissions = get_permissions(username)

    if "all" in permissions:
        return True

    return permission in permissions