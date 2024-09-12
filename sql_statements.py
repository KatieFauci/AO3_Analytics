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
SELECT_WORK_COUNT = "SELECT count(*) FROM works"
SUM_WORD_COUNT = 'SELECT SUM(word_count) FROM works'

# Updates
TOGGLE_FAVORITE = "UPDATE works SET is_favorite = NOT is_favorite WHERE id = ?"


# Database Searche statements
WORK_VALUES =  '''           
                w.id, 
                w.title, 
                a.author, 
                w.rating, 
                w.kudos, 
                w.is_favorite, 
                w.word_count
                '''

SEARCH_BY_TAG = f"""
        SELECT
            {WORK_VALUES}
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