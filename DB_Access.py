import sqlite3

from env import DB_NAME
# Define global SQL strings
# Database Setup
CREATE_WORKS_TABLE = '''CREATE TABLE IF NOT EXISTS works (
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
                    rec BOOLEAN DEFAULT 0,
                    is_favorite BOOLEAN DEFAULT 0,
                    FOREIGN KEY(author_id) REFERENCES authors(id)
)'''
CREATE_AUTHORS_TABLE = '''CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY, author TEXT UNIQUE)'''
CREATE_TAGS_TABLE = '''CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY,
                    tag TEXT UNIQUE,
                    tag_class TEXT,
                    is_ship BOOLEAN DEFAULT 0)'''
CREATE_WORK_TAG_RELATION_TABLE = '''CREATE TABLE IF NOT EXISTS work_tags (
                    work_id INTEGER,
                    tag_id INTEGER,
                    PRIMARY KEY (work_id, tag_id),
                    FOREIGN KEY(work_id) REFERENCES works(id),
                    FOREIGN KEY(tag_id) REFERENCES tags(id)
              )'''
CREATE_FANDOMS_TABLE = '''CREATE TABLE IF NOT EXISTS fandoms (id INTEGER PRIMARY KEY, fandom TEXT UNIQUE)'''
CREATE_WORK_FANDOM_RELATION_TABLE = '''CREATE TABLE IF NOT EXISTS work_fandoms (
                    work_id INTEGER,
                    fandom_id INTEGER,
                    PRIMARY KEY (work_id, fandom_id),
                    FOREIGN KEY(work_id) REFERENCES works(id),
                    FOREIGN KEY(fandom_id) REFERENCES fandoms(id)
              )'''
CREATE_SERIES_TABLE = '''CREATE TABLE IF NOT EXISTS series (
                    series_id INTEGER PRIMARY KEY,
                    series_name TEXT UNIQUE,
                    series_link TEXT UNIQUE
              )'''
CREATE_WORK_SERIES_RELATION_TABLE = '''CREATE TABLE IF NOT EXISTS work_series (
                    work_id INTEGER,
                    series_id INTEGER,
                    part_number INTEGER,
                    PRIMARY KEY (work_id, series_id),
                    FOREIGN KEY(work_id) REFERENCES works(id),
                    FOREIGN KEY(series_id) REFERENCES series(series_id)
              )'''
CREATE_RATINGS_TABLE = '''CREATE TABLE IF NOT EXISTS ratings (
                    id INTEGER PRIMARY KEY,
                    rating TEXT UNIQUE,
                    rating_symbol TEXT UNIQUE
                );'''

# Initalize Reference Tables
INITALIZE_RATINGS_TABLE = '''INSERT OR IGNORE INTO ratings (rating, rating_symbol) VALUES
                    ('General Audiences', 'G'),
                    ('Teen And Up Audiences', 'T'),
                    ('Mature', 'M'),
                    ('Explicit', 'E'),
                    ('Not Rated', 'NR')
                ;'''

# Inserting to tables
INSERT_AUTHOR = "INSERT INTO authors (author) VALUES (?)"
INSERT_WORK = "INSERT INTO works (title, author_id, rating, word_count, last_visited, date_published, lang, completed_chapters, total_chapters, completed, comments, kudos, bookmarks, hits) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
INSERT_TAG = "INSERT INTO tags (tag, tag_class, is_ship) VALUES (?, ?, ?)"
INSERT_WORK_TAG_RELATION = "INSERT INTO work_tags (work_id, tag_id) VALUES (?, ?)"
INSERT_FANDOM = "INSERT INTO fandoms (fandom) VALUES (?)"
INSERT_WORK_FANDOM_RELATION = "INSERT INTO work_fandoms (work_id, fandom_id) VALUES (?, ?)"
INSERT_SERIES = "INSERT OR IGNORE INTO series (series_name, series_link) VALUES (?, ?)"
INSERT_WORK_SERIES_RELATION = "INSERT OR IGNORE INTO work_series (work_id, series_id) VALUES (?, ?)"

# Selects
SELECT_WORK_AUTHOR_TITLE_RATING = "SELECT id FROM works WHERE title = ? AND author_id = ? AND rating = ?"
SELECT_AUTHOR_BY_NAME = "SELECT id FROM authors WHERE author = ?"
SELECT_TAG_WITH_CLASS = "SELECT id FROM tags WHERE tag = ? AND tag_class = ?"
SELECT_WORK_TAG_RELATION = "SELECT * FROM work_tags WHERE work_id = ? AND tag_id = ?"
SELECT_FANDOM_ID_BY_FANDOM = "SELECT id FROM fandoms WHERE fandom = ?"
SELECT_WORK_FANDOM_RELATION = "SELECT * FROM work_fandoms WHERE work_id = ? AND fandom_id = ?"
SELECT_SERIES_ID_BY_NAME = "SELECT series_id FROM series WHERE series_name = ?"
SELECT_FAVORITES = "SELECT * FROM works WHERE is_favorite = 1"
IS_FAVORITE = "SELECT is_favorite FROM works WHERE id = ?"

# Updates
TOGGLE_FAVORITE = "UPDATE works SET is_favorite = NOT is_favorite WHERE id = ?"


# Database Searches
SEARCH_BY_TAG = """
        SELECT
            w.id, w.title, a.author, w.rating, w.kudos, w.is_favorite, w.word_count
        FROM
            works AS w
        JOIN
            authors AS a 
            ON w.author_id = a.id
        JOIN
            work_tags AS wt
            ON w.id = wt.work_id
        JOIN
            tags AS t
            ON wt.tag_id = t.id
        WHERE
            t.tag LIKE ?
        GROUP BY
            w.id, w.title, a.author, w.rating, w.kudos, w.is_favorite
        ORDER BY
            w.kudos DESC;
    """

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_database():
    conn = create_connection()
    c = conn.cursor()
    
    # Create Tables
    c.execute(CREATE_RATINGS_TABLE)
    c.execute(CREATE_WORKS_TABLE)
    c.execute(CREATE_AUTHORS_TABLE)
    c.execute(CREATE_TAGS_TABLE)
    c.execute(CREATE_WORK_TAG_RELATION_TABLE)
    c.execute(CREATE_FANDOMS_TABLE)
    c.execute(CREATE_WORK_FANDOM_RELATION_TABLE)  
    c.execute(CREATE_SERIES_TABLE)
    c.execute(CREATE_WORK_SERIES_RELATION_TABLE)

    # Initalize Table Date
    c.execute(INITALIZE_RATINGS_TABLE)

    conn.commit()
    conn.close()

def add_author(author_name, conn):
    conn = create_connection()
    c = conn.cursor()
    
    # Use the global variable for the SELECT query
    c.execute(SELECT_AUTHOR_BY_NAME, (author_name,))
    author_id = c.fetchone()
    
    if author_id is None:
        try:
            # Use the global variable for the INSERT query
            c.execute(INSERT_AUTHOR, (author_name,))
            conn.commit()  # Commit the changes after inserting a new author
            author_id = c.lastrowid
        except sqlite3.Error as e:
            print(f'Error Adding Author: {e}')  
        else:
            return author_id
    else:
        return author_id[0]
    
    conn.close()

def add_work(data, author_id):
    conn = create_connection()
    c = conn.cursor()

    # Insert into works table
    c.execute(SELECT_WORK_AUTHOR_TITLE_RATING, 
              (data.title, author_id, data.rating))
    work_id = c.fetchone()

    if work_id is None:
        c.execute(INSERT_WORK,
                  (data.title, author_id, data.rating, data.word_count, data.last_visited, data.date_published, data.language, data.completed_chapters, data.total_chapters, data.completed, data.comments, data.kudos, data.bookmarks, data.hits))
        work_id = c.lastrowid
        return work_id
    conn.close()

    return work_id[0]

def add_work_tags(tags, work_id):
    conn = create_connection()
    c = conn.cursor()
    # Insert into tags table and story_tags table
    for tag in tags:
        c.execute(SELECT_TAG_WITH_CLASS, (tag['Tag'], tag['TagClass']))
        tag_id = c.fetchone()
        
        if tag_id is None:
            # Check if the tag is a ship
            is_ship = 1 if tag['TagClass'] == 'relationships' and '/' in tag['Tag'] else 0
            c.execute(INSERT_TAG, (tag['Tag'], tag['TagClass'], is_ship))
            tag_id = c.lastrowid
        else:
            tag_id = tag_id[0]

        c.execute(SELECT_WORK_TAG_RELATION, (work_id, tag_id))
        if c.fetchone() is None:
            c.execute(INSERT_WORK_TAG_RELATION, (work_id, tag_id))
    conn.close()

def add_work_fandoms(fandoms, work_id):
    conn = create_connection()
    c = conn.cursor()
    # Insert into fandoms table and work_fandoms table
    for fandom in fandoms:
        c.execute(SELECT_FANDOM_ID_BY_FANDOM, (fandom,))
        fandom_id = c.fetchone()
        
        if fandom_id is None:
            c.execute(INSERT_FANDOM, (fandom,))
            fandom_id = c.lastrowid
        else:
            fandom_id = fandom_id[0]

        c.execute(SELECT_WORK_FANDOM_RELATION, (work_id, fandom_id))
        if c.fetchone() is None:
            c.execute(INSERT_WORK_FANDOM_RELATION, (work_id, fandom_id))
    conn.close()

def insert_series(series_name, series_link, work_id):
    conn = create_connection()
    c = conn.cursor()
    
    # Insert into series table only if the series_name does not exist
    c.execute(INSERT_SERIES, (series_name, series_link))
    series_id = c.lastrowid

    if series_id == 0:
        c.execute(SELECT_SERIES_ID_BY_NAME, (series_name,))
        series_id = c.fetchone()[0]

    # Insert into work_collections table to link the work to the series
    c.execute(INSERT_WORK_SERIES_RELATION, (work_id, series_id))
    
    conn.commit()
    conn.close()
    return series_id



def insert_work_into_database(data):
    author_id = add_author(data.author)
    work_id = add_work(data, author_id)
    add_work_tags(data.tags, work_id)
    add_work_fandoms(data.fandoms, work_id)
    
    
def toggle_favorite(work_id):
    conn = create_connection()
    c = conn.cursor()

    c.execute(TOGGLE_FAVORITE, (work_id,))
    conn.commit()
    conn.close()

def is_work_favorite(work_id):
    conn = create_connection()
    c = conn.cursor()

    c.execute(IS_FAVORITE, (work_id,))
    result = c.fetchone()
    conn.close()
    # If result is None, the work_id might not exist in the database, 
    # or there could be an issue. Here we assume it's not a favorite if not found.
    return result[0] if result else False

def get_favorites():
    conn = create_connection()
    c = conn.cursor()

    c.execute(SELECT_FAVORITES)
    favorites = c.fetchall()
    conn.close()
    return favorites