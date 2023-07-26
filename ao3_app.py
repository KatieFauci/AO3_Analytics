import eel
import ao3_scrape

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

eel.start('main.html', size=(700, 700)) 
 # Start
