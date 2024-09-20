class Work:
    def __init__(self):
        self.title = ''
        self.author = ''
        self.rating = ''
        self.date_published = ''
        self.word_count = 0
        self.tags = []
        self.last_visited = ''
        self.kudos = 0
        self.hits = 0
        self.language = ''
        self.completed_chapters = 0
        self.total_chapters = 0
        self.completed = False
        self.comments = 0
        self.bookmarks = 0
        self.fandoms = []
        self.series = []

        # Data pulled from database
        self.id = 0
        self.is_favorite = False
        self.is_rec = False
        self.bind_status = ''


    def print_data(self):
        print(f'Title: {self.title} \nAuthor: {self.author}')

