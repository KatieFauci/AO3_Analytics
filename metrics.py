import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from Models.Work import Work
from Models.Tag import Tag
from Models.UserData import UserData
from DB_Access import create_connection, get_relashionships, get_all_ships
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
