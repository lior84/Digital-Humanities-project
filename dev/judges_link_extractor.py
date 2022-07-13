import requests
from bs4 import BeautifulSoup

page_counter = 1
list_of_urls = []

URL = "https://www.verdicts.co.il/%d7%9e%d7%a9%d7%95%d7%91-%d7%94%d7%a9%d7%95%d7%a4%d7%98%d7%99%d7%9d/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

page_numbers = soup.find("div", class_="pagination-wrapper")
page_links = page_numbers.find_all("a", href=True)

judges_entries = soup.find(id="main-content")
judges_links = judges_entries.find_all("a", href=True)

for judge_link in judges_links:
    if judge_link['class'] != ["inactive"]:
        judge_name = judge_link['title'].strip()
        list_of_urls.append([judge_link['href'], page_counter, judge_name])


for page_link in page_links:
    page_counter += 1
    URL = page_link['href']
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    judges_entries = soup.find(id="main-content")
    job_elements = judges_entries.find_all("a", href=True)

    for job_element in job_elements:
        if job_element['class'] != ["inactive"]:
            judge_name = job_element['title'].strip()
            list_of_urls.append([job_element['href'], page_counter, judge_name])

with open(r'urls.txt', 'w') as fp:
    list_of_urls.sort()
    for url in list_of_urls:
        # write each item on a new line
        fp.write("%s\n" % url)

