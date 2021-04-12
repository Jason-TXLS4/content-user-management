import sqlite3

con = sqlite3.connect('content_services.db')  # You can create a new database by changing the name within the quotes
c = con.cursor() # The database will be saved in the location where your 'py' file is saved

c.execute('''

CREATE TABLE items
(
  items_id INTEGER PRIMARY KEY AUTOINCREMENT,
  title varchar,
  description varchar
);
''')

c.execute('''
CREATE TABLE  items_attributes
(
	items_attributes_id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER,
  attr_title varchar,
  attr_value varchar,
  CONSTRAINT FK FOREIGN KEY(item_id) REFERENCES items(items_id)
);
''')

c.execute('''
CREATE TABLE items_aliases
(
	items_aliases_id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER,
  title varchar,
  CONSTRAINT FK FOREIGN KEY(item_id) REFERENCES items(items_id)
);
''')

c.execute('''
CREATE TABLE rooms
(
    rooms_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    title varchar,
    description varchar
);
''')

c.execute('''
CREATE TABLE rooms_attributes
(
    rooms_attributes_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER,
    attr_title varchar,
    attr_value varchar,
    CONSTRAINT FK FOREIGN KEY(rooms_attributes_id) REFERENCES rooms(rooms_id) 
 );
''')

con.commit()
c.close()
con.close()
