import urllib.request
import requests
from bs4 import BeautifulSoup

judgescv_url = "https://www.verdicts.co.il/%d7%9e%d7%a9%d7%95%d7%91-%d7%94%d7%a9%d7%95%d7%a4%d7%98%d7%99%d7%9d/"
judges_name_ref_dict = {}
list_of_urls = []

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





URL = "https://www.verdicts.co.il/%d7%9e%d7%a9%d7%95%d7%91-%d7%94%d7%a9%d7%95%d7%a4%d7%98%d7%99%d7%9d/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

pages_holder = soup.find("div", class_="pagination-wrapper")
page_links = pages_holder.find_all("a", href=True)


results = soup.find(id="main-content")
job_elements = results.find_all("a", href=True)

for job_element in job_elements:
    if job_element['class'] != ["inactive"]:
        list_of_urls.append(job_element['href'])



for page_link in page_links:
    URL = page_link['href']
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="main-content")
    job_elements = results.find_all("a", href=True)

    for job_element in job_elements:
        if job_element['class'] != ["inactive"]:
            list_of_urls.append(job_element['href'])

print(list_of_urls)