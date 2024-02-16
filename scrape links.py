import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
import pandas as pd
import time


# request to gsmarena to extract link of brands- output: fpage_soup(bs4),error_status (boolean)
def request_to_gsmarena():
    try:
        response = requests.get(url_base, headers=headers, timeout=5)
        first_soup = BeautifulSoup(response.text, 'html.parser')
        error_status = False
        return error_status, first_soup
    except requests.exceptions.RequestException as error:
        error_status = True
        return error_status, error


# choose specific brands amonge all brands and extract their urls- output: brands_urls_list(list(urls)),error_status (boolean)
def filter_brands(fpage_soup):
    data = fpage_soup.find_all('div', class_='brandmenu-v2 light l-box clearfix')[0]
    data_href = data.find_all('a', class_='pad-multiple pad-allbrands')[0]['href']
    data_url = url_base + data_href
    try:
        response = requests.get(data_url, headers=headers, timeout=5)
        b_link_soup = BeautifulSoup(response.text, 'html.parser')
        all_brands = b_link_soup.find_all('div', class_='st-text')[0]
        goal_brands = ['alcatel', 'Apple', 'Asus', 'BLU', 'HTC', 'Huawei', 'Infinix', 'Lenovo', 'LG', 'Nokia', 'Sony',
                       'Xiaomi', 'ZTE', 'Samsung']
        brands_hrefs = all_brands.find_all('a')

        brands_urls_list = []
        for tag in brands_hrefs:
            brand_name = re.search(r'^([a-zA-Z ]+)', tag.text)[0]
            if brand_name in goal_brands:
                href = tag['href']
                brand_url = url_base + href
                brands_urls_list.append(brand_url)
        error_status = False
    except:
        error_status = True
    return brands_urls_list, error_status


# extract all links of each brand pages- output: brand_pages_url(dictionary{name:[urls,fsoup]}),error_brand_pages(list(urls)
def urls_pages_brands(phone_brands_urls, input_dict):
    error_brand_pages = []
    brand_pages_url = input_dict  # dictionary of brand name & urls of pages

    for url in phone_brands_urls:
        try:
            brand_info = re.findall(r'com/(.+)-phones-(.+)\.', url)
            brand_name = brand_info[0][0]
            brand_num = brand_info[0][1]

            time.sleep(1)
            response = requests.get(url, headers=headers, timeout=5)
            bpage_soup = BeautifulSoup(response.text, 'html.parser')
            # ---- extract number of pages for a brand
            brand_pages = bpage_soup.find_all('div', class_='nav-pages')[0]('a')
            nums_pages = brand_pages[-2].string
            # ---- extract pages of each brand
            pages_list = []
            for i in range(1, int(nums_pages) + 1):
                page_url = f'https://www.gsmarena.com/{brand_name}-phones-f-{brand_num}-0-p{i}.php'
                pages_list.append(page_url)
            brand_pages_url.update({brand_name: [pages_list, bpage_soup]})
        except requests.exceptions.RequestException as error:
            error_brand_pages.append(url)
            # print(error)
    return brand_pages_url, error_brand_pages


# extract all links of devices(phone,tablet,watch) for each brand- output:extracted_data
# (list[name:['type',url]],url_error_dict(dictionary{name:[url]}),error_status(boolean)
def extract_categorize_urls(brand_pages_url, input_list, error_dict, error_status):
    extracted_data = input_list
    url_error_dict = {}

    # extract urls of devices in each page
    def links(soup, devices_url_list, name):
        devices = soup.find_all('div', class_='makers')[0]
        devices_links = devices.find_all('li')
        for each in devices_links:
            info = each.img['title']
            info_l = info.lower()
            if ('announce' in info_l) and (not ' announced yet' in info_l):
                announced_y = (int(re.findall(r'Announced .* (\d+)\. ', info)[0]))
                if announced_y >= 2010:
                    url = each.a['href'].replace('(', '').replace(')', '')
                    link = f'https://www.gsmarena.com/+{url}'
                    if 'phone' in info_l:
                        devices_url_list.append([name, 'phone', link])
                    elif 'tablet' in info_l:
                        devices_url_list.append([name, 'tablet', link])
                    elif 'watch' in info_l:
                        devices_url_list.append([name, 'watch', link])
        return devices_url_list

    if not error_status:
        brands_name = list(brand_pages_url.keys())
        all_urls = list(brand_pages_url.values())
    else:
        brands_name = list(error_dict.keys())
        all_urls = list(error_dict.values())

    for key, value in zip(brands_name, all_urls):
        b_name = key
        URLs_SOUPs = value
        url_error = []

        for i in range(len(URLs_SOUPs[0])):

            if i == 0 and error_status == False:
                page_soup = URLs_SOUPs[1]
                devices_url_list = links(page_soup, extracted_data, name = b_name)
            else:
                try:
                    time.sleep(1)
                    response_p = requests.get(URLs_SOUPs[0][i], headers = headers, timeout=5)
                    page_soup = BeautifulSoup(response_p.text, 'html.parser')
                    if not error_status:
                        devices_url_list = links(page_soup, devices_url_list, name = b_name)
                    else:
                        devices_url_list = links(page_soup, extracted_data, name = b_name)
                except requests.exceptions.RequestException as error1:
                    print(error1, '\n', b_name, '\n', URLs_SOUPs[0][i])
                    url_error.append(URLs_SOUPs[0][i])
        if len(url_error) != 0:
            error_status = True
            url_error_dict.update({b_name: [url_error]})

        else:
            error_status = False
        extracted_data = devices_url_list
    return extracted_data, url_error_dict, error_status


# save data as csv file
def to_df_to_csv(data):
    data_df = pd.DataFrame(data, columns = ['Brand', 'Device Category', 'Link'])
    data_df.to_csv('AllLinks.csv', index = False)


# --------------------initial settings------------------------------
UA = UserAgent(browsers = ["chrome", "firefox", "safari"], os = ["windows"])
headers = {'User-Agent': UA.random, 'Accept-Language': 'en-US,en,q=0.5'}
url_base = 'https://www.gsmarena.com/'

# -------------------------------main----------------------------------

status, output = request_to_gsmarena()

if not status:
    fpage_soup = output
    phone_brands_urls, filtering_status = filter_brands(fpage_soup)
    while (filtering_status):
        phone_brands_urls, filtering_status = filter_brands(fpage_soup)

    pages_urls, remain_brands = urls_pages_brands(phone_brands_urls, input_dict = {})
    brand_pages_status = len(remain_brands)
    while (brand_pages_status != 0):
        pages_urls, remain_brands = urls_pages_brands(phone_brands_urls = remain_brands, input_dict = pages_urls)
        brand_pages_status = len(remain_brands)

    extracted_links, remain_urls_dict, extract_status = extract_categorize_urls(pages_urls, input_list = [],
                                                                                error_dict = {}, error_status = False)
    while (extract_status):
        extracted_links, remain_urls_dict, extract_status = extract_categorize_urls(pages_urls,
                                                                                    input_list = extracted_links,
                                                                                    error_dict = remain_urls_dict,
                                                                                    error_status = extract_status)

    to_df_to_csv(extracted_links)
    print('Done!')
else:
    error = output
    print(error)
