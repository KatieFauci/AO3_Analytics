import eel
import ao3_scrape
import utils
import metrics
import sqlite3

# Set web files folder
eel.init('GUI')

@eel.expose
def button_press():
    print('HISTORY BUTTON PRESSED')


# Get user history
@eel.expose
def get_history_clicked(un, pwd):
    print('Get History Clicked\n')
    eel.printToOutput('SCRAPE STARTED')
    ao3_scrape.scrape(un, pwd)
    eel.printToOutput('SCRAPE DONE')

# Get Stats Table
@eel.expose
def fill_stats_table():
    return utils.build_stats_table()

# Get Tags Table
@eel.expose
def fill_tags_table(tag_class=None):
    if tag_class == 'None':
        return utils.build_table_of_tags(metrics.get_tags(tag_class))
    return utils.build_table_of_tags(metrics.get_tags(tag_class))

@eel.expose
def fill_relashionship_table(exclude_ships=False):
    return utils.build_table_of_tags(metrics.get_relashionships(exclude_ships))

@eel.expose
def fill_top_10_table(tag_class=None):
    if tag_class == 'None':
        return utils.build_table_of_tags(metrics.top_10_tags(tag_class))
    return utils.build_table_of_tags(metrics.top_10_tags(tag_class))
    
# Get Character List
@eel.expose
def fill_character_list():
    return utils.get_characters()

@eel.expose
def fill_ships_table():
    return utils.build_table_of_tags(metrics.get_all_ships())

@eel.expose
def fill_recently_visited_table():
    return utils.build_recently_visited_table(metrics.get_top_5_recently_visited_works())

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('works.db')
    return conn

@eel.expose
def get_search_results(term, type):
    print(f'{term}:{type}')
    results = utils.build_search_table(utils.get_search_results(term, type))
    return results

@eel.expose
def display_wordcloud(data_type, exclude_ships=False):
    metrics.create_wordcloud(data_type, exclude_ships)

eel.start('main.html', size=(700, 700)) 
 # Start
