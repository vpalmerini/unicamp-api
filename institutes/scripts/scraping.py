from selenium import webdriver
from api.utils import data_to_json

year = '2020'
graduation_level = 'G'
semester = '1'
url = 'https://www.dac.unicamp.br/portal/caderno-de-horarios/{}/{}/S/{}'.format(
    year, semester, graduation_level)
driver_path = '/usr/local/lib/chromedriver'

driver = webdriver.Chrome(driver_path)

data = {}
data["institutes"] = []


def get_institutes(url):
    """Get institutes objects and add them to data"""
    driver.get(url)
    institutes = driver.find_elements_by_class_name('item')

    for institute in institutes:
        obj = {}
        obj["initials"] = institute.find_element_by_tag_name('a').text.split(
            '\n')[0]
        obj["name"] = institute.find_element_by_tag_name('a').text.split(
            '\n')[-1]
        data["institutes"].append(obj)


def main():
    get_institutes(url)
    data_to_json(data, "institutes/institutes.json")


main()
driver.quit()
