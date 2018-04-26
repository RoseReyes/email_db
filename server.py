from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mysql = MySQLConnector(app,'email')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email', methods=['POST'])
def create():
    if not EMAIL_REGEX.match(request.form['email']):
      flash("Invalid Email Address!")
      return redirect('/')
    else:
        query = "INSERT INTO email (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"  
        data = {'email': request.form['email']}
        mysql.query_db(query, data)                       
        print request.form['email']
    return redirect('/success')

@app.route('/success')
def show():
    query = "SELECT * FROM email" 
    emails = mysql.query_db(query) 
    return render_template('success.html', emails = emails)

#add this

# @app.route('/remove_friend/<friend_id>', methods=['POST'])
# def delete(friend_id):
#     query = "DELETE FROM friends WHERE id = :id"
#     data = {'id': friend_id}
#     mysql.query_db(query, data)
#     return redirect('/')

app.run(debug=True)

