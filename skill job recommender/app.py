

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import MySQLdb.cursors
import re
import nltk
from sendemail import sendmail,sendgridmail
import smtplib


  
app = Flask(__name__)
  
app.secret_key = 'a'
english_bot = ChatBot("Chatterbot",storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")
trainer.train("data/data.yml")


  
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'N6vdYYsJDC'
app.config['MYSQL_PASSWORD'] = 'ImembuWEtt'
app.config['MYSQL_DB'] = 'N6vdYYsJDC'
mysql = MySQL(app)
@app.route('/')

def homer():
    return render_template('home.html')

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

        

   
@app.route('/register', methods =['GET', 'POST'])
def registet():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user VALUES ( % s, % s, % s)', (username, email,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            TEXT = "Hello "+username + ",\n\n"+ """Thanks for applying registring at smartinterns """ 
            message  = 'Subject: {}\n\n{}'.format("smartinterns Carrers", TEXT)
            #sendmail(TEXT,email)
            #sendgridmail(email,TEXT)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
@app.route('/dashboard')
def dash():
    
    return render_template('dashboard.html')

@app.route('/apply',methods =['GET', 'POST'])
def apply():
     msg = ''
     if request.method == 'POST' :
         username = request.form['username']
         email = request.form['email']
         
         qualification= request.form['qualification']
         skills = request.form['skills']
         jobs = request.form['s']
         cursor = mysql.connection.cursor()
         cursor.execute('SELECT * FROM jxi WHERE id = % s', (session['id'], ))
         account = cursor.fetchone()
         print(account)
         if account:
            msg = 'there is only 1 job position! for you'
            return render_template('apply.html', msg = msg)

         
         
         
         cursor = mysql.connection.cursor()
         cursor.execute('INSERT INTO jxi VALUES (NULL, % s, % s, % s,% s, % s)', (username, email,qualification,skills,jobs))
         mysql.connection.commit()
         msg = 'You have successfully applied for job !'
         session['loggedin'] = True
         TEXT = "Hello sandeep,a new appliaction for job position" +jobs+"is requested"
         
         #sendmail(TEXT,"sandeep@thesmartbridge.com")
         #sendgridmail("sandeep@thesmartbridge.com",TEXT)
         
         
         
     elif request.method == 'POST':
         msg = 'Please fill out the form !'
     return render_template('apply.html', msg = msg)

@app.route('/display')
def display():
    print(session["id"],session['username'])
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM jxi')#WHERE id = % s', (session['id'],))
    account = cursor.fetchone()
    print("accountdislay",account)

    
    return render_template('display.html',account = account)

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')
@app.route("/index1")
def index():
     return render_template("index1.html") #to send context to html

@app.route("/get")
def get_bot_response():
     userText = request.args.get("msg") #get data from input,we write js  to index.html
     return str(english_bot.get_response(userText))


    
if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port = 8080)