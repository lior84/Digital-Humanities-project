import requests
from bs4 import BeautifulSoup


class JudgeInfo:
    first_name_in_hebrew = ""
    last_name_in_hebrew = ""
    first_name_in_english = ""
    last_name_in_english = ""
    gender = ""
    year_of_birth = ""
    country_of_birth = ""
    role_description = ""
    role_type = ""

    served_in_army: bool
    start_year_of_military = ""
    end_year_of_military = ""

    graduation_year = ""
    appendix = []


list_of_urls = []

URL = "https://www.verdicts.co.il/judge/%D7%94%D7%A9%D7%95%D7%A4%D7%98%D7%AA-%D7%9C%D7%99%D7%90%D7%AA-%D7%99%D7%A8%D7%95%D7%9F/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

liat = JudgeInfo()

judges_entry = soup.find(id="article_body")

# region first and last names and role extraction
english_full_name = ""
hebrew_full_name = ""
h1 = judges_entry.find("h1")
names = h1.text.split('|')

for ch in names[0]:
    if ch != '\n' and ch != '\t':
        hebrew_full_name += ch
for ch in names[1]:
    if ch != '\n' and ch != '\t':
        english_full_name += ch

liat.role_type = hebrew_full_name.split()[0][1:]
hebrew_full_name = hebrew_full_name.split(' ')[1:]
hebrew_full_name = " ".join(hebrew_full_name)

liat.hebrew_first_name = hebrew_full_name.split()[0]
liat.last_name_in_hebrew = hebrew_full_name.split()[1]
liat.first_name_in_english = english_full_name.split()[0]
liat.last_name_in_english = english_full_name.split()[1]
# endregion

# region role description extracting
role_description = judges_entry.find("strong")
liat.role_description = role_description.text
# endregion

# region data extracting
judge_data = soup.find("p")
data_lines = judge_data.text.split('\n')

birth_text = data_lines[0]
birth_text = birth_text.split(' ')

# region gender extractor
if birth_text[0] == "נולדה":
    liat.gender = "Female"
elif birth_text[0] == "נולד":
    liat.gender = "Male"
else:
    liat.gender = "Error_gender"
# endregion

# region birth year extracting
liat.year_of_birth = birth_text[2]
# endregion

# region birth country extracting
liat.country_of_birth = birth_text[3][1:]
# endregion

data_lines = data_lines[1:]

for data_line in data_lines:
    if data_line.__contains__("שירת"):
        # region Army extract
        liat.served_in_army = True
        splitted_line = data_line.split()
        years = []
        for value in splitted_line:
            if value.isnumeric():
                years.append(value)
        liat.start_year_of_military = years[0]
        liat.end_year_of_military = years[1]
        # endregion
    elif data_line.__contains__("תואר ראשון"):
        # region Graduation extract
        splitted_line = data_line.split()
        for value in splitted_line:
            if value.isnumeric():
                liat.graduation_year = value
        # endregion

# endregion
