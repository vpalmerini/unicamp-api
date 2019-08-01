from institutes.models import Institute
from api.utils import json_to_data


def store_institutes(path):
    institutes_data = json_to_data(path)
    institutes = institutes_data["institutes"]
    for institute in institutes:
        Institute.objects.create(initials=institute["initials"],
                                 name=institute["name"],
                                 link=institute["link"])


def run():
    store_institutes("institutes/institutes.json")
