import bs4
import utils
import eel
import tinydb
import json
import DB_Access

class UserData:
    def __init__(self):
        self.story_count = 0
        self.total_words = 0
        self.tag_stats = {}
        self.works = []
        self.page_count = 0

class Work:
    def __init__(self):
        self.title = ''
        self.author = ''
        self.rating = ''
        self.word_count = 0
        self.tags = []
        self.last_visited = ''



def scrape(USERNAME, PASSWORD):

    USERNAME = ""
    PASSWORD = ""

    eel.printToOutput("USERNAME: " + USERNAME)
    eel.printToOutput("PASSWORD: " + PASSWORD)
    page_num = 1
    this_user = UserData()
    response_pages = utils.call_history_v2(USERNAME, PASSWORD)
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
            #print('PARSING PAGE >> ' + str(page_num))

            for work in soup.find_all('li', attrs={"role": "article"}):
                try:
                    this_work = Work()

                    # Get title
                    this_work.title = utils.get_title(work)

                    # Get author
                    this_work.author = utils.get_author(work)

                    # TODO: Get Rating
                    this_work.rating = utils.get_rating(work)

                    # Get Work Word Count
                    this_work.word_count = utils.get_work_word_count(work)

                    # Increment Total Word Count
                    this_user.total_words = this_user.total_words + this_work.word_count

                    # Get Date Last Visited
                    this_work.last_visited = utils.last_visited_date(work)

                    # Get Work Tags
                    this_work.tags = utils.get_work_tags(work)

                    # Add Work To Users Works
                    this_user.works.append(this_work)

                    # Inc Story Count
                    this_user.story_count = this_user.story_count + 1

                    # Store info as JSON
                    dictionary = {
                        "Title": this_work.title,
                        "Author": this_work.author,
                        "Rating": this_work.rating,
                        "WordCount": this_work.word_count, 
                        "LastVisited": str(this_work.last_visited), 
                        "Tags": this_work.tags    
                    }
                    dict_collection.append(dictionary)

                    DB_Access.insert_work_into_database(this_work)

                except Exception as e:
                    eel.printToOutput(f'ERROR getting work on page {page_num} >>>> ERROR: {e}')
            page_num = page_num + 1

        # Get User Stats
        ##this_user.tag_stats = utils.compile_user_tags(this_user)
        this_user.page_count = utils.get_page_count(this_user.total_words);

        utils.print_user_data(this_user)
        utils.store_user_data(this_user)

        json_object = json.dumps(dict_collection, indent=4)

        with open("Scrape_Results/all_works.json", "w") as outfile:
            outfile.write(json_object)

        

        utils.get_tag_stats_from_json()

    print("END")








