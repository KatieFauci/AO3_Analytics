import bs4
import utils
import scrape_utils
import eel
import tinydb
import json
import DB_Access
import metrics
from Models.Work import Work
from Models.UserData import UserData

# FOR TESTING PURPOSES ONLY
import test_env



def scrape(USERNAME, PASSWORD):

    # COMMENT OUT AFTER TESTING
    USERNAME = test_env.USERNAME
    PASSWORD = test_env.PASSWORD

    eel.printToOutput("USERNAME: " + USERNAME)
    eel.printToOutput("PASSWORD: " + PASSWORD)
    
    page_num = 1
    this_user = UserData()
    response_pages = scrape_utils.get_history(USERNAME, PASSWORD)
    dict_collection = []

    DB_Access.create_database()

    if (response_pages == 0):
        eel.printToOutput("UNABLE TO GET HISTORY DUE TO INVALID LOGIN")
        print("UNABLE TO GET HISTORY DUE TO INVALID LOGIN")
        
    else:
        for page in response_pages:
            if ("Sorry, you don't have permission to access the page you were trying to reach. Please log in." in page.text):
                print('Incorrect Page')
            
            soup = bs4.BeautifulSoup(page.text, 'html.parser')

            if ("Sorry, you don't have permission to access the page you were trying to reach. Please log in." in soup):
                print('Incorrect Page')
                break
            
            eel.printToOutput('PARSING PAGE >> ' + str(page_num))

            for work in soup.find_all('li', attrs={"role": "article"}):
                try:
                    this_work = Work()
                    this_work.title = scrape_utils.get_title(work)
                    this_work.author = scrape_utils.get_author(work)
                    this_work.rating = scrape_utils.get_rating(work)
                    this_work.date_published = scrape_utils.get_date_published(work)
                    this_work.word_count = scrape_utils.get_work_word_count(work)
                    this_user.total_words = this_user.total_words + this_work.word_count
                    this_work.last_visited = scrape_utils.get_last_visited_date(work)
                    this_work.tags = scrape_utils.get_work_tags(work)
                    this_work.language = scrape_utils.get_language(work)
                    this_work.completed_chapters, this_work.total_chapters = scrape_utils.get_chapters(work)
                    this_work.completed = scrape_utils.is_completed(work)
                    this_work.comments = scrape_utils.get_comments(work)
                    this_work.kudos = scrape_utils.get_kudos(work)
                    this_work.bookmarks = scrape_utils.get_bookmarks(work)
                    this_work.hits = scrape_utils.get_hits(work)
                    this_work.fandoms = scrape_utils.get_fandoms(work)
                    # Add Work To Users Works
                    this_user.works.append(this_work)
                    # Inc Story Count
                    this_user.story_count = this_user.story_count + 1
                    DB_Access.insert_work_into_database(this_work)
                except Exception as e:
                    eel.printToOutput(f'ERROR getting work on page {page_num} >>>> ERROR: {e}')
            
            page_num = page_num + 1

        # Get User Stats
        this_user.page_count = utils.get_page_count(this_user.total_words);

        utils.print_user_data(metrics.calculate_user_stats())
        utils.store_user_data(metrics.calculate_user_stats())

        json_object = json.dumps(dict_collection, indent=4)

        with open("Scrape_Results/all_works.json", "w") as outfile:
            outfile.write(json_object)

    print("END")








