import json
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

class PageProcessing():
    def __init__(self, main_link):
        self.main_link = main_link
        self.headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/89.0.4389.90 Safari/537.36 OPR/75.0.3969.149'}
        self.all_jobs = None

    def job_handling_hh(self, s_page, all_jobs):
        """Functions that graps and parse jobs from the page and put data to general dictionary"""
        site_name = 'headhunter.ru'
        job_list = s_page.find_all('div', {'class': 'vacancy-serp-item__row_header'})

        for elem in job_list:
            job_data = {}
            job_title = elem.find('span', {'class': 'g-user-content'})
            job_name = job_title.findChildren()[0].getText()
            job_link = job_title.find('a')['href']
            job_salary_block = elem.find('div', {'class': 'vacancy-serp-item__sidebar'})

            min_salary, max_salary, currency = self.salary_processing_hh(job_salary_block)

            job_data['title'] = job_name
            job_data['min_salary'] = min_salary
            job_data['max_salary'] = max_salary
            job_data['currency'] = currency
            job_data['link'] = job_link
            # job_data['site_name'] = site_name
            #print(job_data)
            all_jobs.append(job_data)

    def get_page(self, endpoint):
        """Function that get page and transform it to soup html structure"""
        url = self.main_link + endpoint
        page = requests.get(url=url, headers=self.headers)
        return bs(page.content, features='lxml')

    def get_next_page_link(self, s_page):
        """Function that returns link for the next page ig it exists. Otherwise return None"""
        try:
            next_page_link = s_page.find('a', {'class': 'bloko-button', 'data-qa': 'pager-next'})['href']
            return next_page_link
        except (TypeError):
            return None

    def salary_processing_hh(self, job_salary_block):
        """Recognizing of salary value for job vacancies for head hunter site"""
        if job_salary_block is None:
            return None, None, None

        job_salary = job_salary_block.findChildren()[0] \
            .getText() \
            .replace('\u202f', '') \
            .strip() \
            .split(' ')

        if len(job_salary) == 4:
            min_salary = job_salary[0]
            max_salary = job_salary[2]
        elif job_salary[0].rstrip() == 'от':
            min_salary = job_salary[1]
            max_salary = None
        elif job_salary[0].rstrip() == 'до':
            min_salary = None
            max_salary = job_salary[1]
        else:
            return None, None, None

        return min_salary, max_salary, job_salary[-1]

    def write_results(self, filename, all_jobs):
        self.all_jobs = all_jobs
        result = json.dumps(all_jobs, indent=4, ensure_ascii=False)
        file = filename + '.json'
        with open(file, 'w', encoding='utf-8') as fw:
            fw.write(result)

    def dict_to_pandas(self):
        return pd.DataFrame.from_dict(self.all_jobs).to_string()


    def job_handling_sj(self, s_page, all_jobs):
        site_name = 'superjob.ru'
        """Functions that graps and parse jobs from the page and put data to general dictionary"""
        job_list = s_page.find_all('div', {'class': 'f-test-vacancy-item'})
        for elem in job_list:
            job_data = {}
            job_title = elem.find_all('div', {'class': 'PlM3e'})[0]
            job_name = job_title.findChildren()[0].getText()
            job_link = self.main_link + job_title.findChildren()[0]['href']

            job_salary_block = elem.find('span', {'class': 'f-test-text-company-item-salary'})
            min_salary, max_salary, currency = self.salary_processing_sj(job_salary_block)

            job_data['title'] = job_name
            job_data['min_salary'] = min_salary
            job_data['max_salary'] = max_salary
            job_data['currency'] = currency
            job_data['link'] = job_link
            job_data['site_name'] = site_name
            #print(job_data)
            all_jobs.append(job_data)

    def salary_processing_sj(self, job_salary_block):
        """Recognizing of salary value for job vacancies for head hunter site"""
        job_salary_block = job_salary_block.find('span', {'class': '_2JVkc'})
        if job_salary_block is None:
            return None, None, None


        job_salary = job_salary_block.getText()
        job_salary = re.sub(r'\d\xa0\d', '00', job_salary)
        job_salary = job_salary.strip().split('\xa0')

        if len(job_salary) == 4:
            min_salary = job_salary[0]
            max_salary = job_salary[2]
        elif job_salary[0].rstrip() == 'от':
            min_salary = job_salary[1]
            max_salary = None
        elif job_salary[0].rstrip() == 'до':
            min_salary = None
            max_salary = job_salary[1]
        else:
            return None, None, None

        return min_salary, max_salary, job_salary[-1]