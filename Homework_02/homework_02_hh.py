import homework_02_classes as hw2

# Headhunter processing

candidate_title = 'python'

all_jobs = []
main_url = 'https://hh.ru'
endpoint = f'/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&' \
           f'text={candidate_title}&showClusters=true'
filename_hh = 'hw_02_hh'

prc = hw2.PageProcessing(main_url)
s_page = prc.get_page(endpoint)

while True:
    prc.job_handling_hh(s_page, all_jobs)
    next_page_link = prc.get_next_page_link(s_page)
    if next_page_link is None:
        break
    s_page = prc.get_page(next_page_link)


prc.write_results(filename_hh, all_jobs)
print(prc.dict_to_pandas())
