from professors.models import Professor
from subjects.models import Subject
import json


def store_professors(path):
    classes_data = json_to_data(path)
    classes = classes_data["classes"]
    for _class in classes:
        professors = _class["professors"]
        for professor in professors:
            try:
                subject_instance = Subject.objects.get(
                    initials=_class["subject"])
                class_instance = subject_instance.class_set.get(
                    class_id=_class["class"])
                institute = subject_instance.institute
                professor_instance = Professor(name=str(professor),
                                               institute=institute)
                professor_instance.save()
                professor_instance.classes.add(class_instance)
            except:
                pass


def json_to_data(path):
    """Open .json file with scraped data"""
    with open(path, "r") as file:
        return json.load(file)


def run():
    store_professors("classes/classes.json")
