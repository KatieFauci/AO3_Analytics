from datetime import datetime
from math import floor
import eel
import json
import sqlite3
from Models.Work import Work
import DB_Access

from env import DB_NAME


def print_work_data(work):
    print_out('TITLE: ' + work.title)
    print_out('AUTHOR: ' + work.author)
    print_out('WORDS: ' + str(work.word_count))
    print_out('LAST VISITED: ' + str(work.last_visited))
    print_out('TAGS: ' + str(work.tags))
    print_out('\n-------------------\n')

def print_user_data(user):
    print_out('\nTotal Works Read: ' + str(user.story_count))
    print_out('Total Words Read: ' + str(user.total_words))
    print_out('Total Pages Read: ' + str(user.page_count))
    #for key in user.tag_stats:
    #    print(key + ': ' + str(user.tag_stats.get(key)))

def store_user_data(user):
    dictionary = {
        "WorksRead": user.story_count,
        "WordsRead": user.total_words,
        "PagesRead": user.page_count, 
    }

    json_object = json.dumps(dictionary, indent=4)

    with open("Scrape_Results/user_data.json", "w") as outfile:
        outfile.write(json_object)

def get_page_count(word_count):
    return floor(word_count/300)


############################################
## BUILD HTML FORMAT
############################################
def build_stats_table():
    with open('Scrape_Results/user_data.json', "r") as f:
        data = json.load(f)
        html_table = """<table><tbody>"""

        for key, value in data.items():
            html_table += f"<tr><td><strong>{key}</strong></td><td>{value}</td></tr>"

        html_table += """
        </tbody>
        </table>
        """
    return html_table


def build_table_of_tags(input_list, tag_class=None):
    #results = metrics.top_10_tags(DB_NAME, tag_class)
    html_table = """
    <table>
        <tbody>
    """
    count = 1;
    for r in input_list:
        html_table += f"<tr><td>{count}</td><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
        count += 1

    html_table += """</tbody></table>"""
    return html_table

def build_table_of_works(results):
    table = '''
    <table border="1" id="table-of-works">
        <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Rating</th>
            <th>Word Count</th>
            <th>Kudos</th>
            <th>Favorite</th>
        </tr>
    '''
    for r in results:  
        favorite_icon = '&#9733;' if r.is_favorite else '&#9734;'  # Gold star for favorite, grey star otherwise
        table += f'''
        <tr data-work-id="{r.id}">
            <td>{r.title}</td> <!-- Assuming title is now at index 1 -->
            <td>{r.author}</td>
            <td>{r.rating}</td>
            <td>{r.word_count}</td>
            <td>{r.kudos}</td>
        '''
        if r.is_favorite:
            table += f'''<td><span class="favorite-toggle is-favorite" onclick="toggleFavoriteFromUI({r.id})">{favorite_icon}</td>'''
        else:
           table += f'''<td><span class="favorite-toggle" onclick="toggleFavoriteFromUI({r.id})">{favorite_icon}</td>''' 
        
    table += "</tr></table>"
    return table


'''
Search Database
'''
def get_search_results(search_term, search_type):
    conn = sqlite3.connect(DB_NAME) 
    cursor = conn.cursor()
    query = """
        SELECT
            w.id, w.title, 
            a.author, 
            w.rating, 
            w.kudos, 
            w.is_favorite, 
            w.word_count
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
        cursor.execute(query, (f'%{search_term}%',))
        works = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {e}")
        conn.close()
        return []
    results = []
    for w in works:
        this_work = Work()
        this_work.id = w[0]
        this_work.title = w[1]
        this_work.author = w[2]
        this_work.rating = w[3]
        this_work.kudos = w[4]
        this_work.is_favorite = w[5]
        this_work.word_count = w[6]
        results.append(this_work)

    return results


'''
def search_database(search_type, search_term, rating=None, word_count=None):
    conn = sqlite3.connect(DB_NAME) 
    c = conn.cursor()

    query = """
    SELECT DISTINCT w.title, a.author, w.rating, w.word_count, w.date_published
    FROM works w
    JOIN authors a ON w.author_id = a.id
    """
    where_clause = []
    args = []
    
    if search_type == 'title':
        where_clause.append("w.title LIKE ?")
        args.append(f'%{search_term}%')
    elif search_type == 'author':
        where_clause.append("a.author LIKE ?")
        args.append(f'%{search_term}%')        
    elif search_type == 'tag':
        query += """
                JOIN work_tags wt ON wt.work_id = w.id
                JOIN tags t ON t.id = wt.tag_id
                """
        where_clause.append("t.tag LIKE ?")
        args.append(f'%{search_term}%')
        
    if rating:
        where_clause.append("w.rating = ?")
        args.append(rating)
    
    if word_count:
        where_clause.append("w.word_count > ?")
        args.append(word_count)
    
    if where_clause:
        query += " WHERE " + " AND ".join(where_clause)
    
    query += ";"
    
    c.execute(query, args)
    data = c.fetchall()
    conn.close()
    
    return data
'''



############################################
## OTHER
############################################

def print_out(out):
    print(out)
    eel.printToOutput(out)

