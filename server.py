from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
import flask
import requests
import os
import json
import psycopg2

app = Flask(__name__)

# players_db = os.environ['DATABASE_URL']
# content_db = os.environ['HEROKU_POSTGRESQL_JADE_URL']
players_db = "postgres://ccybprhsnhfxgx:b2ce8114ee71abcadd147b42a47b1caa4ae540ac946317a821d04098d40d4acf@ec2-107-20-153-39.compute-1.amazonaws.com:5432/d4b7p3avace43e"
content_db = "postgres://hbwubwppwmylry:07310537702b404ca848a5c28e8f791fa4bb8abd942f81b8166ea505bf811620@ec2-34-225-103-117.compute-1.amazonaws.com:5432/deml8rlqer0tim"

@app.route('/')
def sayHello():
  return "Hello there"

#API 1.1
@app.route('/game/<game_id>/player/<player_id>/character', methods=['POST'])
def createNewPlayerCharacter(game_id,player_id):
  #insert character into db

  content = request.get_json()
  title = content['title']

  with psycopg2.connect(players_db, sslmode='require') as conn:
    cursor = conn.cursor()
    sqli_query = "INSERT INTO characters (game_id, title, player_id) VALUES (%s,%s,%s) RETURNING characters_id"
    cursor.execute(sqli_query,(int(game_id), title, int(player_id)))
    #if the query failed
    if cursor.rowcount == 0:
      return flask.abort(409, "Could not create character")
    characters_id = cursor.fetchone()[0]

  return_json = {"title":title, "id":str(characters_id), "game_id":game_id, "player_id":player_id, "location":"null", "attributes":"null"}
  return jsonify(return_json), 201
  

#1.2 GET /player/<player_id>/character
#retrieve a list of player characters
@app.route('/player/<player_id>/character',methods=['GET'])
def get_player_characters(player_id):  
  with psycopg2.connect(players_db, sslmode='require') as conn:
    cursor = conn.cursor()
    query = "SELECT characters_id, title FROM characters WHERE player_id=%s"
    cursor.execute(query, (player_id,))
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
  with psycopg2.connect(players_db, sslmode='require') as conn:
    cursor = conn.cursor()
    query = "SELECT * FROM characters WHERE characters_id=%s" 
    cursor.execute(query, (characters_id,))
    if cursor.rowcount == 0:
      return flask.abort(404, "resource not found")
    for record in cursor:
      result_characters_id = record[0]
      result_game_id = record[1]
      result_player_id = record[2]
      result_title = record[3]
    query = "SELECT attr_title, attr_value FROM characters_attributes WHERE character_id=%s" 
    cursor.execute(query, (characters_id,))
    result_attributes = {}
    if cursor.rowcount > 0:
      for record in cursor:
        item = {record[0]:record[1]}
        result_attributes.update(item)
  character = {"title":result_title, "id":result_characters_id, "game_id":result_game_id, "player_id":result_player_id, "attributes":result_attributes}
  return jsonify(character), 200

# API 1.4
# Delete player character
@app.route('/player/<player_id>/character/<characters_id>', methods=['DELETE'])
def deletePlayerCharacter(player_id, characters_id):
    data = request.get_json()
    with psycopg2.connect(players_db, sslmode='require') as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT characters_id FROM characters WHERE characters_id=%s AND player_id=%s", (characters_id, player_id))
      if cursor.fetchone():
        cursor.execute("DELETE FROM characters WHERE characters_id=%s AND player_id=%s", (characters_id, player_id))
      else:
        return flask.abort(404, "Resource (character) not found")
    return '', 204


# 4.1 - Retrieve all items
# GET  /game/<game>/item   
@app.route('/game/<game_id>/item',methods=['GET'])
def get_all_items(game_id):   
  with psycopg2.connect(content_db, sslmode='require') as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT items_id, title FROM items WHERE game_id=%s" 
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
  with psycopg2.connect(content_db, sslmode='require') as conn:
    cursor = conn.cursor()
    sqli_query = "INSERT INTO items (game_id, title, description) VALUES (%s,%s,%s)"
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
      sqli_query = "INSERT INTO items_aliases (item_id, title) VALUES (%s,%s)"
      query = cursor.execute(sqli_query, (item_id, v))      
      if not query:
        return flask.abort(409, "Could not create item")

  # 3. loop through attributes object, insert items_attr. -> item_id, attr_title, attr_value
  with psycopg2.connect(content_db) as conn:
    cursor = conn.cursor()
    for k in attributes:
      sqli_query = "INSERT INTO items_attributes (item_id, attr_title, attr_value) VALUES (%s,%s,%s)"
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
    sqli_query = "SELECT title, description FROM items WHERE game_id=%s AND items_id=%s" 
    cursor.execute(sqli_query, (game_id, item_id))
    result = cursor.fetchone()
    title = result[0]
    description = result[1]
    sqli_query = "SELECT title FROM items_aliases WHERE item_id=%s" #notice here it's item_id and above it's items_id... I was erroneously inconsistent while creating the db
    cursor.execute(sqli_query, (item_id,))
    result = cursor.fetchall()
    aliases = []
    for r in result: 
      aliases.append(r[0])
    sqli_query = "SELECT attr_title, attr_value FROM items_attributes WHERE item_id=%s" #notice here it's item_id and above it's items_id... I was erroneously inconsistent while creating the db
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

  with psycopg2.connect(content_db, sslmode='require') as conn:
    cursor = conn.cursor()
    sqli_query = "UPDATE items SET title=%s, description=%s WHERE items_id=%s"
    query = cursor.execute(sqli_query,(title, description,item_id))
    if not query:
      abort(409, "Could not update")
      #delete aliases and reinsert 
    sqli_query = "DELETE FROM items_aliases WHERE item_id=%s"
    query = cursor.execute(sqli_query,(item_id,))
    if not query:
      abort(409, "Could not update")
    for k in aliases:
      sqli_query = "INSERT INTO items_aliases (item_id, title) VALUES (%s,%s)"
      query = cursor.execute(sqli_query, (item_id, k,))      
      if not query:
        abort(409, "Could not create item")
    #delete old attribtues and insert new ones
    sqli_query = "DELETE FROM items_attributes WHERE item_id=%s"
    query = cursor.execute(sqli_query,(item_id,))
    if not query:
      abort(409, "Could not update")
     # 3. loop through attributes object, insert items_attr. -> item_id, attr_title, attr_value
    for k in attributes:
      sqli_query = "INSERT INTO items_attributes (item_id, attr_title, attr_value) VALUES (%s,%s,%s)"
      query = cursor.execute(sqli_query, (item_id, k, attributes[k]))      
      if not query:
        abort(409, "Could not create item")

  if not query:
    abort(409, "Could not update")

  return get_item(game_id,item_id)

#6.1 Retrieve a list of players
@app.route('/player', methods=['GET'])
def get_players():    
  with psycopg2.connect(players_db, sslmode='require') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
  final = []
  for row in cursor:
        item = {'id': row[0], 'title': row[1]}
        final.append(item) 
  return jsonify(final), 201

#6.2
@app.route('/player', methods=['POST'])
def create_player():
  content = request.get_json()
  title = content['title']
  attributes = content['attributes']
  #2 inserts -> one to player, the other to attributes
  with psycopg2.connect(players_db, sslmode='require') as conn:
    cursor = conn.cursor()
    query = "INSERT INTO players (players_id, title) VALUES(DEFAULT, %s) RETURNING players_id;"
    cursor.execute(query, (title,))
    player_id = cursor.fetchone()[0]
    if cursor.rowcount == 0:
      return flask.abort(409, "Could not create character")
    
    # #loop through attributes
    for k in attributes:
      query = "INSERT INTO players_attributes (attr_title, attr_value, player_id) VALUES (%s, %s, %s);"
      cursor.execute(query,(k,str(attributes[k]), player_id))
      if cursor.rowcount == 0:
        return flask.abort(409, "Could not create character")
  return get_player_details(player_id)

  #6.3 Retrieve Player details
@app.route('/player/<player_id>',methods=['GET'])
def get_player_details(player_id):
  with psycopg2.connect(players_db, sslmode='require') as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT title FROM players WHERE players_id=%s"
    cursor.execute(sqli_query, (player_id,))
    result = cursor.fetchone()
    title = result[0]
    sqli_query = "SELECT characters_id, title FROM characters WHERE player_id=%s"
    cursor.execute(sqli_query, (player_id,))
    result = cursor.fetchall()
    characters = []
    for row in result:
      items = {'id': row[0], 'title': row[1]}
      characters.append(items)
    sqli_query = "SELECT attr_title, attr_value FROM players_attributes WHERE player_id=%s" 
    cursor.execute(sqli_query, (player_id,))
    result = cursor.fetchall()
    attributes = {}
    for row in result:      
      attributes[row[0]] = row[1] 
  return_json = {"title":title, "id":player_id, "attributes":attributes, "characters":characters} 
  return jsonify(return_json), 200

#6.4 Update player details 
@app.route('/player/<player_id>', methods=['PUT'])
def update_player(player_id):
  content = request.get_json()
  title = content['title']
  attributes = content['attributes']

  with psycopg2.connect(players_db, sslmode='require') as conn:
    cursor = conn.cursor()
    query = "UPDATE players SET title=%s WHERE players_id=%s"
    cursor.execute(query,(title, player_id,))      
    if cursor.rowcount == 0:
      return flask.abort(409, "Could not update") 

    query = "SELECT * FROM players_attributes WHERE player_id=%s;"
    cursor.execute(query, (player_id,))
    if cursor.rowcount != 0:
      query = "DELETE FROM players_attributes WHERE player_id=%s;"
      cursor.execute(query, (player_id,))
      if cursor.rowcount == 0:
        return flask.abort(409, "Could not update")
    
    for y in attributes:
      query = "INSERT INTO players_attributes (player_id, attr_title, attr_value) VALUES (%s,%s,%s)"
      cursor.execute(query, (player_id, y, attributes[y]))      
      if cursor.rowcount == 0:
        return flask.abort(409, "Could not update")
  return get_player_details(player_id)


# 6.5 DELETE player
#remove a player -- return (204, "Player deleted")
@app.route('/player/<player_id>',methods=['DELETE'])
def remove_player(player_id):
  with psycopg2.connect(players_db, sslmode='require') as conn:
    cursor = conn.cursor()
    query = "SELECT * FROM players WHERE players_id=%s;" #see that player exists
    cursor.execute(query, (player_id,))
    if cursor.rowcount == 1: #if players exists
      query = "DELETE FROM players_attributes WHERE player_id=%s;"
      cursor.execute(query, (player_id,))
      if cursor.rowcount == 0:
        return flask.abort(409, "Player could not be deleted")
      query = "DELETE FROM players WHERE players_id=%s;" #delete player
      cursor.execute(query, (player_id,))
      if cursor.rowcount == 0:
        return flask.abort(409, "Player could not be deleted")
    else:
      return flask.abort(409, "Player does not exist")
  return '', 204

#7.1 
# Retrieve rooms
@app.route('/game/<game_id>/room', methods=['GET'])
def get_rooms(game_id):  
  with psycopg2.connect(content_db, sslmode='require') as conn:
    cursor = conn.cursor()
    query = "SELECT rooms_id, title FROM rooms WHERE game_id=%s"
    cursor.execute(query, (game_id,))
  result = cursor.fetchall()
  final = []
  for row in result:
    item = {'id': row[0], 'title': row[1]}
    final.append(item)
  return jsonify(final), 200

#7.2 POST 
@app.route('/game/<game_id>/room', methods=['POST'])
def createNewRoom(game_id):
  content = request.get_json()
  title = content['title']
  description = content['description']
  attributes = content['attributes']

  with psycopg2.connect(content_db, sslmode='require') as conn:
    cursor = conn.cursor()
    query = "INSERT INTO rooms (game_id, title, description) VALUES (%s,%s,%s) RETURNING rooms_id;"
    cursor.execute(query,(int(game_id), title, description))
    if cursor.rowcount == 0:
      return flask.abort(409, "Could not create room")
    rooms_id = cursor.fetchone()[0]
  with psycopg2.connect(content_db, sslmode='require') as conn:
    cursor = conn.cursor()
    for key in attributes:
      query = "INSERT INTO rooms_attributes (room_id, attr_title, attr_value) VALUES (%s,%s,%s);"
      cursor.execute(query, (int(rooms_id) ,key, attributes[key]))
  
  return get_room_details(game_id, rooms_id)
  
#7.3
@app.route('/game/<game_id>/room/<room_id>', methods=['GET'])
def get_room_details(game_id, room_id):
  with psycopg2.connect(content_db, sslmode='require') as conn:
    cursor = conn.cursor()
    query = "SELECT title, description FROM rooms WHERE game_id=%s AND rooms_id=%s;" 
    cursor.execute(query, (game_id, room_id))
    if cursor.rowcount == 0:
      return flask.abort(404, "resource(room) not found")
    for record in cursor:
      title = record[0]
      description = record[1]
      
    query = "SELECT attr_title, attr_value FROM rooms_attributes WHERE room_id=%s" 
    cursor.execute(query, (int(room_id),))
    attributes = {}
    if cursor.rowcount > 0:
      for record in cursor:      
        item = {record[0]:record[1]}
        attributes.update(item)

  return_json = {"title":title, "id":room_id, "game_id":game_id, "description":description, "attributes":attributes} 
  return jsonify(return_json), 200

#7.4 Update room details 
@app.route('/game/<game_id>/room/<room_id>', methods=['PUT'])
def update_room_details(game_id, room_id):
  content = request.get_json()
  title = content['title']
  description = content['description']
  attributes = content['attributes']

  with psycopg2.connect(content_db, sslmode='require') as conn:
    cursor = conn.cursor()
    query = "SELECT * FROM rooms WHERE rooms_id=%s;"
    cursor.execute(query, (room_id,))
    if cursor.rowcount != 0:
      query = "UPDATE rooms SET title=%s, description=%s WHERE rooms_id=%s;"
      cursor.execute(query, (title, description, room_id))      
      if cursor.rowcount == 0:
        return flask.abort(409, "Could not update room")
    query = "SELECT * FROM rooms_attributes WHERE rooms_id=%s;"
    cursor.execute(query, (room_id,))
    if cursor.rowcount != 0:
      query = "DELETE FROM rooms_attributes WHERE room_id=%s;"
      cursor.execute(query, (room_id,))
      if cursor.rowcount == 0:
        return flask.abort(409, "Could not update room")
    
    for k in attributes:
      query = "INSERT INTO rooms_attributes (room_id, attr_title, attr_value) VALUES (%s,%s,%s)"
      cursor.execute(sqli_query, (room_id, k, attributes[k]))      
      if cursor.rowcount == 0:
        return flask.abort(409, "Could not update room")
  
  return get_room_details(game_id, room_id)


#this method executes after every API request
@app.after_request
def after_requestuest(response):
  return response

app.debug = True
host = os.environ.get('OP', '0.0.0.0')
port = int(os.environ.get('PORT', 8080))
app.run(host=host, port=port)

# if __name__ == '__main__':
#     app.run(threaded=True, port=5000)
