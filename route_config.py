from flask import Flask
import sqlite3
import os
import json

app = Flask(__name__)
db_name = "player_services.db"

@app.route('/')
def sayHello():
  return "<h1>Hello</h1>"

# @app.route('/v1/player',methods=['GET'])
# def get_player_data():
#   with sqlite3.connect(db_name) as con:
#     c = con.cursor()
#   c.execute("SELECT * FROM players")
#   res = str(c.fetchone())
#   return res

@app.route('/v1/player',methods=['GET'])
def get_player_data():    
  with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT * FROM players"
  cursor.execute(sqli_query)
  result = cursor.fetchall()
  final = []
  for row in result:
        item = {'id': row[0], 'name': row[1]}
        final.append(item)
  return json.dumps(final)


#this is a POST method which stores student details
@app.route('/v1/player',methods=['POST'])
def store_student_data():
  return "Student list[POST]"

#this method executes after every API request
@app.after_request
def after_requestuest(response):
  return response

app.debug = True
host = os.environ.get('OP', '0.0.0.0')
port = int(os.environ.get('PORT', 8080))
app.run(host=host, port=port)