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

say_hello_py('Python World!')
eel.say_hello_js('Python this World!')   # Call a Javascript function


# Get user history
@eel.expose
def get_history_clicked(un, pwd):
    print('HERE\n')
    #eel.printToOutput('Scrape Started')
    ao3_scrape.scrape(un, pwd)
    #eel.printToOutput('Scrape Done')

print('Calling Javascript...')
eel.start('hello.html', size=(500, 700)) 
 # Start
