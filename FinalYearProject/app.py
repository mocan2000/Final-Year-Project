from flask import Flask, render_template, request
import sqlite3 as sql
from flask import request
import nltk
import random
import string
from nltk.classify import *
import nltk.classify.util
import pickle
import sys
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

def format_sentence(tweet):
    return({word: True for word in nltk.word_tokenize(tweet)})
# @app.route('/enternew')
# def new_student():
   # return render_template('student.html')

# @app.route('/addrec',methods = ['POST', 'GET'])
# def addrec():
   # if request.method == 'POST':
      # try:
         # nm = request.form['nm']
         # addr = request.form['add']
         # city = request.form['city']
         # pin = request.form['pin']
         
         # with sql.connect("database.db") as con:
            # cur = con.cursor()
            
            # cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            # con.commit()
            # msg = "Record successfully added"
      # except:
         # con.rollback()
         # msg = "error in insert operation"
      
      # finally:
         # return render_template("result.html",msg = msg)
         # con.close()

@app.route('/human_rights')
def classify():
   f = open('trained_classifier.pickle', 'rb')
   classifier = pickle.load(f)
   f.close()
   con = sql.connect("twitter.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("SELECT * from tweets")

   rows = cur.fetchall();


   #date_mytweets = rows[0]

   for row in range(0,10):
      #theTweets.append(tweet['my_tweet'])
      line = random.choice(rows)
      myLine=line[0]
      text=classifier.classify(format_sentence(myLine))
      sent=str(myLine)
      result=str(text)
   return render_template('human_rights.html',result=result, sent=sent)

@app.route('/list')
def list():
   con = sql.connect("twitter.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("SELECT * from tweets")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)
