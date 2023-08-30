from flask import Flask, render_template, request
import psycopg2
import json

app = Flask(__name__)

# PostgreSQL connection parameters
db_params = {
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost',
    'port': '5432'
}


def get_connection():
    # Establish a connection to the PostgreSQL database
    return psycopg2.connect(**db_params)


def create_table():
    # Create the 'input_data' table if it doesn't exist
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS input_data (
            id SERIAL PRIMARY KEY,
            input_values JSONB
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    # Ensure the table is created
    create_table()

    input_count = 1

    if request.method == 'POST':
        input_count = int(request.form['input_count'])
        input_values = {}

        # Collect input values from the form
        for i in range(input_count):
            input_name = f'name{i}'
            input_value = request.form.get(input_name, '')
            input_values[input_name] = input_value

        # Insert input values into the database
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO input_data (input_values) VALUES (%s)', [json.dumps(input_values)])
        connection.commit()
        cursor.close()
        connection.close()

    # Fetch saved inputs from the database
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT input_values FROM input_data')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    saved_inputs = [row[0] for row in rows]

    # Render the template with input data
    return render_template('index.html', input_count=input_count, saved_inputs=saved_inputs)


@app.route('/view_data')
def view_data():
    # Fetch saved inputs from the database for viewing
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT input_values FROM input_data')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    saved_inputs = [row[0] for row in rows]

    # Render the template to display the saved input data
    return render_template('view_data.html', saved_inputs=saved_inputs)


if __name__ == '__main__':
    app.run()
