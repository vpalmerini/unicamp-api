import time
import codecs
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from api.utils import data_to_json, json_to_data

driver_path = '/usr/local/lib/chromedriver'

data = {}
data["students"] = []

base_url = "https://www1.sistemas.unicamp.br/altmatr/menupublico.do"
files_path = "/home/victorpalmerini/Downloads/"


def get_students_class(_class):
    """
    Scraps data from students that are enrolled in the
    _class passed as parameter.
    """
    driver = webdriver.Chrome(driver_path)
    driver.get(base_url)
    container = driver.find_elements_by_class_name("submenu")[-1]
    matriculados_link = container.find_element_by_tag_name("a").click()

    # switches to the new window
    time.sleep(0.5)
    driver.switch_to_window(driver.window_handles[-1])
    time.sleep(0.5)
    forms = driver.find_element_by_name("FormSelecionarNivelPeriodoDisciplina")
    time.sleep(0.5)
    # value = 1 for 1º Semester
    # value = 2 for 2º Semester
    graduacao_select = Select(
        forms.find_element_by_name("cboSubG")).select_by_value("1")
    ano_select = Select(
        forms.find_element_by_name("cboAno")).select_by_visible_text("2019")
    # subject input
    disciplina_input = forms.find_element_by_name("txtDisciplina")
    disciplina_input.send_keys(_class["subject"])
    # class input
    turma_input = forms.find_element_by_name("txtTurma")
    turma_input.send_keys(_class["class"])
    # submit
    submit_button = forms.find_element_by_name("btnAcao")
    submit_button.click()
    # students list window
    time.sleep(0.3)
    forms_alunos = driver.find_element_by_name("FormConsultaPublica")
    # downloads the list as text file
    download = forms_alunos.find_element_by_xpath(
        "//input[@value='Salvar como texto']")
    download.click()
    time.sleep(0.5)
    # the driver is closed because if stays in the same window, the website will require a captcha
    driver.quit()


def get_students(base_url, path, driver_path):
    """
    Opens the .json that has classes data and iterates over it
    """
    classes_data = json_to_data(path)
    classes = classes_data["classes"]
    for _class in classes:
        try:
            get_students_class(_class)
        except NoSuchElementException as error:
            get_students_class(_class)


def clean_students_file(data):
    """
    Cleans the .txt file that has students data
    """
    aux_list1 = []
    for elem in data:
        aux_list1.append(elem.split("\r"))

    aux_list2 = []
    for elem in aux_list1:
        for elem2 in elem:
            aux_list2.append(elem2.split("\t"))

    students_list = []
    for elem in aux_list2:
        if len(elem) == 6:
            students_list.append(elem)

    return students_list


def read_txt_files(path, data):
    """
    Opens all .txt files that has classes data and create a list of students
    """
    classes_data = json_to_data(path)
    classes = classes_data["classes"]
    for _class in classes:
        with codecs.open(files_path + _class["subject"] + _class["class"] +
                         ".txt",
                         "r",
                         encoding="latin-1",
                         errors="ignore") as file:
            class_data = file.read().split("\n")

        students_list = clean_students_file(class_data)
        for student in students_list:
            stud_obj = {}
            stud_obj["ra"] = student[0].strip()
            stud_obj["name"] = student[1].strip()
            stud_obj["course"] = student[2].strip()
            stud_obj["classes"] = []
            class_obj = {}
            class_obj["subject"] = _class["subject"]
            class_obj["class"] = _class["class"]
            stud_obj["classes"].append(class_obj)
            data["students"].append(stud_obj)


def main():
    get_students(base_url, "classes/classes.json", driver_path)
    read_txt_files("classes/classes.json", data)
    data_to_json(data, "students/students.json")


main()
