import django
django.setup()
from subjects.models import *
import json
import time


def json_to_data(path):
    """Open .json file with scraped data"""
    with open(path, "r") as file:
        return json.load(file)


def store_institutes():
    data = json_to_data("data/subjects.json")
    for institute in data["institutes"]:
        Institute.objects.create(initials=institute["initials"],
                                 name=institute["name"],
                                 link=institute["link"])


def store_courses():
    data = json_to_data("data/courses.json")
    for course in data["courses"]:
        institute_instance = Institute.objects.get(
            initials=course["institute"])
        Course.objects.create(id=course["id"],
                              name=course["name"],
                              shift=course["shift"],
                              institute=institute_instance)


def store_subjects(data):
    for institute in data["institutes"]:
        institute_instance = Institute.objects.get(
            initials=institute["initials"])
        for subject in institute["subjects"]:
            subject_instance = Subject(initials=subject["initials"],
                                       name=subject["name"],
                                       link=subject["link"],
                                       syllabus=subject["syllabus"],
                                       year=subject["year"],
                                       workload=subject["workload"],
                                       institute=institute_instance)
            subject_instance.save()
            for pre_req_obj in subject["pre_reqs"]:
                for pre_req in pre_req_obj["pre_reqs"]:
                    if pre_req != "":
                        try:
                            pre_req_instance = PreReq.objects.get(
                                initials=str(pre_req),
                                year_start=pre_req_obj["year_start"],
                                year_end=pre_req_obj["year_end"])
                        except:
                            pre_req_instance = PreReq(
                                initials=str(pre_req),
                                year_start=pre_req_obj["year_start"],
                                year_end=pre_req_obj["year_end"])
                            pre_req_instance.save()
                        subject_instance.prereqs.add(pre_req_instance)

            for cont_elem in subject["continencies"]:
                if cont_elem != "":
                    try:
                        continence = Continence.objects.get(
                            initials=str(cont_elem))
                    except:
                        continence = Continence(initials=str(cont_elem))
                        continence.save()
                    subject_instance.continences.add(continence)

            for equiv_elem in subject["equivalencies"]:
                if equiv_elem != "":
                    try:
                        equivalence = Equivalence.objects.get(
                            initials=str(equiv_elem))
                    except:
                        equivalence = Equivalence(initials=str(equiv_elem))
                        equivalence.save()
                    subject_instance.equivalences.add(equivalence)


def store_classes(data):
    for institute in data["institutes"]:
        institute_instance = Institute.objects.get(
            initials=institute["initials"])
        for subject in institute["subjects"]:
            subject_instance = Subject.objects.get(
                initials=subject["initials"])
            for _class in subject["classes"]:
                class_instance = Class(class_id=_class["class"],
                                       positions=_class["positions"],
                                       enrolled=_class["enrolled"],
                                       subject=subject_instance)
                class_instance.save()
                for schedule in _class["schedule"]:
                    Schedule.objects.create(day=schedule["day"],
                                            time_start=schedule["time_start"],
                                            time_end=schedule["time_end"],
                                            place=schedule["place"],
                                            class_id=class_instance)
                for professor in _class["professors"]:
                    try:
                        professor_instance = Professor.objects.get(
                            name=str(professor))
                    except:
                        professor_instance = Professor(
                            name=str(professor), institute=institute_instance)
                        professor_instance.save()
                    professor_instance.classes.add(class_instance)

                for course in _class["course_reservation"]:
                    try:
                        course_instance = Course.objects.get(
                            name=course["course_name"])
                        class_instance.courses.add(course_instance)
                    except:
                        pass


def main():
    data = json_to_data("data/subjects.json")
    store_institutes()
    store_courses()
    store_subjects(data)
    store_classes(data)


main()
