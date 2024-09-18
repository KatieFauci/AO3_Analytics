import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from Models.Work import Work
from Models.Tag import Tag
from Models.UserData import UserData
from DB_Access import create_connection
import utils
from sql_statements import *



class result:
    def __init__(self, tag, tag_count, tag_percent):
        self.tag = ""
        self.tag_count = 0
        self.tag_percent = 0

def get_work_count():
    conn = create_connection()
    c = conn.cursor()
    c.execute(SELECT_WORK_COUNT)
    work_count = c.fetchall()
    conn.close()
    return int(work_count[0][0])


def get_tags(tag_class=None):
    conn = create_connection()  # Replace with your database file
    c = conn.cursor()
    print(f'GETTING <{tag_class}> TAGS')

    try:
        if tag_class:
            c.execute("""
                  SELECT tags.tag, COUNT(work_tags.work_id) as count
                  FROM tags
                  JOIN work_tags ON tags.id = work_tags.tag_id
                  WHERE tags.tag_class = ?
                  GROUP BY tags.tag
                  ORDER BY count DESC;
                  """, (tag_class,))
        else:
            c.execute("""
                  SELECT tags.tag, COUNT(work_tags.work_id) as count
                  FROM tags
                  JOIN work_tags ON tags.id = work_tags.tag_id
                  GROUP BY tags.tag
                  ORDER BY count DESC;
                  """)

        tags = c.fetchall()
        return utils.build_tag_results(tags)

    finally:
        conn.close()


def get_relashionships(exclude_ships=False):
    conn = create_connection()
    c = conn.cursor()
    print(f'GETTING <relationships> TAGS')

    try:
        if exclude_ships:
            c.execute("""
                  SELECT tags.tag, COUNT(work_tags.work_id) as count
                  FROM tags
                  JOIN work_tags ON tags.id = work_tags.tag_id
                  WHERE tags.tag_class = "relationships"
                  AND tags.is_ship = 0
                  GROUP BY tags.tag
                  ORDER BY count DESC;
                  """)
        else:
            c.execute("""
                  SELECT tags.tag, COUNT(work_tags.work_id) as count
                  FROM tags
                  JOIN work_tags ON tags.id = work_tags.tag_id
                  WHERE tags.tag_class = "relationships"
                  GROUP BY tags.tag
                  ORDER BY count DESC;
                  """)
            
        tags = c.fetchall()
    finally:
        conn.close()

    return utils.build_tag_results(tags)

def get_all_ships():
    conn = create_connection()
    c = conn.cursor()

    try:
        c.execute('''
            SELECT t.tag, COUNT(wt.tag_id) AS count
            FROM tags AS t
            JOIN work_tags AS wt ON t.id = wt.tag_id
            WHERE t.is_ship = 1
            GROUP BY t.tag
            ORDER BY count DESC
        ''')
        tags = c.fetchall()
    finally:
       conn.close()

    return utils.build_tag_results(tags)

def get_author_tags(author, tag_class=None):
    conn = create_connection()
    c = conn.cursor()
    
    if tag_class:
        c.execute("""
            SELECT t.tag, wt.work_id, COUNT(wt.tag_id) AS count
            FROM works w
            JOIN authors a ON w.author_id = a.id
            JOIN work_tags wt ON w.id = wt.work_id
            JOIN tags t ON wt.tag_id = t.id
            WHERE a.author = ? AND t.tag_class = ?
            GROUP BY t.tag, wt.work_id
            ORDER BY count DESC
        """, (author, tag_class))
    else:
        c.execute("""
            SELECT t.tag, wt.work_id, COUNT(wt.tag_id) AS count
            FROM works w
            JOIN authors a ON w.author_id = a.id
            JOIN work_tags wt ON w.id = wt.work_id
            JOIN tags t ON wt.tag_id = t.id
            WHERE a.author = ?
            GROUP BY t.tag, wt.work_id
            ORDER BY count DESC
        """, (author,))
    
    author_tags = c.fetchall()
    
    conn.close()
    return author_tags

def get_recently_visited_works():
    conn = create_connection()
    c = conn.cursor()

    query = f'''
    SELECT {WORK_VALUES}
    FROM works AS w
    JOIN authors AS a ON w.author_id = a.id
    ORDER BY w.last_visited DESC
    LIMIT 5
    '''
    try:
        c.execute(query)
        works = c.fetchall()
    finally:
        conn.close()

    return utils.build_work_results(works)

def get_favorites():
    conn = create_connection()
    c = conn.cursor()

    query = f'''
    SELECT {WORK_VALUES}
    FROM works AS w
    JOIN authors AS a ON w.author_id = a.id
    WHERE w.is_favorite = true
    '''
    try:
        c.execute(query)
        works = c.fetchall()
    finally:
        conn.close()

    return utils.build_work_results(works)

def calculate_user_stats():
    conn = create_connection()
    c = conn.cursor()

    try:
        c.execute(SUM_WORD_COUNT)
        words_read = c.fetchone()[0] if result else 0
        print(f'words read from db: {words_read}')
    finally:
        conn.close()

    this_user = UserData()
    this_user.story_count = get_work_count()
    this_user.total_words = words_read
    this_user.page_count = utils.get_page_count(words_read)

    return this_user

def create_wordcloud(tag_set, exclude_ships):

    if tag_set == 'Characters':
        data = {tag.tag: tag.count for tag in get_tags('characters')}
    elif tag_set == 'Freeform':
        data = {tag.tag: tag.count for tag in get_tags('freeforms')}
    elif tag_set == 'Relationships':
        data = {tag.tag: tag.count for tag in get_relashionships(exclude_ships)}
    elif tag_set == 'Ships':
        data = {tag.tag: tag.count for tag in get_all_ships()}


    wordcloud = WordCloud(width=1600, height=800, background_color='grey', min_font_size=10, max_font_size=200, colormap='Reds').generate_from_frequencies(data)
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()


'''
Search Database
'''
def get_search_results(search_term, search_type):
    conn = create_connection()
    c = conn.cursor()
    query = f"""
        SELECT {WORK_VALUES}
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
    try:
        c.execute(query, (f'%{search_term}%',))
        works = c.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {e}")
        conn.close()
        return []
    
    return utils.build_work_results(works)
