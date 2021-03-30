import sys
sys.path.append(r'C:\\Users\\W-book\\.virtualenvs\\automation_job-hsQ2VWpp\\lib\\site-packages')
import sqlite3

def main():
    conn = sqlite3.connect('./data/NW_DB.db')
    c = conn.cursor()

    conn_db = sqlite3.connect('./data/DB.db')
    c_db = conn_db.cursor()


    # Get the contents of a table
    c.execute('SELECT * FROM jobtable')
    output = c.fetchall()   # Returns the results as a list.

    # Insert those contents into another table.
    for row in output:
        c_db.execute('INSERT INTO jobtable VALUES (?,?,?,?,?,?,?,?,?,?)', row)

    # Cleanup
    conn_db.commit()
    c_db.close()
    c.close()

if __name__=='__main__':
    main()
