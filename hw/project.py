from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine("sqlite:////vagrant/catalog/restaurantemenu.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#API Endpoints
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
	menu_item = session.query(MenuItem).get(menu_id)
	return jsonify(MenuItem = menu_item.serialize)

#UI Endpoints
@app.route('/')
@app.route('/restaurants/')
def restaurantIndex():
	index = session.query(Restaurant).order_by(Restaurant.name).all()
	return render_template('index.html', restaurants=index)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template('menu.html', restaurant=restaurant, items=items) 

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash('New menu item created.')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		restaurant = session.query(Restaurant).get(restaurant_id)
		return render_template('newmenuitem.html', restaurant = restaurant) 

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	menu_item = session.query(MenuItem).get(menu_id)
	
	if request.method == 'POST':
		menu_item.name = request.form['name']
		session.add(menu_item)
		session.commit()
		flash('Menu item updated.')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		restaurant = session.query(Restaurant).get(restaurant_id)
		return render_template('editmenuitem.html', restaurant=restaurant, menu_item=menu_item)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	menu_item = session.query(MenuItem).get(menu_id)
	
	if request.method == 'POST':
		session.delete(menu_item)
		session.commit()
		flash('Menu item deleted.')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html', item=menu_item)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8080)