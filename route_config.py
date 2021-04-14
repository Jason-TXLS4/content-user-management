from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
import requests
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

  content = request.get_json()
  title = content['title']

  with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    sqli_query = "INSERT INTO characters (game_id, title, player_id) VALUES (?,?,?)"
    query = cursor.execute(sqli_query,(int(game_id), title, int(player_id)))
    if query != False:#not sure if this if is needed, but i figured if the insert didn't work, I shouldn't get the lastrowid
      characters_id = cursor.lastrowid #this gets the characters_id
  #if the query failed
  if not query:
    abort(409, "Could not create character")

  return_json = {"title":title, "id":str(characters_id), "game_id":game_id, "player_id":player_id, "location":"null", "attributes":"null"}
  return jsonify(return_json), 201
  

#1.2 GET /player/<player_id>/character
#retrieve a list of player characters
@app.route('/player/<player_id>/character',methods=['GET'])
def get_player_characters(player_id):  
  test = "123456" 
  with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT characters_id, title FROM characters WHERE player_id=?"
    cursor.execute(sqli_query, (test,))
  result = cursor.fetchall()
  final = []
  for row in result:
    item = {'id': row[0], 'title': row[1]}
    final.append(item)
  return jsonify(final), 201
  

#1.3 GET  /player/<player_id>/character/<character_id>
#retrieve player characer details
@app.route('/player/<player_id>/character/<character_id>',methods=['GET'])
def get_player_characters_details(player_id, character_id):   
  with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    sqli_query = "" 
    cursor.execute(sqli_query)
  result = cursor.fetchall()
  final = []
  for row in result:
    item = {}
    final.append(item)
  return jsonify(final), 201




#this method executes after every API request
@app.after_request
def after_requestuest(response):
  return response

app.debug = True
host = os.environ.get('OP', '0.0.0.0')
port = int(os.environ.get('PORT', 8080))
app.run(host=host, port=port)