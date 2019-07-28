import json
from selenium import webdriver

main_url = "https://www.dac.unicamp.br/portal/graduacao/cursos"
driver_path = '/usr/local/lib/chromedriver'

driver = webdriver.Chrome(driver_path)
driver.get(main_url)

data = {}
data["courses"] = []

container = driver.find_element_by_id("conteudo")


def get_courses():
    divs = container.find_elements_by_class_name("table-responsive")
    institutes = container.find_elements_by_tag_name('p')[2:]
    for table, institute in zip(divs, institutes):
        courses = table.find_elements_by_tag_name('tr')[1:]
        i = 0
        while i < len(courses):
            rows = courses[i].find_elements_by_tag_name('td')
            obj = {}
            obj["institute"] = institute.text.split("-")[-1].strip()
            obj["id"] = rows[0].text
            obj["name"] = rows[1].text
            obj["shift"] = rows[2].text
            obj["specializations"] = []
            if len(rows) == 3:
                next_tr = courses[i].find_element_by_xpath(
                    "following-sibling::tr")
                next_tds = next_tr.find_elements_by_tag_name('td')
                i += 1
                while (len(next_tds) == 2):
                    spec_obj = {}
                    spec_obj["code"] = next_tds[0].text
                    spec_obj["specialization"] = next_tds[1].text
                    obj["specializations"].append(spec_obj)
                    i += 1
                    try:
                        next_tr = next_tr.find_element_by_xpath(
                            "following-sibling::tr")
                        next_tds = next_tr.find_elements_by_tag_name('td')
                    except:
                        break
            else:
                obj["specializations"].append({
                    "code":
                    rows[3].text.strip('-'),
                    "specialization":
                    rows[4].text.strip('-')
                })
                i += 1
            data["courses"].append(obj)


def data_to_json(data):
    """Store all data in a .json file"""
    with open("courses.json", "w") as file:
        json.dump(data, file, ensure_ascii=False)


def merge_specializations(data, duplicated_courses, id):
    specializations = []
    for course in data["courses"]:
        if course["id"] == id:
            # specializations.append(course["specializations"])
            for specialization in course["specializations"]:
                specializations.append(specialization)
    return specializations


def handle_duplicated_courses(data):
    courses = data["courses"]
    ids = []
    for course in courses:
        ids.append(course["id"])

    i = 0
    while i < len(ids):
        duplicated_courses = []
        if ids.count(ids[i]) > 1:
            j = 0
            while j < len(courses):
                if courses[j]["id"] == ids[i]:
                    duplicated_courses.append(courses[j])
                j += 1
            j = 0
            while j < len(courses):
                if courses[j]["id"] == duplicated_courses[0]["id"]:
                    courses[j]["specializations"] = merge_specializations(
                        data, duplicated_courses, courses[j]["id"])
                    k = j + 1
                    while k < len(courses):
                        if courses[k]["id"] == courses[j]["id"]:
                            del courses[k]
                        k += 1
                j += 1
            ids = [value for value in ids if value != ids[i]]
        i += 1


def main():
    get_courses()
    handle_duplicated_courses(data)
    data_to_json(data)


main()
driver.quit()
