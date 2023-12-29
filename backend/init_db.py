import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="flask_db2",
        # user=os.environ['DB_USERNAME'],
        # password=os.environ['DB_PASSWORD'])
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute DDL to create a new table
cur.execute('DROP TABLE IF EXISTS books;')
cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                                 'comment varchar (150) NOT NULL,'
                                 'userName varchar (50) NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('Nice work!',
             'janunine')
            )

conn.commit()

cur.close()
conn.close()
