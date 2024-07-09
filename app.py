import eel
import ao3_scrape
import utils
import metrics

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
        return utils.build_tags_table()
    return utils.build_tags_table(tag_class)
    
# Get Character List
@eel.expose
def fill_character_list():
    return utils.get_characters()

@eel.expose
def fill_ships_table():
    return utils.build_ship_table(metrics.get_ship_tags_with_count())

@eel.expose
def fill_recently_visited_table():
    return utils.build_recently_visited_table(metrics.get_top_5_recently_visited_works())

eel.start('main.html', size=(700, 700)) 
 # Start
