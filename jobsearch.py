import sqlite3
import sys
from datetime import datetime as dt

def try_sqlite3(func):
    ''' Decorator to handle sqlite3 exceptions '''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            sys.exit(1)

    return wrapper

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
        return sqlite3.connect(db_file)

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
        crs = db.conn.cursor()
        crs.execute('PRAGMA table_info({})'.format(table))
        return crs.fetchall()
    
    @classmethod
    def table_columns(cls, db, table):
        ''' Return names of columns in table '''
        return tuple(c[1] for c in cls.table_info(db, table))

    @try_sqlite3
    def add_app(self, table, values):
        ''' Add application entry to database '''
        with self.conn:
            crs = self.conn.cursor()
            names = self.table_columns(self, table)[1:]
            fields = ', '.join(names)
            hold = ', '.join(['?'] * len(names))
            statement = 'INSERT INTO {}({}) VALUES({})'
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

    datetime_fmt = "%Y/%m/%d %H:%M:%S"

    db = Database(db_file, table, fields)
    count = 0

    while input("Add new entry? (Y/n)").lower() in ['y', '']:

        values = ()
        names = Database.table_columns(db, table)
        print(names)
        print("Enter details for new entry:")
        for i, name in enumerate(names):
            if i: # 'Id' has i==0 and is auto incremented 
                if name == "Date":
                    now = dt.now().strftime(datetime_fmt)
                    value = input('{} (default: \"{}\"): '.format(name, now))
                    if not value:
                        value = now
                else:
                    value = input('{}: '.format(name))

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
    print("The table now contains {} entries".format(len(db.get_entry(table))))

    db.disconnect()

        
    
