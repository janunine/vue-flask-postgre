import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db2',
                            # user=os.environ['DB_USERNAME'],
                            # password=os.environ['DB_PASSWORD']
                            )
    return conn


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

@app.route('/addComment', methods=['POST'])
def addComment():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        data = request.get_json()
        comment_content = data['content']

        #Insert the comment into the database
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (comment_content, "author", "999", "review"))
        conn.commit()

        return jsonify({'message': 'Comment added successfully'}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/deleteMsg/<int:id>', methods=['DELETE'])
def deleteMsg(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        print(id)

        # delete the comment into the database
        cur.execute("DELETE FROM books WHERE id = %s", (id,))
        conn.commit()

        return jsonify({'message': 'Comment deleted successfully'}), 204
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# route
@app.route('/test', methods=['GET'])
def test():
    return jsonify('OK!')


# route
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify('from flask!')


if __name__ == '__main__':
    app.run()