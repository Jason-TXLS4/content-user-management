from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
import requests
import sqlite3
import os
import json


app = Flask(__name__)
players_db = "player_services.db"
content_db = "content_services.db"

@app.route('/')
def sayHello():
  return "hello there"

#API 1.1
@app.route('/game/<game_id>/player/<player_id>/character', methods=['POST'])
def createNewPlayerCharacter(game_id,player_id):
  #insert character into db

  content = request.get_json()
  title = content['title']

  with sqlite3.connect(players_db) as conn:
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
  with sqlite3.connect(players_db) as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT characters_id, title FROM characters WHERE player_id=?"
    cursor.execute(sqli_query, (test,))
  result = cursor.fetchall()
  final = []
  for row in result:
    item = {'id': row[0], 'title': row[1]}
    final.append(item)
  return jsonify(final), 200
  

#1.3 GET  /player/<player_id>/character/<character_id>
#retrieve player character details
@app.route('/player/<player_id>/character/<characters_id>',methods=['GET'])
def get_player_characters_details(player_id, characters_id):   
  with sqlite3.connect(players_db) as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT * FROM characters WHERE characters_id=?" 
    cursor.execute(sqli_query, (characters_id,))
  result = cursor.fetchone()
  result_characters_id = result[0]
  result_game_id = result[1]
  result_player_id = result[2]
  result_title = result[3]

  with sqlite3.connect(players_db) as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT * FROM characters_attributes WHERE character_id=?" 
    cursor.execute(sqli_query, (characters_id,))  
  result = cursor.fetchone()
  result_attributes = {"players_attributes_id":result[0],"player_id":result[1],"attr_title":result[2],"attr_value":result[3]}
  character = {"title":result_title, "id":result_characters_id, "game_id":result_game_id, "player_id":result_player_id, "attributes":result_attributes}
  return jsonify(character), 200

#get 1.4 from Laura


# 4.1 - Retrieve all items
# GET  /game/<game>/item   
@app.route('/game/<game_id>/item',methods=['GET'])
def get_all_items(game_id):   
  with sqlite3.connect(content_db) as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT items_id, title FROM items WHERE game_id=?" 
    cursor.execute(sqli_query, (game_id,))
  result = cursor.fetchall()
  return_json = []
  for row in result:
    item = {'id': row[0], 'title': row[1]}
    return_json.append(item)
  return jsonify(return_json), 200

 

#this method executes after every API request
@app.after_request
def after_requestuest(response):
  return response

app.debug = True
host = os.environ.get('OP', '0.0.0.0')
port = int(os.environ.get('PORT', 8080))
app.run(host=host, port=port)