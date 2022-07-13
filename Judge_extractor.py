import json
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
    served_in_army = False
    start_year_of_military = ""
    end_year_of_military = ""
    graduation_year = ""
    intern_start = ""
    intern_end = ""
    year_of_certification = ""
    job_history = ""
    page_reference = ""


list_of_urls = []
judges_list = []

url_file = open('urls.txt', 'r')
Lines = url_file.readlines()

for line in Lines:
    list_of_urls.append(line.strip())

for URL in list_of_urls:
    try:
        page = requests.get(URL)
    except:
        print("No url: ", URL)
        continue
    soup = BeautifulSoup(page.content, "html.parser")
    liat = JudgeInfo()
    judges_entry = soup.find(id="article_body")

    # region first and last names and role extraction
    english_full_name = ""
    hebrew_full_name = ""
    try:
        h1 = judges_entry.find("h1")
    except:
        print("Empty? ", URL)
        continue

    names = h1.text.split('|')

    for ch in names[0]:
        if ch != '\n' and ch != '\t':
            hebrew_full_name += ch
    for ch in names[1]:
        if ch != '\n' and ch != '\t':
            english_full_name += ch

    liat.page_reference = URL
    liat.role_type = hebrew_full_name.split()[0][1:]
    hebrew_full_name = hebrew_full_name.split(' ')[1:]
    hebrew_full_name = " ".join(hebrew_full_name)
    liat.hebrew_first_name = hebrew_full_name.split()[0]
    liat.last_name_in_hebrew = hebrew_full_name.split()[1]
    liat.first_name_in_english = english_full_name.split()[0]
    liat.last_name_in_english = english_full_name.split()[1]
    # endregion

    # region role description extracting
    try:
        role_description = judges_entry.find("strong")
        liat.role_description = role_description.text
    except:
        print("No strong element? ", URL)
    # endregion


    # region data extracting

    try:
        judge_data = soup.find("p")
        data_lines = judge_data.text.split('\n')
    except:
        print("no data data judge? ", URL)

    try:
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
    except:
        print("No gender? ", URL)

    try:
        # region birth year extracting
        liat.year_of_birth = birth_text[2]
        # endregion
    except:
        liat.year_of_birth = ""

    try:
        # region birth country extracting
        liat.country_of_birth = birth_text[3][1:]
        # endregion
    except:
        try:
            liat.country_of_birth = birth_text[1][1:]
        except:
            print("No country birth? ", URL)

    try:
        data_lines = data_lines[1:]
    except:
        print("No data lines? ", URL)

    got_certified = False

    liat.served_in_army = False
    liat.start_year_of_military = ""
    liat.end_year_of_military = ""
    liat.graduation_year = ""
    liat.intern_start = ""
    liat.intern_end = ""
    liat.year_of_certification = ""
    liat.job_history = ""
    for data_line in data_lines:
        if got_certified:
            liat.job_history += data_line
        elif data_line.__contains__("שירת"):
            # region Army extract
            liat.served_in_army = True
            splitted_line = data_line.split()
            years = []
            for value in splitted_line:
                if value.isnumeric():
                    years.append(value)
            try:
                liat.start_year_of_military = years[0]
                liat.end_year_of_military = years[1]
            except:
                splitted_army = data_line.split("-")
                for army_line in splitted_army:
                    for value in army_line.split():
                        if value.isnumeric():
                            years.append(value)
                try:
                    liat.start_year_of_military = years[0]
                    liat.end_year_of_military = years[1]
                except:
                    print("No army? ", URL)
                    continue
            # endregion
        elif data_line.__contains__("תואר ראשון"):
            # region Graduation extract
            splitted_line = data_line.split()
            for value in splitted_line:
                if value.isnumeric():
                    liat.graduation_year = value
            # endregion
        elif data_line.__contains__("התמחה") or data_line.__contains__("התמחתה"):
            # region internship extract
            years = []
            splitted_line = data_line.split()
            for value in splitted_line:
                if value.isnumeric():
                    years.append(value)

            try:
                liat.intern_start = years[0]
                liat.intern_end = years[1]
            except:
                splitted_intern = data_line.split("-")
                for inter_line in splitted_intern:
                    for value in inter_line.split():
                        if value.isnumeric():
                            years.append(value)
                try:
                    liat.intern_start = years[0]
                    liat.intern_end = years[1]
                except:
                    print("No intern? ", URL)
                    continue
            # endregion
        elif data_line.__contains__("הוסמכה") or data_line.__contains__("הוסמך"):
            # region internship extract
            years = []
            splitted_line = data_line.split()
            for value in splitted_line:
                if value.isnumeric():
                    liat.year_of_certification = value
                    got_certified = True
                    break
            # endregion

    # endregion

    judges_list.append(liat)

# Writing to judges.json
with open("judges.json", "w") as outfile:
    json_string = json.dumps([ob.__dict__ for ob in judges_list], ensure_ascii=False)
    outfile.write(json_string)

# print(jsonstr)
