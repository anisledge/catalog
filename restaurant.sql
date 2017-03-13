CREATE TABLE restaurant (
	name VARCHAR(80) NOT NULL,
	id INTEGER PRIMARY KEY ASC
);

CREATE TABLE menu_item (
	name VARCHAR(80) NOT NULL,
	id INTEGER PRIMARY KEY ASC,
	course VARCHAR(250),
	description VARCHAR(250),
	price VARCHAR(8),
	restaurant_id INTEGER NOT NULL,
	FOREIGN KEY(restaurant_id) REFERENCES restaurant(id)
);