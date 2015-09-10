import sqlite3
import sys

def try_sqlite3(func):
    ''' Decorator to handle sqlite3 exceptions '''
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)

        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            sys.exit(1)

class Database(object):

    def __init__(self, db_file, table='Main', fields=("Name TEXT",)):
    ''' One initial table may be specified '''
        self.conn = self.db_init(db_file)
        self.table_init(self.conn, table, fields)

    @try_sqlite3
    def disconnect(self):
        self.conn.close()

    @staticmethod
    @try_sqlite3
    def db_init(db_file):
    ''' Return connection to database '''
        conn = sqlite3.connect(db_file)
        return conn

    @staticmethod
    @try_sqlite3
    def table_init(conn, table, fields=("Name TEXT",)):
    ''' Create table if it doesn't exist '''
        with conn:
            crs = conn.cursor()
            fields_ = ', '.join(fields)
            crs.execute('''CREATE TABLE IF NOT EXISTS {}
                           (Id INTEGER PRIMARY KEY, {})'''.format(table, fields_))

    @staticmethod
    @try_sqlite3
    def table_info(db, table):
        crs = db.conn.cursor
        crs.execute('PRAGMA table_info({})'.format(table))
        return crs.fetchall()
    
    @try_sqlite3
    def add_app(self, table, values):
    ''' Add application entry to database '''
        with self.conn:
            crs = self.conn.cursor()
            statement = 'INSERT INTO {}({}) VALUES({})'
            fields = ', '.join(list(self.fields[table].keys()))
            hold = ', '.join(['?'] * len(values))
            crs.execute(statement.format(table, fields, hold), values)

    def get_entry(self, table, id=None):
    ''' Return entry with given Id, else return all entries '''
        with self.conn:
            crs = self.conn.cursor()
            if id:
                try:
                    crs.execute('SELECT * FROM Apps WHERE Id={}'.format(id))
                except:
                    print("Invalid entry Id!")
            else:
                crs.execute('SELECT * FROM Apps')
            
            return crs.fetchall()            


if __name__ == '__main__':
    try:
        db_file = sys.argv[1]
    except IndexError:
        db_file = "jobsearch.db"
    try:
        table = sys.argv[2]
    except IndexError:
        table = "Apps"

    fields = ("Date TEXT", "Deadline TEXT", "Org TEXT", "Source TEXT", 
              "Contact TEXT", "Title TEXT", "Type TEXT", "Pay REAL", "Note TEXT")

    db = Database(db_file, table, fields)
    count = 0

    while input("Add new entry? (Y/n)").lower() in ['y', '']:

        values = ()
        table_info = Database.table_info(db, table)
        names = tuple(i[1] for i in table_info)

        print("Enter details for new entry:")
        for i, name in enumerate(names):
            if i: 
                value = input('{}: '.format(name[0]))
                if value.lower() == 'exit': 
                    values += (value.lower(),)
                    break
                else:
                    values += (value,)

        if 'exit' in values:
            break
        else:
            db.add_app(table, values)
            count += 1

    print("{} new entries added to table {} in {}".format(count, table, db_file))

    db.disconnect()

        
    
