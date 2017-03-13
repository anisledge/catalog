from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine("sqlite:////vagrant/catalog/restaurantemenu.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
	restaurants = session.query(Restaurant).order_by(Restaurant.name).all()
	return render_template('index.html', restaurants=restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		new_restaurant = Restaurant(name = request.form.get('name'))
		session.add(new_restaurant)
		session.commit()
		flash('New Restaurant Created')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).get(restaurant_id)
	if request.method == 'POST':
		restaurant.name = request.form.get('name')
		session.add(restaurant)
		session.commit()
		flash('Restaurant Successfully Edited')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).get(restaurant_id)
	if request.method == 'POST':
		session.delete(restaurant)
		session.commit()
		flash('Restaurant Successfully Deleted')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleterestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).get(restaurant_id)
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return render_template('menu.html', restaurant = restaurant, items = items)
 
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).get(restaurant_id)
	if request.method == 'POST':
		name = request.form.get('name')
		description = request.form.get('description')
		price = request.form.get('price')
		course = request.form.get('course')

		new_item = MenuItem(name = name, description = description, price = price, course = course, restaurant_id = restaurant_id)
		session.add(new_item)
		session.commit()
		flash('New Menu Item Created')
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).get(restaurant_id)
	item = session.query(MenuItem).get(menu_id)
	if request.method == 'POST':
		
		item.name = request.form.get('name')
		item.description = request.form.get('description')
		item.price = request.form.get('price')
		item.course = request.form.get('course')

		session.add(item)
		session.commit()
		flash('Menu Item Successfully Edited')
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant=restaurant, item=item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).get(restaurant_id)
	item = session.query(MenuItem).get(menu_id)
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash('Menu Item Successfully Deleted')
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant=restaurant, item=item)

#API ENDPOINTS
@app.route('/restaurant/JSON/')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants = [i.serialize for i in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def menuJSON(restaurant_id):
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).get(menu_id)
	return jsonify(MenuItem = item.serialize)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8080)