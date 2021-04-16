import homework_03_classes as hw3
import MongoProcessing as mng
from copy import deepcopy
from pprint import pprint


# Superjob processing
main_url = 'https://www.superjob.ru'
db_name = 'sj_data'
collect_name = 'superjob'
expected_salary = 300000
filename_sj = 'hw_03_sj'

all_jobs = []

candidate_title = input('Please enter desirable vacancy title for search: \n')
if candidate_title is None or candidate_title == '':
    candidate_title = 'python'

endpoint = f'/vacancy/search/?keywords={candidate_title}&geo[c][0]=9'

db_handling = mng.MongoProcessing()
prcs = hw3.PageProcessing(main_url)
ss_page = prcs.get_page(endpoint)

while True:
    prcs.job_handling_sj(ss_page, all_jobs)
    next_page_link = None
    prcs.get_next_page_link(ss_page)
    if next_page_link is None:
        break
    ss_page = prcs.get_page(next_page_link)


db_handling.db_init(db_name)
db_handling.collection_init("sj")

all_jobs_new = deepcopy(all_jobs)
counter = db_handling.add_new_entries(all_jobs_new)

prcs.write_results(filename_sj, all_jobs)
print(prcs.dict_to_pandas())

db_handling.currency_converting()

job_list = db_handling.find_data_by_salary(expected_salary)
pprint(job_list)
print(len(job_list))