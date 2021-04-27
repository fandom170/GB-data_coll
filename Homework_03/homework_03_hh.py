"""1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные
вакансии в созданную БД.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта."""

import homework_03_classes as hw3
import MongoProcessing as mng
from copy import deepcopy
from pprint import pprint

# Headhunter processing

candidate_title = 'python'

all_jobs = []
main_url = 'https://hh.ru'
endpoint = f'/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&' \
           f'text={candidate_title}&showClusters=true'
filename_hh = 'hw_03_hh'
db_name = 'hh_data'
collect_name = 'headhunter'
expected_salary = 300000

prc = hw3.PageProcessing(main_url)
db_handling = mng.MongoProcessing()

db_handling.db_init(db_name)
db_handling.collection_init("hh")


s_page = prc.get_page(endpoint)

while True:
    prc.job_handling_hh(s_page, all_jobs)
    next_page_link = prc.get_next_page_link(s_page)

    if next_page_link is None:
        break
    s_page = prc.get_page(next_page_link)

all_jobs_new = deepcopy(all_jobs)
counter = db_handling.add_new_entries(all_jobs_new)
print(f"Inserting to MongoDB completed. {counter} new entries have been added.")

prc.write_results(filename_hh, all_jobs)
print(prc.dict_to_pandas())

db_handling.currency_converting()

job_list = db_handling.find_data_by_salary(expected_salary)
pprint(job_list)
print(len(job_list))


