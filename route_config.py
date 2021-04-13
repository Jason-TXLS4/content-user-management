from flask import Flask
from flask import Request
from flask import Response
import sqlite3
import os
import json

app = Flask(__name__)
db_name = "player_services.db"

@app.route('/')
def sayHello():
  return "hello there"

#API 1.1
@app.route('/game/<game_id>/player/<player_id>/character', methods=['POST'])
def createNewPlayerCharacter(game_id,player_id):
  #insert character into db
  json_data = Request.json
  game_id = json_data["game_id"]
  title = json_data["title"]
  with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    sqli_query = "INSERT INTO characters (game_id, title) VALUES ('"+ title +", " + game_id + "') "
  query = cursor.execute(sqli_query)
  #if the query failed
  if(query == False):
    return Response(status=500)
  
  #build response json
    #make a query for data needed
    # RESPONSE MODEL - application/json
    # title string
    # id string
    # game_id string
    # player_id string
    # location string
    # attributes object
    #build a python data structure (a list of dicts)
    #replace the json below here with the json built in the step above
  return Response("replace this with json.dumps(<jasdata>) ", status=201, mimetype='application/json')
  
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
    return Response(json.dumps(final), status=201,  mimetype='application/json')


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