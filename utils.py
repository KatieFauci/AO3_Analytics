from datetime import datetime
from math import floor
import eel
import json
from Models.Work import Work
from Models.Tag import Tag
import metrics



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
    print(f'word count is {word_count}')
    if word_count != None:
        return int(floor(word_count/300))
    else: 
        print("ERROR >> Word Count Not Valid To Calculate Page Count")

def build_work_results(works):
    results = []
    for work_id, title, author, rating, kudos, is_favorite, word_count in works:
        this_work = Work()
        this_work.id = work_id
        this_work.title = title
        this_work.author = author
        this_work.rating = rating
        this_work.kudos = kudos
        this_work.is_favorite = is_favorite
        this_work.word_count = word_count
        results.append(this_work)

    return results

def build_tag_results(tags):
    results = []
    for tag, count in tags:
        results.append(Tag(tag, count))
    return results

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

def build_table_of_tags(tags):
    html_table = """
    <table>
        <tbody>
    """
    work_count = metrics.get_work_count()
    count = 1
    for tag in tags:
        percent = round((tag.count/work_count)*100, 2)
        html_table += f"<tr><td>{count}</td><td>{tag.tag}</td><td>{tag.count}</td><td>{percent}%</td></tr>"
        count += 1

    html_table += """
        </tbody>
    </table>
    """
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




############################################
## OTHER
############################################

def print_out(out):
    print(out)
    eel.printToOutput(out)

