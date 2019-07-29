from subjects.models import Subject, PreReq, Continence, Equivalence
from institutes.models import Institute
import json


def store_subjects(path):
    subjects_data = json_to_data(path)
    subjects = subjects_data["subjects"]

    for subject in subjects:
        institute_instance = Institute.objects.get(
            initials=subject["institute"])
        subject_instance = Subject(initials=subject["initials"],
                                   name=subject["name"],
                                   link=subject["link"],
                                   syllabus=subject["syllabus"],
                                   year=subject["year"],
                                   workload=string_to_int(subject["workload"]),
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
    store_subjects("subjects/subjects.json")
