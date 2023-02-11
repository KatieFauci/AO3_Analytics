from tkinter import ROUND
from urllib import response
import bs4
from datetime import datetime
from math import floor
import requests
import time
from bs4 import BeautifulSoup as bs


def print_work_data(work):
    print('TITLE: ' + work.title)
    print('AUTHOR: ' + work.author)
    print('WORDS: ' + str(work.word_count))
    print('LAST VISITED: ' + str(work.last_visited))
    print('TAGS: ' + str(work.tags))
    print('\n-------------------\n')

def print_user_data(user):
    print('\nTotal Works Read: ' + str(user.story_count))
    print('Total Words Read: ' + str(user.total_words))
    print('Total Pages Read: ' + str(user.page_count))
    #for key in user.tag_stats:
    #    print(key + ': ' + str(user.tag_stats.get(key)))

def get_title(work):
     temp = work.find_all('div', class_='header module')[0].find_all('h4')[0].find_all('a')
     return temp[0].get_text()

def get_author(work):
    temp = work.find_all('div', class_='header module')[0].find_all('h4')[0].find_all('a')
    try:
        return temp[1].get_text()
    except:
        return 'Anonymous'

def get_work_tags(entry):
    tag_list = entry.find('ul', class_='tags commas').find_all('li')
    parsed_tags = []
    for tag in tag_list:
        tag_info = [tag.a.get_text()]
        tag_info.append(tag['class'].pop())
        #tag_info = [tag['class'].pop()]
        #tag_info.append(tag.a.get_text())
        if tag_info[0] != 'Show warnings':
            parsed_tags.append(tag_info)
    return parsed_tags
    #print(entry.find('ul', class_='tags commas').find_all('li'))

def compile_user_tags(user):
    tag_stats = {}
    for work in user.works:
        for tag in work.tags:
            if tag[0] in tag_stats:
                # increment count
                tag_stats[tag[0]] = tag_stats.get(tag[0]) + 1;
            else: 
                tag_stats[tag[0]] = 1

    return tag_stats

def get_work_word_count(work):
    return int(work.dl.dd.next_sibling.next_sibling.next_sibling.next_sibling.get_text().replace(',', ''))

def last_visited_date(work):
    date_str = work.find('div', class_='user module group').h4.get_text().split(':')[1].split('\n')[0].strip(' ')
    return datetime.strptime(date_str, '%d %b %Y')

def get_page_count(word_count):
    return floor(word_count/300)

def call_history():
    
    pages = []

    cookies = {
        'flash_is_set': '1',
        'user_credentials': '1',
        '_otwarchive_session': 'b%2BBPKgpFGK7ncmlJF7BBMK16zyvrQZMuqRYKNcgt1xXIK9UhfsJLnkRafFEBXxI8kJMp6OVDMG9kgcen1lpoESFyj4KWcnjPIRb7xXeRqgQ5EpC%2FwQSfT65%2FAIRSfZNuB9GIFkSZ7l3Inz6GfJdTlsNffQsC0QLDeKKbVDW3O%2FzOwFgfQiU2mC%2BaY5EgOrhGv%2BRfBKKoZgGgulK2nQGKVA2HmttL2Jjzhu54FpJJmagsDMuWWYpBIKlbcyzgS2fDJAKnXH%2BUfPseX6SDv10I0xPE2x2tz9DUVSUJh%2FNtr9L7nb1HYDRX33gfLLPxfrddQnNIs9PGDM%2B%2FhQQLqTboNYumfJDBxeNweEN8zq61SsKbIpj%2FHZsjzkfeZfQnSU%2BhPlAEsLDzHkF3wfieXiBfnEJAo3glpd11qm1XZ%2B8OTvzh9hvKQAjE6ajyihKtdCnEAJIRt1%2FyXs6NCy1zc438x8afIy8R%2FWbexLFyiyoyT6jVHVqFQnxj5hR%2B%2FROOVlQrZShLZDg3u8kcWvwFWS6UdBNkbR0KMDMP%2BJzpA9CXA4QntuJUS%2Bv%2FnpnDabiE--zEkY27bbgLXV9av1--RHRayuMFttAEaP7cmfzgXQ%3D%3D',
     }

    headers = {
        'authority': 'archiveofourown.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'flash_is_set=1; user_credentials=1; _otwarchive_session=b%2BBPKgpFGK7ncmlJF7BBMK16zyvrQZMuqRYKNcgt1xXIK9UhfsJLnkRafFEBXxI8kJMp6OVDMG9kgcen1lpoESFyj4KWcnjPIRb7xXeRqgQ5EpC%2FwQSfT65%2FAIRSfZNuB9GIFkSZ7l3Inz6GfJdTlsNffQsC0QLDeKKbVDW3O%2FzOwFgfQiU2mC%2BaY5EgOrhGv%2BRfBKKoZgGgulK2nQGKVA2HmttL2Jjzhu54FpJJmagsDMuWWYpBIKlbcyzgS2fDJAKnXH%2BUfPseX6SDv10I0xPE2x2tz9DUVSUJh%2FNtr9L7nb1HYDRX33gfLLPxfrddQnNIs9PGDM%2B%2FhQQLqTboNYumfJDBxeNweEN8zq61SsKbIpj%2FHZsjzkfeZfQnSU%2BhPlAEsLDzHkF3wfieXiBfnEJAo3glpd11qm1XZ%2B8OTvzh9hvKQAjE6ajyihKtdCnEAJIRt1%2FyXs6NCy1zc438x8afIy8R%2FWbexLFyiyoyT6jVHVqFQnxj5hR%2B%2FROOVlQrZShLZDg3u8kcWvwFWS6UdBNkbR0KMDMP%2BJzpA9CXA4QntuJUS%2Bv%2FnpnDabiE--zEkY27bbgLXV9av1--RHRayuMFttAEaP7cmfzgXQ%3D%3D',
        'referer': 'https://archiveofourown.org/users/login',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    url = 'https://archiveofourown.org/users/WrongfulRuffian/readings'
    print('GETTING PAGE >> 1')
    first_request = requests.get(url, cookies=cookies, headers=headers)

    pages.append(first_request)

    # https://archiveofourown.org/users/WrongfulRuffian/readings
    # https://archiveofourown.org/users/WrongfulRuffian/readings?page=2

    page_num = 2
    print('PAGE NUM SET TO ' + str(page_num))
    while True:
        print('IN WHILE')
        try:
            print('IN TRY')
            time.sleep(1)
            print('GETTING PAGE >> ' + str(page_num))
            this_url = url + '?page=' + str(page_num)
            print('URL: ' + this_url)
            pages.append(requests.get(this_url, cookies=cookies, headers=headers))
            page_num += 1
            if page_num == 11:
                print('BREAK' + page_num)
        except:
            print('IN EXCEPT')
            return pages

def call_history_v2(USERNAME, PASSWORD):
    pages = []
    history_url = f'https://archiveofourown.org/users/{USERNAME}/readings'
    login_url = 'https://archiveofourown.org/users/login'

    sess = requests.Session()

    req = sess.get('https://archiveofourown.org')
    soup = bs(req.text, features='html.parser')
    authenticity_token = soup.find('input', {'name': 'authenticity_token'})['value']

    # Log in to AO3
    login_request = sess.post(login_url, params={
        'authenticity_token': authenticity_token,
        'user[login]': USERNAME,
        'user[password]': PASSWORD,
    })

    # Check if login Successful
    if ("The password or user name you entered doesn't match our records" in login_request.text):
        print('INVALID LOGIN')
        return 0
    

    # Fetch my private reading history
    first_request = sess.get(history_url)
    pages.append(first_request)
    
    page_num = 2
    while True:
        try:
            time.sleep(1)
            print('GETTING PAGE >> ' + str(page_num))
            this_url = history_url + '?page=' + str(page_num)
            print('URL: ' + this_url)
            pages.append(sess.get(this_url))
            page_num += 1
            if page_num == 6:
                print('BREAK' + page_num)
        except:
            print('IN EXCEPT')
            return pages
