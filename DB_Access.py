import sqlite3
import eel
from sql_statements import *
from env import DB_NAME
# Define global SQL strings
# Database Setup

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

def add_author(author_name):
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
    
    conn.commit()
    conn.close()

def add_work(data, author_id):
    try:
        conn = create_connection()
        c = conn.cursor()
        # Insert into works table
        c.execute(SELECT_WORK_AUTHOR_TITLE_RATING, 
                (data.title, author_id, data.rating))
        work_id = c.fetchone()
        
        if work_id is None:
            c.execute(INSERT_WORK,
                    (data.title, author_id, data.rating, data.word_count, data.last_visited, data.date_published, data.language, data.completed_chapters, data.total_chapters, data.completed, data.comments, data.kudos, data.bookmarks, data.hits))
            conn.commit() 
            work_id = c.lastrowid
        else:
            work_id = work_id[0]

        conn.close()

        return work_id
    except Exception as e:
        eel.printToOutput(f'ERROR Adding Work >>>> ERROR: {e}')

def add_work_tags(tags, work_id):
    conn = create_connection()
    c = conn.cursor()
    # Insert into tags table and story_tags table
    try:
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
            relation = c.fetchone()
            if relation is None:
                c.execute(INSERT_WORK_TAG_RELATION, (work_id, tag_id))

        conn.commit()    
        conn.close()
    except Exception as e:
        eel.printToOutput(f'ERROR Adding Work Tags >>>> ERROR: {e}')

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
    conn.commit()    
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
    try:
        author_id = add_author(data.author)
        work_id = add_work(data, author_id)
        add_work_tags(data.tags, work_id)
        add_work_fandoms(data.fandoms, work_id)
    except Exception as e:
        eel.printToOutput(f'ERROR Inserting Full Work Data >>>> ERROR: {e}')
    
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