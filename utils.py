from datetime import datetime
from math import floor
import eel
import json
import sqlite3
from Models.Work import Work

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

# --------------------------------------------------------
#  JSON UTILS
# --------------------------------------------------------
def get_tag_stats_from_json(start_date = 0, end_date = datetime.now):
    
    f = open('Scrape_Results./all_works.json')
    works = json.load(f)

    tag_stats = [];

    # Get subset of works based on date if not getting whole history
    if start_date != 0:
        #get all history
        # Open json file
        print('Getting history subset')
        # Iterate through the tags
    
    for work in works:
        for tag in work['Tags']:

            if any(this_tag['Tag'] == tag['Tag'] for this_tag in tag_stats):
                for t in tag_stats:
                    if t['Tag'] == tag['Tag']:
                        t['Count'] = int(t.get('Count')) + 1
            else: 
                this_tag = {
                    'Tag': tag['Tag'],
                    'Class': tag['TagClass'],
                    'Count': 1,
                }
                tag_stats.append(this_tag)
                
    json_object = json.dumps(tag_stats, indent=4)

    with open("Scrape_Results/user_tag_stats.json", "w") as outfile:
        outfile.write(json_object)


def get_top_ten_tags():
    f = open('Scrape_Results./user_tag_stats.json')
    tags = json.load(f)

    #Sort tags
    tags_by_count = sorted(tags, key=lambda d: d['Count'], reverse=True)
    relationships_tags = []
    characters_tags = []
    freeforms_tags = []
    # Sort tags by class
    for tag in tags_by_count:
        if tag['Class'] == 'relationships':
            relationships_tags.append(tag)
        if tag['Class'] == 'characters':
            characters_tags.append(tag)
        if tag['Class'] == 'freeforms':
            freeforms_tags.append(tag)
        
    #Print first 10 tags
    i = 0
    while i < 10:
        print(freeforms_tags[i])
        i+=1

def get_characters():
        f = open('Scrape_Results./user_tag_stats.json')
        tags = json.load(f)

        # Filter for "character" tags
        character_tags = [item["Tag"] for item in data if item["Class"] == "characters"]

        # Create HTML list
        html = "<ul>\n"
        for tag in character_tags:
            html += f"  <li>{tag}</li>\n"
        html += "</ul>"

        return(html)


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


def build_ship_table(input_list):
 
    html_string = '''<table border="1">{}</table>'''
    row_format = '''<tr><td>{}</td><td>{}</td><td>{}</td></tr>'''
    temp_list = []
    
    for index, item in enumerate(input_list, start=1):
        temp_list.append(row_format.format(index, item[0], item[1]))      
    return html_string.format(''.join(temp_list))


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




############################################
## OTHER
############################################

def print_out(out):
    print(out)
    eel.printToOutput(out)

def get_tag_classes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT tag_class FROM tags")
    tag_classes = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return tag_classes


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







