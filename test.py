import psycopg2


players_db = "postgres://ccybprhsnhfxgx:b2ce8114ee71abcadd147b42a47b1caa4ae540ac946317a821d04098d40d4acf@ec2-107-20-153-39.compute-1.amazonaws.com:5432/d4b7p3avace43e"
content_db = "postgres://hbwubwppwmylry:07310537702b404ca848a5c28e8f791fa4bb8abd942f81b8166ea505bf811620@ec2-34-225-103-117.compute-1.amazonaws.com:5432/deml8rlqer0tim"
con = psycopg2.connect(players_db, sslmode='require')
c = con.cursor() 



# c.execute('''
# INSERT INTO players (title) values ('Clark');
# ''')

# c.execute('''
# INSERT INTO players (title) values ('Bruce');
# ''')

# c.execute('''
# INSERT INTO players (title) values ('Hal');
# ''')


# c.execute('''
# INSERT INTO items (game_id, title, description) values (123,'shortsword','Short sword. Sharp.');
# ''')

# c.execute('''
# INSERT INTO items (game_id, title, description) values (123,'Laser Blaster','Pew Pew');
# ''')

# c.execute('''
# INSERT INTO items (game_id, title, description) values (456,'Sais','weapon of choice for a certain ninja turle');
# ''')

# c.execute('''
# INSERT INTO items (game_id, title, description) values (456,'Sais','weapon of choice for a certain ninja turle');
# ''')

c.execute('''
INSERT INTO characters_attributes (character_id, attr_title, attr_value) values (4,'height',182);
''')

# c.execute('''
# INSERT INTO rooms (game_id, title, description) values (123,'Lounge','Couches galore') RETURNING rooms_id;
# ''')
# c.execute('''
# INSERT INTO rooms (game_id, title, description) values (123,'BAsement','Man Cave') RETURNING rooms_id;
# ''')

con.commit()
c.close()
con.close()