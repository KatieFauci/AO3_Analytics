import cookiejar as cookielib
import urllib

# set these to whatever your fb account is
username = "WrongfulRuffian"
password = "Szi646Feis!5SWH"

class login_ao3(object):

    def __init__(self, login, password):
        """ Start up... """
        self.login = login
        self.password = password

        self.cj = cookielib.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(debuglevel=0),
            urllib.request.HTTPSHandler(debuglevel=0),
            urllib.request.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'))
        ]

        # need this twice - once to set cookies, once to log in...
        self.loginToAo3()
        self.loginToAo3()

    def loginToAo3(self):
        """
        Handle login. This should populate our cookie jar.
        """
        login_data = urllib.urlencode({
            'email' : 'WrongfulRuffian',
            'pass' : 'Szi646Feis!5SWH',
        })
        response = self.opener.open('https://archiveofourown.org/users/login', login_data)
        return ''.join(response.readlines())