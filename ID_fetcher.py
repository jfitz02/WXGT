import sqlite3 as sql

def get_next_id(db, table, value):
    db = sql.connect(db)
    c = db.cursor()

    c.execute('''SELECT MAX({}) FROM {}'''.format(value, table))

    data = c.fetchall()[0][0]
    
    if data == None:
        return 1
    return data+1
