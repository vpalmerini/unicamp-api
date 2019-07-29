from classes.models import Class, Schedule
from courses.models import Course
from subjects.models import Subject
import json


def store_classes(path):
    classes_data = json_to_data(path)
    classes = classes_data["classes"]
    for _class in classes:
        subject_instance = Subject.objects.get(initials=_class["subject"])
        class_instance = Class(class_id=_class["class"],
                               positions=string_to_int(_class["positions"]),
                               enrolled=string_to_int(_class["enrolled"]),
                               subject=subject_instance)
        class_instance.save()
        for schedule in _class["schedule"]:
            Schedule.objects.create(day=schedule["day"],
                                    time_start=schedule["time_start"],
                                    time_end=schedule["time_end"],
                                    place=schedule["place"],
                                    class_id=class_instance)
        for course in _class["course_reservation"]:
            try:
                course_instance = Course.objects.get(
                    name=course["course_name"])
                class_instance.courses.add(course_instance)
            except:
                pass


def string_to_int(value):
    if value == "":
        return 0
    else:
        return int(value)


def json_to_data(path):
    """Open .json file with scraped data"""
    with open(path, "r") as file:
        return json.load(file)


def run():
    store_classes("classes/classes.json")
