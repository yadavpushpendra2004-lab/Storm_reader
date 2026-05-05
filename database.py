import sqlite3

def init_db():
    conn = sqlite3.connect('storm_reader.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes 
                 (pdf_name TEXT, page_int INTEGER, content TEXT, PRIMARY KEY (pdf_name, page_int))''')
    conn.commit()
    conn.close()

init_db()