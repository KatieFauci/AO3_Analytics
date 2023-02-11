import bs4
import utils

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
        self.word_count = 0
        self.tags = []
        self.last_visited = ''



def scrape(USERNAME, PASSWORD):
    #USERNAME = "WrongfulRuffian"
    #PASSWORD = "Szi646Feis!5SWH"
    page_num = 1
    this_user = UserData()
    response_pages = utils.call_history_v2(USERNAME, PASSWORD)

    if (response_pages == 0):
        print("UNABLE TO GET HISTORY DUE TO INVALID LOGIN")
    else:
        print(response_pages)

        for page in response_pages:
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            
            print('PARSING PAGE >> ' + str(page_num))

            for work in soup.find_all('li', attrs={"role": "article"}):

                try:
                    this_work = Work()

                    # Get title
                    this_work.title = utils.get_title(work)

                    # Get author
                    this_work.author = utils.get_author(work)

                    # TODO: Get Rating

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
                except:
                    print(f'ERROR getting work on page {page_num}')

            page_num = page_num + 1

        # Get User Stats
        this_user.tag_stats = utils.compile_user_tags(this_user)
        this_user.page_count = utils.get_page_count(this_user.total_words);

        utils.print_user_data(this_user)

    print("END")







