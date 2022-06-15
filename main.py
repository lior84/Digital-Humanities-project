from bs4 import BeautifulSoup

judgescv_url = "https://judgescv.court.gov.il"
judges_name_ref_dict = {}


class JudgesExtractor():

    def extract_judge(self, judges_li):
        name = judges_li.find_all('a')[0]['title']
        reference = judgescv_url + judges_li.find_all('a')[0]['href']
        judges_name_ref_dict[name] = reference

    def extract_li(self):
        with open('judges_data.html', 'r') as f:
            contents = f.read()

            soup = BeautifulSoup(contents, 'html.parser')

            judges_ul = soup.find_all('ul', class_='animate-container list-unstyled remove-last-speace')

            judges_entries = list(judges_ul[0].find_all("li"))

            for judges_li in judges_entries:
                self.extract_judge(judges_li)


obj = JudgesExtractor()
obj.extract_li()
print(judges_name_ref_dict)
