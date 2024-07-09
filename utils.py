from tkinter import ROUND
from urllib import response
import bs4
from datetime import datetime
from math import floor
import requests
import time
from bs4 import BeautifulSoup as bs
import eel
import json
import sqlite3
import metrics

db_name = 'works.db'


def print_work_data(work):
    print_out('TITLE: ' + work.title)
    print_out('AUTHOR: ' + work.author)
    print_out('WORDS: ' + str(work.word_count))
    print_out('LAST VISITED: ' + str(work.last_visited))
    print_out('TAGS: ' + str(work.tags))
    print_out('\n-------------------\n')

def print_user_data(user):
    print_out('\nTotal Works Read: ' + str(user.story_count))
    print_out('Total Words Read: ' + str(user.total_words))
    print_out('Total Pages Read: ' + str(user.page_count))
    #for key in user.tag_stats:
    #    print(key + ': ' + str(user.tag_stats.get(key)))

def store_user_data(user):
    dictionary = {
        "WorksRead": user.story_count,
        "WordsRead": user.total_words,
        "PagesRead": user.page_count, 
    }

    json_object = json.dumps(dictionary, indent=4)

    with open("Scrape_Results/user_data.json", "w") as outfile:
        outfile.write(json_object)

def get_title(work):
     temp = work.find_all('div', class_='header module')[0].find_all('h4')[0].find_all('a')
     return temp[0].get_text()

def get_author(work):
    temp = work.find_all('div', class_='header module')[0].find_all('h4')[0].find_all('a')
    try:
        return temp[1].get_text()
    except:
        return 'Anonymous'
    
def get_rating(work):
    temp = work.find_all('ul', class_='required-tags')[0].find_all('li')[0].find_all('span', class_='text')
    try: 
        return temp[0].get_text()
    except:
        return 'Rating Not Found'
    
def get_language(work):
    temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='language')
    if temp:
        return temp[0].find_next('dd').get_text()
    else:
        return None

def get_chapters(work):
    temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='chapters')
    if temp:
        chapters = temp[0].find_next('dd').get_text().split('/')
        return chapters[0].strip(), chapters[1].strip() if chapters[1].strip().isdigit() else None
    else:
        return None, None
    
def is_completed(work):
    completed_chapters, total_chapters = get_chapters(work)
    if completed_chapters and total_chapters:
        return completed_chapters == total_chapters
    else:
        return False

def get_collections(work):
    temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='collections')
    if temp:
        return temp[0].find_next('dd').get_text()
    else:
        return None

def get_fandoms(work):
    temp = work.find_all('h5', class_='fandoms heading')
    if temp:
        fandoms = temp[0].find_all('a', class_='tag')
        return [fandom.get_text() for fandom in fandoms]
    else:
        return None
    

def get_work_tags(entry):
    tag_list = entry.find('ul', class_='tags commas').find_all('li')
    parsed_tags = []
    for tag in tag_list:
        tag_info = [tag.a.get_text()]
        tag_info.append(tag['class'].pop())
        #tag_info = [tag['class'].pop()]
        #tag_info.append(tag.a.get_text())
        if tag_info[0] != 'Show warnings':
            dict_tag = {
                "Tag": tag_info[0],
                "TagClass": tag_info[1],
            }
            parsed_tags.append(dict_tag)
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

def get_comments(work):
    temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='comments')
    if temp:
        return temp[0].find_next('dd').get_text()
    else:
        return None

def get_kudos(work):
    temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='kudos')
    if temp:
        return temp[0].find_next('dd').get_text()
    else:
        return None

def get_bookmarks(work):
    temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='bookmarks')
    if temp:
        return temp[0].find_next('dd').get_text()
    else:
        return None

def get_hits(work):
    temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='hits')
    if temp:
        return temp[0].find_next('dd').get_text()
    else:
        return None

def get_date_published(work):
    temp = work.find_all('div', class_='header module')[0].find_all('p', class_='datetime')
    if temp:
        return temp[0].get_text()
    else:
        return None










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
    print_out('GETTING PAGE >> 1')
    first_request = requests.get(url, cookies=cookies, headers=headers)

    pages.append(first_request)

    # https://archiveofourown.org/users/WrongfulRuffian/readings
    # https://archiveofourown.org/users/WrongfulRuffian/readings?page=2

    page_num = 2
    print_out('PAGE NUM SET TO ' + str(page_num))
    while True:
        print_out('IN WHILE')
        try:
            print_out('IN TRY')
            time.sleep(1)
            print_out('GETTING PAGE >> ' + str(page_num))
            this_url = url + '?page=' + str(page_num)
            print_out('URL: ' + this_url)
            pages.append(requests.get(this_url, cookies=cookies, headers=headers))
            page_num += 1
            if page_num == 11:
                print_out('BREAK' + page_num)
        except:
            print_out('IN EXCEPT 2')
            return pages

def call_history_v2(USERNAME, PASSWORD):
    pages = []
    history_url = f'https://archiveofourown.org/users/{USERNAME}/readings'
    login_url = 'https://archiveofourown.org/users/login'

    sess = requests.Session()

    req = sess.get(login_url)
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
        print_out('LOGIN ERROR: INVALID CRIDENTIALS')
        return 0
    elif ("Sorry, you don't have permission to access the page you were trying to reach. Please log in." in login_request.text):
        print_out('LOGIN ERROR: PERMISSION DENIED')
        return 0
    elif ("Your current session has expired and we can't authenticate your request" in login_request.text):
        print_out('LOGIN ERROR: AUTHENTICATION ERROR')
        return 0 

    # Fetch my private reading history
    print_out('GETTING PAGE >> 1')
    first_request = sess.get(history_url)
    pages.append(first_request)
    
    page_num = 2
    while True:
        try:
            time.sleep(1)
            print_out('GETTING PAGE >> ' + str(page_num))
            this_url = history_url + '?page=' + str(page_num)
            print_out('URL: ' + this_url)
            pages.append(sess.get(this_url))
            page_num += 1
            if page_num == 3:
                print_out('BREAK' + page_num)
        except:
            print_out('DONE FETCHING PAGES')
            return pages


# --------------------------------------------------------
#  JSON UTILS
# --------------------------------------------------------
def get_tag_stats_from_json(start_date = 0, end_date = datetime.now):
    
    f = open('Scrape_Results./all_works.json')
    works = json.load(f)

    tag_stats = [];

    # Get subset of works based on date if not getting whole history
    if start_date != 0:
        #get all history
        # Open json file
        print('Getting history subset')
        # Iterate through the tags
    
    for work in works:
        for tag in work['Tags']:

            if any(this_tag['Tag'] == tag['Tag'] for this_tag in tag_stats):
                for t in tag_stats:
                    if t['Tag'] == tag['Tag']:
                        t['Count'] = int(t.get('Count')) + 1
            else: 
                this_tag = {
                    'Tag': tag['Tag'],
                    'Class': tag['TagClass'],
                    'Count': 1,
                }
                tag_stats.append(this_tag)
                
    json_object = json.dumps(tag_stats, indent=4)

    with open("Scrape_Results/user_tag_stats.json", "w") as outfile:
        outfile.write(json_object)


def get_top_ten_tags():
    f = open('Scrape_Results./user_tag_stats.json')
    tags = json.load(f)

    #Sort tags
    tags_by_count = sorted(tags, key=lambda d: d['Count'], reverse=True)
    relationships_tags = []
    characters_tags = []
    freeforms_tags = []
    # Sort tags by class
    for tag in tags_by_count:
        if tag['Class'] == 'relationships':
            relationships_tags.append(tag)
        if tag['Class'] == 'characters':
            characters_tags.append(tag)
        if tag['Class'] == 'freeforms':
            freeforms_tags.append(tag)
        
    #Print first 10 tags
    i = 0
    while i < 10:
        print(freeforms_tags[i])
        i+=1

def get_characters():
        f = open('Scrape_Results./user_tag_stats.json')
        tags = json.load(f)

        # Filter for "character" tags
        character_tags = [item["Tag"] for item in data if item["Class"] == "characters"]

        # Create HTML list
        html = "<ul>\n"
        for tag in character_tags:
            html += f"  <li>{tag}</li>\n"
        html += "</ul>"

        return(html)


############################################
## BUILD HTML FORMAT
############################################
def build_stats_table():
    with open('Scrape_Results/user_data.json', "r") as f:
        data = json.load(f)
        html_table = """<table><tbody>"""

        for key, value in data.items():
            html_table += f"<tr><td><strong>{key}</strong></td><td>{value}</td></tr>"

        html_table += """
        </tbody>
        </table>
        """
    return html_table


def build_tags_table(tag_class=None):
    tags = metrics.top_10_tags(db_name, tag_class)
    html_table = """
    <table>
        <tbody>
    """
    count = 1;
    for tag in tags:
        html_table += f"<tr><td>{count}</td><td>{tag[0]}</td><td>{tag[1]}</td></tr>"
        count += 1

    html_table += """</tbody></table>"""
    return html_table

def build_ship_table(input_list):
 
    html_string = '''<table border="1">{}</table>'''
    row_format = '''<tr><td>{}</td><td>{}</td><td>{}</td></tr>'''
    temp_list = []
    
    for index, item in enumerate(input_list, start=1):
        temp_list.append(row_format.format(index, item[0], item[1]))      
    return html_string.format(''.join(temp_list))



def build_recently_visited_table(top_5_works):
    html_table = '''
    <table border="1">
       <tr>
           <th>Title</th>
           <th>Author</th>
           <th>Rating</th>
           <th>Word Count</th>
       </tr>
    '''
    print(top_5_works)
    for work in top_5_works:
        html_table += f'''
        <tr>
            <td>{work[0]}</td>
            <td>{work[1]}</td>
            <td>{work[2]}</td>
            <td>{work[3]}</td>
        </tr>
        '''
    html_table += "</table>"
    return html_table

############################################
## OTHER
############################################

def print_out(out):
    print(out)
    eel.printToOutput(out)



def get_tag_classes(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT tag_class FROM tags")
    tag_classes = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return tag_classes


'''
Search Database
'''
def search_database_a(db_name, keyword, tables=None):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    if tables is None:
        tables = ['works', 'authors', 'tags']

    results = {}

    if 'works' in tables:
        c.execute("SELECT * FROM works WHERE title LIKE ?", ('%' + keyword + '%',))
        results['works'] = c.fetchall()

    if 'authors' in tables:
        c.execute("SELECT * FROM authors WHERE author LIKE ?", ('%' + keyword + '%',))
        results['authors'] = c.fetchall()

    if 'tags' in tables:
        c.execute("SELECT * FROM tags WHERE tag LIKE ?", ('%' + keyword + '%',))
        results['tags'] = c.fetchall()

    conn.close()

    return results




def get_works_by_author_a(author_name):
    conn = sqlite3.connect('works.db')  # replace 'database.db' with your database name
    c = conn.cursor()

    # Get the author id from the authors table
    c.execute("SELECT id FROM authors WHERE author=?", (author_name,))
    author_id = c.fetchone()
    
    if author_id:
        author_id = author_id[0]
        # Get the works by the author id
        c.execute("SELECT * FROM works WHERE author_id=?", (author_id,))
        works = c.fetchall()
        
        # For each work, get the associated tags
        for i in range(len(works)):
            work_id = works[i][0]
            c.execute("SELECT tag FROM tags JOIN work_tags ON tags.id=work_tags.tag_id WHERE work_tags.work_id=?", (work_id,))
            tags = c.fetchall()
            works[i] += (tags,)
        
        return works
    else:
        return None

    conn.close()


def get_works_by_author_b(author_name):
    conn = sqlite3.connect('works.db')  # replace 'database.db' with your database name
    c = conn.cursor()

    # Get the author id from the authors table
    c.execute("SELECT id FROM authors WHERE author=?", (author_name,))
    author_id = c.fetchone()
    
    if author_id:
        author_id = author_id[0]
        # Get the works by the author id
        c.execute("SELECT * FROM works WHERE author_id=?", (author_id,))
        works = c.fetchall()
        
        # For each work, get the associated tags
        for i in range(len(works)):
            work_id = works[i][0]
            c.execute("SELECT tag FROM tags JOIN work_tags ON tags.id=work_tags.tag_id WHERE work_tags.work_id=?", (work_id,))
            tags = c.fetchall()
            works[i] += (tags,)
        
        return works
    else:
        return None

    conn.close()









