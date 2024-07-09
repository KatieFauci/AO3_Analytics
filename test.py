import sqlite3

def get_top_5_recently_visited_works(db_file):
    conn = sqlite3.connect(db_file)
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

if __name__ == "__main__":
        # Replace 'your_database.db' with the actual filename of your SQLite database
        db_file = 'works.db'  
        print("Top 5 Recently Visited Works:")
        for i, work in enumerate(get_top_5_recently_visited_works(db_file), start=1):
            print(f"{i}. {work[0]} - {work[1]} (Rating: {work[2]}, Word Count: {work[3]})") 