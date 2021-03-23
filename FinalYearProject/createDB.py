import sqlite3

conn = sqlite3.connect('twitter.db')
print("Opened database successfully")

conn.execute('CREATE TABLE tweets (tweetText TEXT, user TEXT, date TEXT, location TEXT)')
print("Table created successfully")
conn.close()
