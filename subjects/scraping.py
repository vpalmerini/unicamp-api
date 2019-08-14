import json
from selenium import webdriver

driver_path = '/usr/local/lib/chromedriver'
driver = webdriver.Chrome(driver_path)

data = {}
data["subjects"] = []


def get_subjects(path):
    """Gets subjects from institutes webpages and add them to subjects.json"""
    institutes_data = json_to_data(path)
    institutes = institutes_data["institutes"]
    for institute in institutes:
        driver.get(institute["link"])
        subjects = driver.find_elements_by_class_name('disciplina')
        for subject in subjects:
            obj = {}
            obj["institute"] = institute["initials"]
            obj["initials"] = subject.find_element_by_tag_name('a').text.split(
                '\n')[0]
            obj["name"] = subject.find_element_by_tag_name('a').text.split(
                '\n')[-1]
            obj["link"] = subject.find_element_by_tag_name('a').get_attribute(
                'href')
            data["subjects"].append(obj)


def get_subjects_details():
    for subject in data["subjects"]:
        driver.get(subject["link"])
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
                obj = {}
                obj["year_start"] = pre_req.find_element_by_tag_name(
                    'small').text.split()[1].strip()
                obj["year_end"] = pre_req.find_element_by_tag_name(
                    'small').text.split()[3].split(':')[0].strip()
                pre_reqs = pre_req.find_element_by_tag_name('mark').text.split(
                    '/')
                obj["pre_reqs"] = [pr.strip() for pr in pre_reqs]
                subject["pre_reqs"].append(obj)
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


def data_to_json(data):
    """Store all data in a .json file"""
    with open("subjects/subjects.json", "w") as file:
        json.dump(data, file, ensure_ascii=False)


def json_to_data(path):
    """Open .json file with scraped data"""
    with open(path, "r") as file:
        return json.load(file)


def main():
    get_subjects("institutes/institutes.json")
    get_subjects_details()
    data_to_json(data, "subjects/subjects.json")


main()
driver.quit()