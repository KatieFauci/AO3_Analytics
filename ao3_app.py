import eel
import ao3_scrape

# Set web files folder
eel.init('GUI')

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello!!! from %s' % x)

@eel.expose
def button_press():
    print('HISTORY BUTTON PRESSED')


# Get user history
@eel.expose
def get_history_clicked(un, pwd):
    print('HERE\n')
    eel.printToOutput('SCRAPE STARTED')
    ao3_scrape.scrape(un, pwd)
    eel.printToOutput('SCRAPE DONE')

print('Calling Javascript...')
eel.start('main.html', size=(700, 700)) 
 # Start
