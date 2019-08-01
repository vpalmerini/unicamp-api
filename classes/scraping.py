from selenium import webdriver
from api.utils import json_to_data, data_to_json

driver_path = '/usr/local/lib/chromedriver'
driver = webdriver.Chrome(driver_path)

data = {}
data["classes"] = []


def get_classes(path):
    """
    Gets classes from subjects webpages
    """
    subjects_data = json_to_data(path)
    subjects = subjects_data["subjects"]
    for subject in subjects:
        driver.get(subject["link"])
        container = driver.find_element_by_id('conteudo')
        subject_classes_elements = container.find_elements_by_xpath(
            "//div[contains(@class, 'turma')]")
        for subject_class in subject_classes_elements:
            class_obj = {}
            class_obj["subject"] = subject["initials"]
            class_obj["class"] = subject_class.find_element_by_xpath(
                "*//h3[contains(text(), 'Turma')]//following-sibling::span"
            ).text
            class_obj["positions"] = subject_class.find_element_by_xpath(
                "*//span[contains(text(), 'Vagas')]//following-sibling::span"
            ).text
            try:
                class_obj["enrolled"] = subject_class.find_element_by_xpath(
                    "*//p[contains(text(), 'Número de alunos matriculados')]//following-sibling::span"
                ).text
            except:
                class_obj["enrolled"] = ""
            try:
                class_schedule_list_element = subject_class.find_element_by_class_name(
                    'horariosFormatado')
                class_schedule_elements = class_schedule_list_element.find_elements_by_tag_name(
                    'li')
                class_obj["schedule"] = []
                for li in class_schedule_elements:
                    schedule_obj = {}
                    schedule_obj["day"] = li.find_element_by_class_name(
                        'diaSemana').text
                    schedule_obj["time_start"] = li.find_element_by_class_name(
                        'horarios').text.split('-')[0].strip()
                    schedule_obj["time_end"] = li.find_element_by_class_name(
                        'horarios').text.split('-')[-1].strip()
                    schedule_obj["place"] = li.find_element_by_class_name(
                        'salaAula').text
                    class_obj["schedule"].append(schedule_obj)
            except:
                class_obj["schedule"] = []

            try:
                professors_list_element = subject_class.find_element_by_class_name(
                    'docentes')
                professors_elements = professors_list_element.find_elements_by_tag_name(
                    'li')
                class_obj["professors"] = []
                for li in professors_elements:
                    class_obj["professors"].append(li.text)
            except:
                class_obj["professors"] = []

            try:
                courses_list_element = subject_class.find_element_by_class_name(
                    'reservas')
                courses_elements = courses_list_element.find_elements_by_tag_name(
                    'li')
                class_obj["course_reservation"] = []
                for li in courses_elements:
                    course = {}
                    course["course_number"] = li.text.split('-')[0].strip()
                    course["course_name"] = li.text.split('-')[-1].strip()
                    class_obj["course_reservation"].append(course)
            except:
                class_obj["course_reservation"] = []
            data["classes"].append(class_obj)


def main():
    get_classes("subjects/subjects.json")
    # store classes data in classes.json
    data_to_json(data)


main()
driver.quit()