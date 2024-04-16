import sqlite3

def create_database():
    conn = sqlite3.connect('works.db')
    c = conn.cursor()

    # Create works table
    c.execute('''CREATE TABLE IF NOT EXISTS works
                 (id INTEGER PRIMARY KEY,
                  title TEXT,
                  author_id INTEGER NOT NULL,
                  rating TEXT,
                  word_count INTEGER,
                  last_visited DATE, 
                  FOREIGN KEY(author_id) REFERENCES authors(id))''')
    
    # Create author table
    c.execute('''CREATE TABLE IF NOT EXISTS authors
                (id INTEGER PRIMARY KEY, 
                 author TEXT)''')

    # Create tags table
    c.execute('''CREATE TABLE IF NOT EXISTS tags
                 (id INTEGER PRIMARY KEY,
                  tag TEXT,
                  tag_class TEXT)''')

    # Create story_tags table
    c.execute('''CREATE TABLE IF NOT EXISTS work_tags
                 (work_id INTEGER,
                  tag_id INTEGER,
                  FOREIGN KEY(work_id) REFERENCES works(id),
                  FOREIGN KEY(tag_id) REFERENCES tags(id))''')

    conn.commit()
    conn.close()

def add_author(author_name, c):
    # Insert into authors table
    c.execute("SELECT id FROM authors WHERE author = ?", (author_name,))
    author_id = c.fetchone()

    if author_id is None:
        try:
            c.execute("INSERT INTO authors (author) VALUES (?)", (author_name,))
            author_id = c.lastrowid
        except Exception as e:
            print(f'Error Adding Author: {e}, AUTHOR_ID = {author_id}')
        return author_id
    
    return author_id[0];

def add_work(data, author_id, c):

    # Insert into works table
    c.execute("SELECT id FROM works WHERE title = ? AND author_id = ? AND rating = ?", 
              (data.title, author_id, data.rating))
    work_id = c.fetchone()

    if work_id is None:
        c.execute("INSERT INTO works (title, author_id, rating, word_count, last_visited) VALUES (?, ?, ?, ?, ?)", 
                  (data.title, author_id, data.rating, data.word_count, data.last_visited))
        work_id = c.lastrowid
        return work_id

    return work_id[0]

def add_work_tags(tags, work_id, c):
    # Insert into tags table and story_tags table
    for tag in tags:
        c.execute("SELECT id FROM tags WHERE tag = ? AND tag_class = ?", (tag['Tag'], tag['TagClass']))
        tag_id = c.fetchone()
        
        if tag_id is None:
            c.execute("INSERT INTO tags (tag, tag_class) VALUES (?, ?)", (tag['Tag'], tag['TagClass']))
            tag_id = c.lastrowid
        else:
            tag_id = tag_id[0]

        c.execute("SELECT * FROM work_tags WHERE work_id = ? AND tag_id = ?", (work_id, tag_id))
        if c.fetchone() is None:
            c.execute("INSERT INTO work_tags (work_id, tag_id) VALUES (?, ?)", (work_id, tag_id))

def insert_work_into_database(data):
    conn = sqlite3.connect('works.db')
    c = conn.cursor()

    author_id = add_author(data.author, c)
    work_id = add_work(data, author_id, c)
    add_work_tags(data.tags, work_id, c)
    
    conn.commit()
    conn.close()


