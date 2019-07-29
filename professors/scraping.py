# import json
# from selenium import webdriver

# main_url = "https://www.dac.unicamp.br/portal/graduacao/cursos"
# driver_path = '/usr/local/lib/chromedriver'

# driver = webdriver.Chrome(driver_path)
# driver.get(main_url)

# data = {}
# data["professors"] = []

# def json_to_data(path):
#     """Open .json file with scraped data"""
#     with open(path, "r") as file:
#         return json.load(file)

# def get_professors():
#     classes = json_to_data("../classes/classes.json")
#     for _class in classes:
