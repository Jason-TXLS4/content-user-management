import os
import psycopg2

#content_db = os.environ['HEROKU_POSTGRESQL_JADE_URL']
conn = psycopg2.connect(content_db, sslmode='require')  
c = conn.cursor()

c.execute('''

CREATE TABLE items
(
  items_id SERIAL PRIMARY KEY,
  game_id INTEGER,
  title varchar,
  description varchar
);
''')

c.execute('''
CREATE TABLE  items_attributes
(
  items_attributes_id SERIAL PRIMARY KEY,
  item_id INTEGER,
  attr_title varchar,
  attr_value varchar,
  CONSTRAINT FK FOREIGN KEY(item_id) REFERENCES items(items_id)
);
''')

c.execute('''
CREATE TABLE items_aliases
(
  items_aliases_id SERIAL PRIMARY KEY,
  item_id INTEGER,
  title varchar,
  CONSTRAINT FK FOREIGN KEY(item_id) REFERENCES items(items_id)
);
''')

c.execute('''
CREATE TABLE rooms
(
    rooms_id SERIAL PRIMARY KEY,
    game_id INTEGER,
    title varchar,
    description varchar
);
''')

c.execute('''
CREATE TABLE rooms_attributes
(
    rooms_attributes_id SERIAL PRIMARY KEY,
    room_id INTEGER,
    attr_title varchar,
    attr_value varchar,
    CONSTRAINT FK FOREIGN KEY(rooms_attributes_id) REFERENCES rooms(rooms_id) 
);
''')

conn.commit()
c.close()
conn.close()
