from institutes.models import Institute
import json


def store_institutes(path):
    institutes_data = json_to_data(path)
    institutes = institutes_data["institutes"]
    for institute in institutes:
        Institute.objects.create(initials=institute["initials"],
                                 name=institute["name"],
                                 link=institute["link"])


def json_to_data(path):
    """Open .json file with scraped data"""
    with open(path, "r") as file:
        return json.load(file)


def run():
    store_institutes("institutes/institutes.json")
