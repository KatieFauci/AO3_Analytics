import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from Models.Work import Work
from DB_Access import create_connection
import utils

WORK_VALUES =  '''           
                w.id, w.title, 
                a.author, 
                w.rating, 
                w.kudos, 
                w.is_favorite, 
                w.word_count
                '''


class result:
    def __init__(self, tag, tag_count, tag_percent):
        self.tag = ""
        self.tag_count = 0
        self.tag_percent = 0

def get_work_count():
    conn = create_connection()
    c = conn.cursor()
    c.execute("""
    SELECT count(*) FROM works;          
    """)
    work_count = c.fetchall()
    conn.close()
    return int(work_count[0][0])

'''
Counts the number of times each tag in the database appears. 
'''
def count_tag_occurences(tag_class=None):
    conn = create_connection()
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
def count_specific_tag_occurrence(tag):
    conn = create_connection()
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


def top_10_tags(tag_class=None):
    conn = create_connection()
    c = conn.cursor()

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

    tag_data = c.fetchall()


    conn.close()

    # Build Results
    results = []
    for t in tag_data:
        percent = round((int(t[1])/get_work_count())*100, 2)
        results.append([t[0],t[1],f"{percent}%"])

    return results



def get_tags(tag_class=None):
    conn = create_connection()
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
            
        tag_data = c.fetchall()
    finally:
        conn.close()


     # Build Results
    results = []
    for t in tag_data:
        percent = round((int(t[1])/get_work_count())*100, 2)
        results.append([t[0],t[1],f"{percent}%"])

    return results

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
            
        tag_data = c.fetchall()
    finally:
        conn.close()

     # Build Results
    results = []
    for t in tag_data:
        percent = round((int(t[1])/get_work_count())*100, 2)
        results.append([t[0],t[1],f"{percent}%"])

    return results

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
        tag_data = c.fetchall()
    finally:
       conn.close()

    # Build Results
    results = []
    for t in tag_data:
        percent = round((int(t[1])/get_work_count())*100, 2)
        results.append([t[0],t[1],f"{percent}%"])

    return results

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

def create_wordcloud(tag_set, exclude_ships):

    if tag_set == 'Top10':
        data = {item[0]: item[1] for item in top_10_tags()}
    elif tag_set == 'Characters':
        data = {item[0]: item[1] for item in get_tags('characters')}
    elif tag_set == 'Freeform':
        data = {item[0]: item[1] for item in get_tags('freeforms')}
    elif tag_set == 'Relationships':
        data = {item[0]: item[1] for item in get_relashionships(exclude_ships)}
    elif tag_set == 'Ships':
        data = {item[0]: item[1] for item in get_all_ships()}


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
