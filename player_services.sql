
CREATE TABLE players
(
  players_id INTEGER PRIMARY KEY AUTOINCREMENT,
  title varchar
);

CREATE TABLE  players_attributes
(
	players_attributes_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    attr_title varchar,
    attr_value varchar,
    CONSTRAINT FK FOREIGN KEY(player_id) REFERENCES players(players_id)
);

CREATE TABLE characters
(
	characters_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    player_id INTEGER,
    title varchar,
    CONSTRAINT FK FOREIGN KEY(player_id) REFERENCES players(players_id)

);

CREATE TABLE items
(
    items INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER,
    item_id INTEGER,
    CONSTRAINT FK FOREIGN KEY(character_id) REFERENCES characters(characters_id)
);

CREATE TABLE characters_attributes
(
    characters_attributes_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER,
    attr_title varchar,
    attr_value varchar,
    CONSTRAINT FK FOREIGN KEY(character_id) REFERENCES characters(characters_id) 
 );