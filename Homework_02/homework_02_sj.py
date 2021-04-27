import homework_02_classes as hw2



# Superjob processing
main_url = 'https://www.superjob.ru'

candidate_title = input('Please enter desirable vacancy title for search: \n')
if candidate_title is None or candidate_title == '':
    candidate_title = 'developer'


endpoint = f'/vacancy/search/?keywords={candidate_title}'
filename_sj = 'hw_02_sj'
all_jobs = []

prcs = hw2.PageProcessing(main_url)
ss_page = prcs.get_page(endpoint)

while True:
    prcs.job_handling_sj(ss_page, all_jobs)
    next_page_link = None
    #prcs.get_next_page_link(ss_page)
    if next_page_link is None:
        break
    #ss_page = prcs.get_page(next_page_link)

prcs.write_results(filename_sj, all_jobs)
print(prcs.dict_to_pandas())