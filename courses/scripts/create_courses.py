from courses.models import Course
from institutes.models import Institute
from api.utils import json_to_data


def store_courses(path):
    courses_data = json_to_data(path)
    courses = courses_data["courses"]
    for course in courses:
        institute_instance = Institute.objects.get(
            initials=course["institute"])
        Course.objects.create(id=course["id"],
                              name=course["name"],
                              shift=course["shift"],
                              institute=institute_instance)


def run():
    store_courses("courses/courses.json")
