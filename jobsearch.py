import sqlite3
import sys

class Database(object):

    def __init__(self, db_file, table='Main', fields=("Name TEXT",)):
    ''' One initial table may be specified '''
        self.conn = self.db_init(db_file)
        self.table_init(self.conn, table, fields)

    def close(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))

    @staticmethod
    def db_init(db_file):
    ''' Return connection to database '''
        try:
            conn = sqlite3.connect(db_file)
            return conn

        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            sys.exit(1)

    @staticmethod
    def table_init(conn, table, fields=("Name TEXT",)):
    ''' Create table if it doesn't exist '''
        try:
            with conn:
                crs = conn.cursor()
                fields_ = ', '.join(fields)
                crs.execute('''CREATE TABLE IF NOT EXISTS {}
                               (Id INTEGER PRIMARY KEY, {})'''.format(table, fields_))

        except sqlite3.Error as e:
            print("Error {}:".format(e.args[0]))
            sys.exit(1)

    @staticmethod
    def table_info(conn, table):
        try:
            crs = conn.cursor
            crs.execute('PRAGMA table_info({})'.format(table))
            return crs.fetchall()

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
    db_file = "jobsearch.db"
    table = "Apps"
    fields = ("Date TEXT", "Deadline TEXT", "Org TEXT", "Source TEXT", 
              "Contact TEXT", "Title TEXT", "Type TEXT", "Pay REAL", "Note TEXT")
    db = Database(db_file, table, fields)
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

        
    
