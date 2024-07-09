import sqlite3

def create_database():
    conn = sqlite3.connect('works.db')
    c = conn.cursor()
    
    # Create works table
    c.execute('''CREATE TABLE works (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    author_id INTEGER NOT NULL,
                    rating TEXT,
                    word_count INTEGER,
                    date_published DATE, 
                    lang TEXT,
                    completed_chapters INTEGER,
                    total_chapters INTEGER,
                    completed BOOLEAN DEFAULT 0,
                    last_visited DATE,
                    hits INTEGER DEFAULT 0,
                    kudos INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    bookmarks INTEGER DEFAULT 0,
                    is_in_series BOOLEAN DEFAULT 0,
                    num_collections INTEGER DEFAULT 0,
                    collections_link TEXT,
                    FOREIGN KEY(author_id) REFERENCES authors(id)
                )'''
              )
    
    # Create author table
    c.execute('''CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY,
                    author TEXT UNIQUE
              )'''
              )
    
    # Create tags table
    c.execute('''CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY,
                    tag TEXT UNIQUE,
                    tag_class TEXT,
                    is_ship BOOLEAN DEFAULT 0
              )'''
              )
    
   # Create work_tags table
    c.execute('''CREATE TABLE IF NOT EXISTS work_tags (
                    work_id INTEGER,
                    tag_id INTEGER,
                    PRIMARY KEY (work_id, tag_id),
                    FOREIGN KEY(work_id) REFERENCES works(id),
                    FOREIGN KEY(tag_id) REFERENCES tags(id)
              )'''
              )
    
    # Create fandoms table
    c.execute('''CREATE TABLE IF NOT EXISTS fandoms (
                    id INTEGER PRIMARY KEY,
                    fandom TEXT UNIQUE
              )'''
              )
    
    # Create work_fandoms table
    c.execute('''CREATE TABLE IF NOT EXISTS work_fandoms (
                    work_id INTEGER,
                    fandom_id INTEGER,
                    PRIMARY KEY (work_id, fandom_id),
                    FOREIGN KEY(work_id) REFERENCES works(id),
                    FOREIGN KEY(fandom_id) REFERENCES fandoms(id)
              )'''
              )  

    # Create series table
    c.execute('''CREATE TABLE IF NOT EXISTS series (
                    series_id INTEGER PRIMARY KEY,
                    series_name TEXT UNIQUE,
                    series_link TEXT UNIQUE
              )'''
              )

  
    # Create work_series table
    c.execute('''CREATE TABLE IF NOT EXISTS work_series (
                    work_id INTEGER,
                    series_id INTEGER,
                    part_number INTEGER,
                    PRIMARY KEY (work_id, series_id),
                    FOREIGN KEY(work_id) REFERENCES works(id),
                    FOREIGN KEY(series_id) REFERENCES series(series_id)
              )'''
             )

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
        c.execute("INSERT INTO works (title, author_id, rating, word_count, last_visited, date_published, lang, completed_chapters, total_chapters, completed, comments, kudos, bookmarks, hits) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (data.title, author_id, data.rating, data.word_count, data.last_visited, data.published, data.language, data.completed_chapters, data.total_chapters, data.completed, data.comments, data.kudos, data.bookmarks, data.hits))
        work_id = c.lastrowid
        return work_id

    return work_id[0]

def add_work_tags(tags, work_id, c):
    # Insert into tags table and story_tags table
    for tag in tags:
        c.execute("SELECT id FROM tags WHERE tag = ? AND tag_class = ?", (tag['Tag'], tag['TagClass']))
        tag_id = c.fetchone()
        
        if tag_id is None:
            # Check if the tag is a ship
            is_ship = 1 if tag['TagClass'] == 'relationships' and '/' in tag['Tag'] else 0
            c.execute("INSERT INTO tags (tag, tag_class, is_ship) VALUES (?, ?, ?)", (tag['Tag'], tag['TagClass'], is_ship))
            tag_id = c.lastrowid
        else:
            tag_id = tag_id[0]

        c.execute("SELECT * FROM work_tags WHERE work_id = ? AND tag_id = ?", (work_id, tag_id))
        if c.fetchone() is None:
            c.execute("INSERT INTO work_tags (work_id, tag_id) VALUES (?, ?)", (work_id, tag_id))

def add_work_fandoms(fandoms, work_id, c):
    # Insert into fandoms table and work_fandoms table
    for fandom in fandoms:
        c.execute("SELECT id FROM fandoms WHERE fandom = ?", (fandom,))
        fandom_id = c.fetchone()
        
        if fandom_id is None:
            c.execute("INSERT INTO fandoms (fandom) VALUES (?)", (fandom,))
            fandom_id = c.lastrowid
        else:
            fandom_id = fandom_id[0]

        c.execute("SELECT * FROM work_fandoms WHERE work_id = ? AND fandom_id = ?", (work_id, fandom_id))
        if c.fetchone() is None:
            c.execute("INSERT INTO work_fandoms (work_id, fandom_id) VALUES (?, ?)", (work_id, fandom_id))

def insert_series(series_name, series_link, work_id):
    conn = sqlite3.connect('works.db')
    c = conn.cursor()
    
    # Insert into series table only if the series_name does not exist
    c.execute("INSERT OR IGNORE INTO series (series_name, series_link) VALUES (?, ?)", (series_name, series_link))
    series_id = c.lastrowid

    if series_id == 0:
        c.execute("SELECT series_id FROM series WHERE series_name = ?", (series_name,))
        series_id = c.fetchone()[0]

    # Insert into work_collections table to link the work to the series
    c.execute("INSERT OR IGNORE INTO work_series (work_id, series_id) VALUES (?, ?)", (work_id, series_id))
    
    conn.commit()
    conn.close()
    return series_id



def insert_work_into_database(data):
    conn = sqlite3.connect('works.db')
    c = conn.cursor()

    author_id = add_author(data.author, c)
    work_id = add_work(data, author_id, c)
    add_work_tags(data.tags, work_id, c)
    add_work_fandoms(data.fandoms, work_id, c)
    
    conn.commit()
    conn.close()


