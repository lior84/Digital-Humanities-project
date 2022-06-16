import requests
from bs4 import BeautifulSoup
import urllib.request


judgescv_url = "https://judgescv.court.gov.il"
judges_name_ref_dict = {}


def extract_judge(judges_li):
    name = judges_li.find_all('a')[0]['title']
    reference = judgescv_url + judges_li.find_all('a')[0]['href']
    judges_name_ref_dict[name] = reference

def extract_li():
    with open('judges_data.html', 'r') as f:
        contents = f.read()

        soup = BeautifulSoup(contents, 'html.parser')

        judges_ul = soup.find_all('ul', class_='animate-container list-unstyled remove-last-speace')

        judges_entries = list(judges_ul[0].find_all("li"))

        for judges_li in judges_entries:
            extract_judge(judges_li)


extract_li()
# print(judges_name_ref_dict)

for name, ref in zip(judges_name_ref_dict.keys(), judges_name_ref_dict.values()):
    page = requests.get(ref)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    break
    # print(ref)