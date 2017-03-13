def index(items):	
	html = """
	<html>
	<title>Restaurant Catalog</title>
	<style>
		h2 {
			margin-top: 0.5em;
			margin-bottom: 0.5em;
		}
	</style>
	<body>
	"""
	item_html = """
	<h2>%(name)s</h2>
	<p><a href='/restaurants/%(id)s/edit'>Edit</a></p>
	<p><a href='/restaurants/%(id)s/delete'>Delete</a></p>
	"""
	for item in items:
		html += item_html % { 'name' : item.name, 'id' : item.id }

	html += "<p><a href='/restaurants/new'>Make a New Restaurant</a></p>"
	html += "</body></html>"
	return html

def new():
	html = """
	<html>
	<title>Restaurant Catalog</title>
	<style>
		h2 {
			margin-top: 0.5em;
			margin-bottom: 0.5em;
		}
	</style>
	<body>
	<h1>Make a New Restaurant</h1>
	<form method='POST' enctype='multipart/form-data'>
	<input name='name' type='text'>
	<input type='submit' value='Create'></form>
	</body></html>
	"""	
	return html

def rename():
	html = """
	<html>
	<title>Restaurant Catalog</title>
	<style>
		h2 {
			margin-top: 0.5em;
			margin-bottom: 0.5em;
		}
	</style>
	<body>
	<h1>%(name)s</h1>
	<form method='POST' enctype='multipart/form-data'>
	<input name='name' type='text'>
	<input type='submit' value='Rename'></form>
	</body></html>
	"""	
	return html

def delete():
	html = """
	<html>
	<title>Restaurant Catalog</title>
	<style>
		h2 {
			margin-top: 0.5em;
			margin-bottom: 0.5em;
		}
	</style>
	<body>
	<h1>Are you sure you want to delete %(name)s?</h1>
	<form method='POST' enctype='multipart/form-data'>
	<input type='submit' value='Delete'></form>
	</body></html>
	"""	
	return html

