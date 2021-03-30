import sys
import sqlite3
#sys.path.append(r'C:\\Users\\W-book\\.virtualenvs\\automation_job-hsQ2VWpp\\lib\\site-packages')
#import pandas as pd

def main():

    conn = sqlite3.connect('./data/NW_DB.db')
    c = conn.cursor()

    def create_table():
        c.execute('CREATE TABLE IF NOT EXISTS jobtable(company TEXT,job_title TEXT,Describtion TEXT,\
           jobdate TEXT,text TEXT,joblink TEXT,date DATE, im TEXT,postuler TEXT,job_type TEXT)')


    conn_db = sqlite3.connect('./data/DB.db')
    c_db = conn_db.cursor()


    # Get the contents of a table
    c.execute('SELECT * FROM jobtable')
    output = c.fetchall()   # Returns the results as a list.len(output)
    #pd.read_sql_query("SELECT * FROM jobtable ", conn_db)

    # Insert those contents into another table.
    for row in output:
        c_db.execute('INSERT INTO jobtable VALUES (?,?,?,?,?,?,?,?,?,?)', row)
        conn_db.commit()

    try:
        c.execute('DROP TABLE jobtable ')
        conn.commit()
        create_table()
    except:
        create_table()

    # Cleanup
    c_db.close()
    c.close()

if __name__=='__main__':
    main()
