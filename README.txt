# Catalog
A catalog of restaurants and menu items, using Python and Flask.
**In process**

## Setup the Database
You will need to create a sqlite database with the Restaurant and MenuItem tables. If you do not have the sqlite3 command line tools installed, you will need to do so first. See http://www.thegeekstuff.com/2011/07/install-sqlite3. 

Copy the sql schema in catalog.sql into sqlite3 to create the tables:
```
$sqlite3 restaurantemenu.db
>>>CREATE TABLE restaurant (
	name VARCHAR(80) NOT NULL,
	id INTEGER PRIMARY KEY ASC
);

>>>CREATE TABLE menu_item (
	name VARCHAR(80) NOT NULL,
	id INTEGER PRIMARY KEY ASC,
	course VARCHAR(250),
	description VARCHAR(250),
	price VARCHAR(8),
	restaurant_id INTEGER NOT NULL,
	FOREIGN KEY(restaurant_id) REFERENCES restaurant(id)
);
^D
```
This should create restaurantemenu.db in the CWD. In your python files, use create_engine to access the resulting restaurantemenu.db file.
```
engine = create_engine('sqlite:///absolute_path_to_db_file'')
```
There should be four backslashes total (three plus the one for the root in the file path). 'create_engine' is called in database_setup.py, lotsofmenus.py, and any time you want to use the SQLAlchemy ORM in the python command line.

Access the Database in Python Command Line:
```
$python
>>>from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker
	from database_setup import Base, Restaurant, MenuItem
	engine = create_engine("sqlite:////vagrant/catalog/restaurantemenu.db")
	Base.metadata.bin = engine
	DBSession = sessionmaker(bind = engine)
	session = DBSession()


To save you changes to the database, call:
>>>session.commit()
```



