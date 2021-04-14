import sqlite3
from flask import Response
import json

db_name = 'player_services.db'

def get_char_data():    
  with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    sqli_query = "SELECT * FROM characters"
  cursor.execute(sqli_query)
  result = cursor.fetchall()
  final = []
  for row in result:
    item = {'id': row[0], 'game_id': row[1], 'player_id': row[2], 'title': row[3]}
    print(str(item))
    # final.append(item)
    # return Response(json.dumps(final), status=201,  mimetype='application/json')

get_char_data()
