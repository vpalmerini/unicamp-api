import json


def json_to_data(path):
    """Open .json file in the specified path"""
    with open(path, "r") as file:
        return json.load(file)


def data_to_json(data, path):
    """Store all data in a .json file"""
    with open(path, "w") as file:
        json.dump(data, file, ensure_ascii=False)


def string_to_int(value):
    """Parse numbers in string format to int"""
    if value == "":
        return 0
    else:
        return int(value)
