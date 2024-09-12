import eel
import ao3_scrape
import utils
import metrics
import sqlite3
import DB_Access

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
    return utils.build_table_of_works(metrics.get_recently_visited_works())

@eel.expose
def fill_favorites_table():
    return utils.build_table_of_works(metrics.get_favorites())

@eel.expose
def get_search_results(term, type):
    print(f'{term}:{type}')
    results = utils.build_table_of_works(metrics.get_search_results(term, type))
    return results

@eel.expose
def display_wordcloud(data_type, exclude_ships=False):
    metrics.create_wordcloud(data_type, exclude_ships)

@eel.expose
def toggle_favorite_ui(work_id):
    # Toggle the favorite status
    DB_Access.toggle_favorite(work_id)
    # Now, retrieve the new status to return it
    is_favorite = DB_Access.is_work_favorite(work_id)
    return {"is_favorite": is_favorite, "message": "Favorite toggled"}

eel.start('main.html', size=(1500, 800)) 
 # Start
