from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2005'
app.config['MYSQL_DB'] = 'lab_management'  # Updated database name
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/labtests')
def labtests():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM labtests")
    testinfo = cur.fetchall()
    cur.close()
    return render_template('labtests.html', tests=testinfo)

@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        testid = request.form['testid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM labtests WHERE id LIKE %s", ('%' + testid + '%',))
        results = cur.fetchall()
        cur.close()
        return render_template('labtests.html', tests=results)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        testid = request.form['testid']
        name = request.form['name']
        description = request.form['description']
        cost = request.form['cost']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO labtests (id, name, description, cost) VALUES (%s, %s, %s, %s)", (testid, name, description, cost))
        mysql.connection.commit()
        return redirect(url_for('labtests'))

@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM labtests WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for('labtests'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        testid = request.form['testid']
        name = request.form['name']
        description = request.form['description']
        cost = request.form['cost']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE labtests SET name = %s, description = %s, cost = %s WHERE id = %s", (name, description, cost, testid))
        mysql.connection.commit()
        return redirect(url_for('labtests'))

if __name__ == "__main__":
    app.run(debug=True)
