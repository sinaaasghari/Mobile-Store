import requests
from bs4 import BeautifulSoup
import random
import time
import pandas as pd

import concurrent.futures

directory = '.'
links = pd.read_csv('AllLinks.csv')
links['Index'] = links.index

def record_mobile_features(url):

    url_idx = url['Index'].tolist()[0]
    url = url['Link'].tolist()[0]

    headers = {'User-Agent': 'Chrome/120.0.0.0', 'Accept-Language': 'en-US'}

    state = False
    while not state:
        state = True
        try:
            time.sleep(random.randint(10, 15))
            page = requests.get(url, headers=headers, timeout=5)
        except Exception as e:
            print(e)
            state = False
    
    soup = BeautifulSoup(page.content, 'html.parser')

    details = soup.find_all(id = 'specs-list')
    parts = details[0].find_all('table')


    sections_set = {}
    num_section = len(parts)

    product_name = soup.find_all('title')[0].text.strip()
    sections_set['Name'] = {'Name':[product_name]}

    for sec_idx in range(num_section):
        section_name = parts[sec_idx].find_all('th')[0].text.strip()

        sub_section = parts[sec_idx].find_all('tr')

        num_sub_section = len(sub_section)
        sub_sections_set = {}
        for sub_sec_idx in range(num_sub_section):
            try:
                name_sub_section = sub_section[sub_sec_idx].find_all('td')[0].text.strip()

                if len(name_sub_section) == 0:
                    name_sub_section = f'{section_name}_Extra'
                else:
                    name_sub_section = f'{section_name}_{name_sub_section}'
                sub_sections_set[name_sub_section] = sub_section[sub_sec_idx].find_all('td')[1].text.strip()
            except Exception as e:
                print(e)
                continue
        
        sections_set[section_name] = sub_sections_set
    
    record = {}
    for d in sections_set.values():
        record.update(d)

    record['Index'] = url_idx
    print(f'Index {url_idx} recoreded.')
    
    return record

# def make_dataset(links, file_path):

#     loop_threshold = 10
#     num_loop = 1

#     first_idx = links.index.tolist()[0]
#     last_idx = links.index.tolist()[-1]

#     records = pd.DataFrame()

#     for idx in range(first_idx, last_idx+1):
#         url = links['Link'][idx]

#         while num_loop < loop_threshold:
#             try:
#                 mobile_info = record_mobile_features(url)
#                 records = pd.concat([records, pd.DataFrame(mobile_info)])
#                 print(f'url index {idx} recorded.')
#                 num_loop = 1
#                 break

#             except Exception as e:
#                 print(e)
#                 num_loop += 1
#                 records.sort_index(axis = 1).to_csv(file_path, index=False)
#                 continue
    
#     records.sort_index(axis = 1).to_csv(file_path, index=False)
#     return records

def scrape_all_links(urls):

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        futures = [executor.submit(record_mobile_features, urls.loc[urls['Index']==idx, :]) for idx in urls['Index']]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(pd.DataFrame(result))
        
        result_df = pd.concat(results)
    
    return result_df

indices = [(0,1000), (1000,2000), (2000,3000), (3000,links.shape[0])]
for i in range(len(indices)):
    urls = links.iloc[indices[i][0]:indices[i][1],:]
    result_df = scrape_all_links(urls)

    pd.merge(result_df, urls, on='Index').to_csv(f'Results_WithLinks_Part{i+1}.csv', index=False)


df1 = pd.read_csv('./Scrape/Results_WithLinks_Part1.csv')
df2 = pd.read_csv('./Scrape/Results_WithLinks_Part2.csv')
df3 = pd.read_csv('./Scrape/Results_WithLinks_Part3.csv')
df4 = pd.read_csv('./Scrape/Results_WithLinks_Part4.csv')

df_final = pd.concat([df1, df2, df3, df4])
df_final.sort_values('Index').to_csv('./Scrape/Scraped_DataSet.csv')