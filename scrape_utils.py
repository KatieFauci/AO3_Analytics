from datetime import datetime
from math import floor
from utils import print_out
import requests
import time
import eel
from datetime import datetime
from math import floor
from bs4 import BeautifulSoup as bs
from Models.Work import Work


#----------------------------------------
# Scrape Functions
#----------------------------------------
def get_title(work):
    try:
        temp = work.find_all('div', class_='header module')[0].find_all('h4')[0].find_all('a')
        return temp[0].get_text()
    except Exception as e:
        eel.printToOutput(f'ERROR getting Title >>>> ERROR: {e}')


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
    try:
        temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='language')
        if temp:
            return temp[0].find_next('dd').get_text()
        else:
            return None
    except Exception as e:
        eel.printToOutput(f'ERROR getting Language >>>> ERROR: {e}')


def get_chapters(work):
    try:
        temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='chapters')
        if temp:
            chapters = temp[0].find_next('dd').get_text().split('/')
            return chapters[0].strip(), chapters[1].strip() if chapters[1].strip().isdigit() else None
        else:
            return None, None
    except Exception as e:
        eel.printToOutput(f'ERROR getting Chapters >>>> ERROR: {e}')

def is_completed(work):
    try:
        completed_chapters, total_chapters = get_chapters(work)
        if completed_chapters and total_chapters:
            return completed_chapters == total_chapters
        else:
            return False
    except Exception as e:
        eel.printToOutput(f'ERROR getting Completion Status >>>> ERROR: {e}')

def get_collections(work):
    try:
        temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='collections')
        if temp:
            return temp[0].find_next('dd').get_text()
        else:
            return None
    except Exception as e:
        eel.printToOutput(f'ERROR getting Collections >>>> ERROR: {e}')

def get_fandoms(work):
    try:
        temp = work.find_all('h5', class_='fandoms heading')
        if temp:
            fandoms = temp[0].find_all('a', class_='tag')
            return [fandom.get_text() for fandom in fandoms]
        else:
            return None
    except Exception as e:
        eel.printToOutput(f'ERROR getting Fandoms >>>> ERROR: {e}')
    

def get_work_tags(entry):
    try:
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
    except Exception as e:
        eel.printToOutput(f'ERROR getting Work Tags >>>> ERROR: {e}')

def compile_user_tags(user):
    try:
        tag_stats = {}
        for work in user.works:
            for tag in work.tags:
                if tag[0] in tag_stats:
                    # increment count
                    tag_stats[tag[0]] = tag_stats.get(tag[0]) + 1;
                else: 
                    tag_stats[tag[0]] = 1

        return tag_stats
    except Exception as e:
        eel.printToOutput(f'ERROR getting User Tags >>>> ERROR: {e}')

def get_work_word_count(work):
    try:
        return int(work.dl.dd.next_sibling.next_sibling.next_sibling.next_sibling.get_text().replace(',', ''))
    except Exception as e:
        eel.printToOutput(f'ERROR getting Work Word Count >>>> ERROR: {e}')

def get_last_visited_date(work):
    try:
        date_str = work.find('div', class_='user module group').h4.get_text().split(':')[1].split('\n')[0].strip(' ')
        return datetime.strptime(date_str, '%d %b %Y')
    except Exception as e:
        eel.printToOutput(f'ERROR getting Last Visited Date >>>> ERROR: {e}')

def get_comments(work):
    try:
        temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='comments')
        if temp:
            return temp[0].find_next('dd').get_text()
        else:
            return None
    except Exception as e:
        eel.printToOutput(f'ERROR getting Comment Count >>>> ERROR: {e}')

def get_kudos(work):
    try:
        temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='kudos')
        if temp:
            return temp[0].find_next('dd').get_text()
        else:
            return None
    except Exception as e:
        eel.printToOutput(f'ERROR getting Kudos Count >>>> ERROR: {e}')

def get_bookmarks(work):
    try:
        temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='bookmarks')
        if temp:
            return temp[0].find_next('dd').get_text()
        else:
            return None
    except Exception as e:
        eel.printToOutput(f'ERROR getting Bookmark Count >>>> ERROR: {e}')

def get_hits(work):
    try:
        temp = work.find_all('dl', class_='stats')[0].find_all('dt', class_='hits')
        if temp:
            return temp[0].find_next('dd').get_text()
        else:
            return None
    except Exception as e:
        eel.printToOutput(f'ERROR getting Hits Count >>>> ERROR: {e}')

def get_date_published(work):
    try:
        temp = work.find_all('div', class_='header module')[0].find_all('p', class_='datetime')
        if temp:
            return temp[0].get_text()
        else:
            return None
    except Exception as e:
        eel.printToOutput(f'ERROR getting Data Published >>>> ERROR: {e}')


def get_history(USERNAME, PASSWORD):
    pages = []
    history_url = f'https://archiveofourown.org/users/{USERNAME}/readings'
    login_url = 'https://archiveofourown.org/users/login'
    
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }

    sess = requests.Session()
    req = sess.get(login_url, headers=headers)

    soup = bs(req.text, features='html.parser')
    authenticity_token = soup.find('input', {'name': 'authenticity_token'})['value']
    
    # Log in to AO3
    login_request = sess.post(login_url, headers=headers, params={
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
    first_request = sess.get(history_url, headers=headers)
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