import sqlite3
import logging

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from multiprocessing import Value

counter = Value('i', 0)


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


def test_db_connection():
    try:
        number_of_articles = get_number_of_articles()

        # Check if anything at all is returned
        return True

    except:
        app.logger.info("ERROR IN CONNECTION")
    return False

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    connection.close()
    counter.value += 1
    return post


def get_number_of_articles():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    counter.value += 1
    return len(posts)


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    counter.value += 1
    return render_template('index.html', posts=posts)


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info('404 "' + str(post_id) + '" article not found!')
        return render_template('404.html'), 404
    else:
        app.logger.info('Article "' + str(post['title'] + '" retrieved!'))
        return render_template('post.html', post=post)


# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About Us Page retrieved!')
    return render_template('about.html')


# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            connection.close()
            counter.value += 1

            app.logger.info('Article "' + title + '" created!')

            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def healthcheck():

    result_message = "OK - healthy"
    result_status = 200

    if not test_db_connection():
        result_message = "db connection error"
        result_status = 500

    response = app.response_class(
        response=json.dumps({"result": result_message}),
        status=result_status,
        mimetype='application/json'
    )

    app.logger.info('Health check request complete')
    return response


@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    number_of_articles = get_number_of_articles()
    metric_text = '{"db_connection_count": ' + str(counter.value) + ', "post_count": ' + str(number_of_articles) + '}'

    response = app.response_class(
        response=json.dumps(metric_text),
        status=200,
        mimetype='application/json'
    )

    app.logger.info('Metrics request successful')
    return response


# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
    app.run(host='0.0.0.0', port='3111')
