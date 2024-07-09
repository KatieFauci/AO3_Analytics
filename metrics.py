import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

db_name = 'works.db'
'''
Counts the number of times each tag in the database appears. 
'''
def count_tag_occurences(db_name, tag_class=None):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    if tag_class:
        c.execute("""
                  SELECT tags.tag, COUNT(work_tags.work_id) as count
                  FROM tags
                  LEFT JOIN work_tags ON tags.id = work_tags.tag_id
                  WHERE tags.tag_class = ?
                  GROUP BY tags.tag
                  ORDER BY count DESC;
                  """, (tag_class,))
    else:
        c.execute("""
                  SELECT tags.tag, COUNT(work_tags.work_id) as count
                  FROM tags
                  LEFT JOIN work_tags ON tags.id = work_tags.tag_id
                  GROUP BY tags.tag
                  ORDER BY count DESC;
                  """)

    result = c.fetchall()
    conn.close()

    return {tag: count for tag, count in result}


'''
Counts the number of times a specified tag appears
'''
def count_specific_tag_occurrence(db_name, tag):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("""
              SELECT COUNT(DISTINCT work_tags.work_id) as count
              FROM tags
              JOIN work_tags ON tags.id = work_tags.tag_id
              WHERE tags.tag = ?;
              """, (tag,))

    result = c.fetchone()
    conn.close()

    return result[0] if result else 0



def top_10_tags(db_name, tag_class=None):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print(tag_class)

    if tag_class:
        c.execute("""
                  SELECT tags.tag, COUNT(work_tags.work_id) as count
                  FROM tags
                  JOIN work_tags ON tags.id = work_tags.tag_id
                  WHERE tags.tag_class = ?
                  GROUP BY tags.tag
                  ORDER BY count DESC
                  LIMIT 10;
                  """, (tag_class,))
    else:
        c.execute("""
                  SELECT tags.tag, COUNT(work_tags.work_id) as count
                  FROM tags
                  JOIN work_tags ON tags.id = work_tags.tag_id
                  GROUP BY tags.tag
                  ORDER BY count DESC
                  LIMIT 10;
                  """)

    result = c.fetchall()
    conn.close()

    return result



def get_author_tags(db_name, author, tag_class=None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    if tag_class:
        cursor.execute("""
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
        cursor.execute("""
            SELECT t.tag, wt.work_id, COUNT(wt.tag_id) AS count
            FROM works w
            JOIN authors a ON w.author_id = a.id
            JOIN work_tags wt ON w.id = wt.work_id
            JOIN tags t ON wt.tag_id = t.id
            WHERE a.author = ?
            GROUP BY t.tag, wt.work_id
            ORDER BY count DESC
        """, (author,))
    
    author_tags = cursor.fetchall()
    
    conn.close()
    return author_tags


def get_ship_tags_with_count():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Query to select ship tags along with their counts
    query = '''
    SELECT t.tag, COUNT(wt.tag_id) AS count
    FROM tags AS t
    JOIN work_tags AS wt ON t.id = wt.tag_id
    WHERE t.is_ship = 1
    GROUP BY t.tag
    ORDER BY count DESC
    '''
    
    try:
       cursor.execute(query)
       result = cursor.fetchall()
       ship_tags_with_count = [(tag[0], tag[1]) for tag in result]
       return ship_tags_with_count
    finally:
       connection.close()


def get_top_5_recently_visited_works():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = '''
    SELECT w.title, a.author, w.rating, w.word_count
    FROM works AS w
    JOIN authors AS a ON w.author_id = a.id
    ORDER BY w.last_visited DESC
    LIMIT 5
    '''
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        conn.close()

    
def create_wordcloud(tag_counts):
    wordcloud = WordCloud(width=1600, height=800, background_color='grey', min_font_size=10, max_font_size=200, colormap='Reds').generate_from_frequencies(tag_counts)
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()