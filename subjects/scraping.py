import json
from selenium import webdriver
from api.utils import data_to_json, json_to_data

driver_path = '/usr/local/lib/chromedriver'
driver = webdriver.Chrome(driver_path)

years = ['2017', '2018', '2019']
semesters = ['1', '2']
graduation_levels = ['G', 'P']

base_url = 'https://www.dac.unicamp.br/portal/caderno-de-horarios/'

data = {}
data["subjects"] = []


def get_subjects(path, years, semesters, graduation_levels):
    """Gets subjects from institutes webpages and add them to subjects.json"""
    institutes_data = json_to_data(path)
    institutes = institutes_data["institutes"]
    for institute in institutes:
        for year in years:
            for semester in semesters:
                for level in graduation_levels:
                    # desconsider CEL institute as it doesn't have graduate courses/subjects
                    if level == "P" and institute["initials"] == "CEL":
                        continue
                    url = base_url + year + '/' + semester + '/' + 'S' + '/' + level + '/' + institute[
                        "initials"]
                    driver.get(url)
                    subjects = driver.find_elements_by_class_name('disciplina')
                    for subject in subjects:
                        sems_obj = {}
                        sems_obj["year"] = year
                        sems_obj["semester"] = semester

                        subj_obj = {}
                        subj_obj["institute"] = institute["initials"]
                        subj_obj[
                            "initials"] = subject.find_element_by_tag_name(
                                'a').text.split('\n')[0]
                        subj_obj["name"] = subject.find_element_by_tag_name(
                            'a').text.split('\n')[-1]
                        subj_obj["degree"] = level
                        subj_obj["semester"] = sems_obj
                        data["subjects"].append(subj_obj)


def get_subjects_details():
    for subject in data["subjects"]:
        url = base_url + subject["semester"]["year"] + '/' + subject[
            "semester"]["semester"] + '/' + 'S' + '/' + subject[
                "degree"] + '/' + subject["institute"] + '/' + subject[
                    "initials"]
        driver.get(url)
        container = driver.find_element_by_id('conteudo')
        basic_info_container = container.find_element_by_class_name(
            'disciplina')
        basic_info_items = basic_info_container.find_elements_by_tag_name('p')
        try:
            subject["syllabus"] = basic_info_container.find_element_by_xpath(
                "//b[contains(text(), 'Ementa')]//parent::p//following-sibling::p"
            ).text
        except:
            subject["syllabus"] = basic_info_container.find_element_by_xpath(
                "//b[contains(text(), 'Ementa')]//parent::p").text
        subject["year"] = basic_info_container.find_element_by_xpath(
            "//b[contains(text(), 'Ano de Catálogo')]//following-sibling::span"
        ).text
        subject["workload"] = basic_info_container.find_element_by_xpath(
            "//b[contains(text(), 'Créditos')]//following-sibling::span").text
        try:
            pre_reqs_list_element = basic_info_container.find_element_by_class_name(
                'prerequisitos')
            pre_reqs_elements = pre_reqs_list_element.find_elements_by_tag_name(
                'li')
            subject["pre_reqs"] = []
            for pre_req in pre_reqs_elements:
                pre_req_obj = {}
                pre_req_obj["year_start"] = pre_req.find_element_by_tag_name(
                    'small').text.split()[1].strip()
                pre_req_obj["year_end"] = pre_req.find_element_by_tag_name(
                    'small').text.split()[3].split(':')[0].strip()
                pre_reqs = pre_req.find_element_by_tag_name('mark').text.split(
                    '/')
                obj["pre_reqs"] = [pr.strip() for pr in pre_reqs]
                subject["pre_reqs"].append(pre_req_obj)
        except:
            # the subject does not have pre-reqs
            subject["pre_reqs"] = []

        try:
            continencies_element = basic_info_container.find_element_by_xpath(
                "//b[contains(text(), 'Continência')]")
            subject[
                "continencies"] = continencies_element.find_element_by_xpath(
                    "following-sibling::mark").text.split('/')
        except:
            # the subject does not have continencies
            subject["continencies"] = []
        try:
            equivalencies_element = basic_info_container.find_element_by_xpath(
                "//b[contains(text(), 'Equivalência')]")
            subject[
                "equivalencies"] = equivalencies_element.find_element_by_xpath(
                    "following-sibling::mark").text.split('/')
        except:
            # the subject does not have equivalencies
            subject["equivalencies"] = []


def main():
    get_subjects("institutes/institutes.json", years, semesters,
                 graduation_levels)
    get_subjects_details()
    data_to_json(data, "subjects/subjects.json")


main()
driver.quit()