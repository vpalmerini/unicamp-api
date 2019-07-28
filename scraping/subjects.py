import json
from selenium import webdriver

main_url = 'https://www.dac.unicamp.br/portal/caderno-de-horarios/2019/1/S/G'
driver_path = '/usr/local/lib/chromedriver'

driver = webdriver.Chrome(driver_path)
driver.get(main_url)

data = {}
data["institutes"] = []


def get_institutes(url):
    """Get institutes objects and add them to data"""
    driver.get(url)
    institutes = driver.find_elements_by_class_name('item')

    for institute in institutes:
        initials = institute.find_element_by_tag_name('a').text.split('\n')[0]
        name = institute.find_element_by_tag_name('a').text.split('\n')[-1]
        link = institute.find_element_by_tag_name('a').get_attribute('href')
        obj = {}
        obj["initials"] = initials
        obj["name"] = name
        obj["link"] = link
        obj["subjects"] = []
        data["institutes"].append(obj)


def get_subjects(institutes):
    """Get subjects from institutes and add them to data"""
    for institute in institutes:
        driver.get(institute["link"])
        subjects = driver.find_elements_by_class_name('disciplina')
        for subject in subjects:
            initials = subject.find_element_by_tag_name('a').text.split('\n')[0]
            name = subject.find_element_by_tag_name('a').text.split('\n')[-1]
            link = subject.find_element_by_tag_name('a').get_attribute('href')
            obj = {}
            obj["initials"] = initials
            obj["name"] = name
            obj["link"] = link
            institute["subjects"].append(obj)


def get_classes(institutes):
    """Get classes from subjects and add them to data"""
    for institute in institutes:
        for subject in institute["subjects"]:
            driver.get(subject["link"])
            container = driver.find_element_by_id('conteudo')
            basic_info_container = container.find_element_by_class_name('disciplina')
            basic_info_items = basic_info_container.find_elements_by_tag_name('p')
            try:
                syllabus = basic_info_container.find_element_by_xpath("//b[contains(text(), 'Ementa')]//parent::p//following-sibling::p").text
            except:
                syllabus = basic_info_container.find_element_by_xpath("//b[contains(text(), 'Ementa')]//parent::p").text
            year = basic_info_container.find_element_by_xpath("//b[contains(text(), 'Ano de Catálogo')]//following-sibling::span").text
            workload = basic_info_container.find_element_by_xpath("//b[contains(text(), 'Créditos')]//following-sibling::span").text

            subject["syllabus"] = syllabus
            subject["year"] = year
            subject["workload"] = workload

            try:
                pre_reqs_list_element = basic_info_container.find_element_by_class_name('prerequisitos')
                pre_reqs_elements = pre_reqs_list_element.find_elements_by_tag_name('li')
                subject["pre_reqs"] = []
                for pre_req in pre_reqs_elements:
                    obj = {}
                    obj["year_start"] = pre_req.find_element_by_tag_name('small').text.split()[1].strip()
                    obj["year_end"] = pre_req.find_element_by_tag_name('small').text.split()[3].split(':')[0].strip()
                    pre_reqs = pre_req.find_element_by_tag_name('mark').text.split('/')
                    obj["pre_reqs"] = [pr.strip() for pr in pre_reqs]
                    subject["pre_reqs"].append(obj)
            except:
                # the subject does not have pre-reqs
                subject["pre_reqs"] = []

            try:
                continencies_element = basic_info_container.find_element_by_xpath("//b[contains(text(), 'Continência')]")
                subject["continencies"] = continencies_element.find_element_by_xpath("following-sibling::mark").text.split('/')
            except:
                # the subject does not have continencies
                subject["continencies"] = []
            try:
                equivalencies_element = basic_info_container.find_element_by_xpath("//b[contains(text(), 'Equivalência')]")
                subject["equivalencies"] = equivalencies_element.find_element_by_xpath("following-sibling::mark").text.split('/')
            except:
                # the subject does not have equivalencies
                subject["equivalencies"] = []

            subject["classes"] = []
            subject_classes_elements = container.find_elements_by_xpath("//div[contains(@class, 'turma')]")
            for subject_class in subject_classes_elements:
                class_obj = {}
                class_obj["class"] = subject_class.find_element_by_xpath("*//h3[contains(text(), 'Turma')]//following-sibling::span").text
                class_obj["positions"] = subject_class.find_element_by_xpath("*//span[contains(text(), 'Vagas')]//following-sibling::span").text
                try:
                    class_obj["enrolled"] = subject_class.find_element_by_xpath("*//p[contains(text(), 'Número de alunos matriculados')]//following-sibling::span").text
                except:
                    class_obj["enrolled"] = ""
                try:
                    class_schedule_list_element = subject_class.find_element_by_class_name('horariosFormatado')
                    class_schedule_elements = class_schedule_list_element.find_elements_by_tag_name('li')
                    class_obj["schedule"] = []
                    for li in class_schedule_elements:
                        schedule_obj = {}
                        schedule_obj["day"] = li.find_element_by_class_name('diaSemana').text
                        schedule_obj["time_start"] = li.find_element_by_class_name('horarios').text.split('-')[0].strip()
                        schedule_obj["time_end"] = li.find_element_by_class_name('horarios').text.split('-')[-1].strip()
                        schedule_obj["place"] = li.find_element_by_class_name('salaAula').text
                        class_obj["schedule"].append(schedule_obj)
                except:
                    class_obj["schedule"] = []

                try:
                    professors_list_element = subject_class.find_element_by_class_name('docentes')
                    professors_elements = professors_list_element.find_elements_by_tag_name('li')
                    class_obj["professors"] = []
                    for li in professors_elements:
                        class_obj["professors"].append(li.text)
                except:
                    class_obj["professors"] = []

                try:
                    courses_list_element = subject_class.find_element_by_class_name('reservas')
                    courses_elements = courses_list_element.find_elements_by_tag_name('li')
                    class_obj["course_reservation"] = []
                    for li in courses_elements:
                        course = {}
                        course["course_number"] = li.text.split('-')[0].strip()
                        course["course_name"] = li.text.split('-')[-1].strip()
                        class_obj["course_reservation"].append(course)
                except:
                    class_obj["course_reservation"] = []
                subject["classes"].append(class_obj)


def data_to_json(data):
    """Store all data in a .json file"""
    with open("subjects.json", "w") as file:
        json.dump(data, file, ensure_ascii=False)

def main():
    get_institutes(main_url)
    get_subjects(data["institutes"])
    get_classes(data["institutes"])
    data_to_json(data)

main()