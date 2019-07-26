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
            obj["institute"] = institute.text.split("-")[-1]
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


def main():
    get_courses()
    data_to_json(data)


main()
driver.quit()
