import psycopg2


players_db = "postgres://ccybprhsnhfxgx:b2ce8114ee71abcadd147b42a47b1caa4ae540ac946317a821d04098d40d4acf@ec2-107-20-153-39.compute-1.amazonaws.com:5432/d4b7p3avace43e"
content_db = "postgres://hbwubwppwmylry:07310537702b404ca848a5c28e8f791fa4bb8abd942f81b8166ea505bf811620@ec2-34-225-103-117.compute-1.amazonaws.com:5432/deml8rlqer0tim"
con = psycopg2.connect(content_db, sslmode='require')
c = con.cursor() 

c.execute('''
DROP TABLE rooms_attributes
''')
c.execute('''
CREATE TABLE rooms_attributes
(
    rooms_attributes_id SERIAL PRIMARY KEY,
    room_id INTEGER,
    attr_title varchar,
    attr_value varchar,
    CONSTRAINT FK FOREIGN KEY(room_id) REFERENCES rooms(rooms_id) 
);
''')

con.commit()
c.close()
con.close()