import sqlite3
import sys

db = "jobsearch.db"
t = "Apps"
conn = None
names = None

def add_app(conn, values):
    with conn:
        crs = conn.cursor()
        crs.execute(
            '''
            INSERT INTO Apps(Date, Deadline, Org, Source, 
                             Contact, Title, Type, Pay, Note) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''', values)

try:
    conn = sqlite3.connect(db)
    crs = conn.cursor()
    crs.execute('''CREATE TABLE IF NOT EXISTS {}
                   (Id INTEGER PRIMARY KEY, Date TEXT, 
                    Deadline TEXT, Org TEXT, Source TEXT,
                    Contact TEXT, Title TEXT, Type TEXT,
                    Pay REAL, Note TEXT)'''.format(t))
    crs.execute('PRAGMA table_info({})'.format(t))
    names = [r[1:] for r in crs.fetchall()]

except sqlite3.Error as e:
    print("Error {}:".format(e.args[0]))
    sys.exit(1)

while True:
    values = ()
    print("Enter details for new application:")
    print("(or type 'exit' to save last entry and exit)")
    for i, name in enumerate(names):
        if i: 
            value = input('{}: '.format(name[0]))
            values += (value,)
            if value == 'exit': 
                break
    if 'exit' in values:
        break
    else:
        add_app(conn, values)

if conn: 
    conn.close()


        
    
