import eel
import ao3_scrape
import utils

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
    print('In app.py')
    print(utils.build_stats_table())
    return utils.build_stats_table()
    
# Get Character List
@eel.expose
def fill_character_list():
    print('In app.py')
    print(utils.get_characters())
    return utils.get_characters()
    
eel.start('main.html', size=(700, 700)) 
 # Start
