from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
import requests
import os
import json
import psycopg2

app = Flask(__name__)

players_db = os.environ['DATABASE_URL']
content_db = os.environ['HEROKU_POSTGRESQL_JADE_URL']

@app.route('/')
def sayHello():
  return "Hello there"


#API 1.1
@app.route('/game/<game_id>/player/<player_id>/character', methods=['POST'])
def createNewPlayerCharacter(game_id,player_id):
  #insert character into db

  content = request.get_json()
  title = content['title']

  with psycopg2.connect(players_db) as conn:
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
  with psycopg2.connect(players_db) as conn:
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
  with psycopg2.connect(players_db) as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT * FROM characters WHERE characters_id=?" 
    cursor.execute(sqli_query, (characters_id,))
  result = cursor.fetchone()
  result_characters_id = result[0]
  result_game_id = result[1]
  result_player_id = result[2]
  result_title = result[3]

  with psycopg2.connect(players_db) as conn:
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
  with psycopg2.connect(content_db) as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT items_id, title FROM items WHERE game_id=?" 
    cursor.execute(sqli_query, (game_id,))
  result = cursor.fetchall()
  return_json = []
  for row in result:
    item = {'id': row[0], 'title': row[1]}
    return_json.append(item)
  return jsonify(return_json), 200


# 4.2 add a new item to a game
# POST  /game/<game_id>/item 
@app.route('/game/<game_id>/item', methods=['POST'])
def createNewItem(game_id):

  content = request.get_json()
  title = content['title']
  description = content['description']
  aliases = content['aliases']#array
  attributes = content['attributes']#object
  
  #3 inserts
  # 1. insert items -> title, desc, game_id
  # !!get the lastrowid
  with psycopg2.connect(content_db) as conn:
    cursor = conn.cursor()
    sqli_query = "INSERT INTO items (game_id, title, description) VALUES (?,?,?)"
    query = cursor.execute(sqli_query,(int(game_id), title, description))
    if query != False: 
      item_id = cursor.lastrowid
  #if the query failed
  if not query:
    abort(409, "Could not create item")

  # 2. loop through aliases array, insert into aliases -> item_id, title
  with psycopg2.connect(content_db) as conn:
    cursor = conn.cursor()
    for v in aliases:
      sqli_query = "INSERT INTO items_aliases (item_id, title) VALUES (?,?)"
      query = cursor.execute(sqli_query, (item_id, v))      
      if not query:
        abort(409, "Could not create item")

  # 3. loop through attributes object, insert items_attr. -> item_id, attr_title, attr_value
  with psycopg2.connect(content_db) as conn:
    cursor = conn.cursor()
    for k in attributes:
      sqli_query = "INSERT INTO items_attributes (item_id, attr_title, attr_value) VALUES (?,?,?)"
      query = cursor.execute(sqli_query, (item_id, k, attributes[k]))      
      if not query:
        abort(409, "Could not create item")

  #return_json = {"title":title, "id":items_id, "game_id":game_id, "description":description, "aliases":aliases, "attributes":attributes}
  #return jsonify(return_json), 201
  return get_item(game_id, item_id)


# 4.3 - retrieve all item details
@app.route('/game/<game_id>/item/<item_id>',methods=['GET'])
def get_item(game_id,item_id):   
  with psycopg2.connect(content_db) as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT title, description FROM items WHERE game_id=? AND items_id=?" 
    cursor.execute(sqli_query, (game_id, item_id))
    result = cursor.fetchone()
    title = result[0]
    description = result[1]
    sqli_query = "SELECT title FROM items_aliases WHERE item_id=?" #notice here it's item_id and above it's items_id... I was erroneously inconsistent while creating the db
    cursor.execute(sqli_query, (item_id,))
    result = cursor.fetchall()
    aliases = []
    for r in result: 
      aliases.append(r[0])
    sqli_query = "SELECT attr_title, attr_value FROM items_attributes WHERE item_id=?" #notice here it's item_id and above it's items_id... I was erroneously inconsistent while creating the db
    cursor.execute(sqli_query, (item_id,))
    result = cursor.fetchall()
    attributes = {}
    for row in result:      
      attributes[row[0]] = row[1]


  return_json = {"title":title, "id":item_id, "game_id":game_id, "description":description, "aliases":aliases, "attributes":attributes} 
  return jsonify(return_json), 200

# 4.4 update item details
@app.route('/game/<game_id>/item/<item_id>', methods=['PUT'])
def updateItemDetails(game_id,item_id):

  content = request.get_json()
  title = content['title']
  description = content['description']
  aliases = content['aliases']#array
  attributes = content['attributes']#object

  with psycopg2.connect(content_db) as conn:
    cursor = conn.cursor()
    sqli_query = "UPDATE items SET title=?, description=? WHERE items_id=?"
    query = cursor.execute(sqli_query,(title, description,item_id))
    if not query:
      abort(409, "Could not update")
      #delete aliases and reinsert 
    sqli_query = "DELETE FROM items_aliases WHERE item_id=?"
    query = cursor.execute(sqli_query,(item_id,))
    if not query:
      abort(409, "Could not update")
    for k in aliases:
      sqli_query = "INSERT INTO items_aliases (item_id, title) VALUES (?,?)"
      query = cursor.execute(sqli_query, (item_id, k,))      
      if not query:
        abort(409, "Could not create item")
    #delete old attribtues and insert new ones
    sqli_query = "DELETE FROM items_attributes WHERE item_id=?"
    query = cursor.execute(sqli_query,(item_id,))
    if not query:
      abort(409, "Could not update")
     # 3. loop through attributes object, insert items_attr. -> item_id, attr_title, attr_value
    for k in attributes:
      sqli_query = "INSERT INTO items_attributes (item_id, attr_title, attr_value) VALUES (?,?,?)"
      query = cursor.execute(sqli_query, (item_id, k, attributes[k]))      
      if not query:
        abort(409, "Could not create item")

  if not query:
    abort(409, "Could not update")

  return get_item(game_id,item_id)

#this method executes after every API request
@app.after_request
def after_requestuest(response):
  return response

app.debug = True
host = os.environ.get('OP', '0.0.0.0')
port = int(os.environ.get('PORT', 8080))
app.run(host=host, port=port)
