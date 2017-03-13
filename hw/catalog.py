from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import template
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine("sqlite:////vagrant/catalog/restaurantemenu.db")
Base.metadata.bin = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

edit_path = re.compile('^\/restaurants\/([0-9]+)\/edit$')
delete_path = re.compile('^\/restaurants\/([0-9]+)\/delete$')

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				
				restaurant_data = session.query(Restaurant).order_by(Restaurant.name).all()
				output = template.index(restaurant_data)

				self.wfile.write(output)
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = template.new()
				self.wfile.write(output)
				return

			edit = edit_path.match(self.path)
			if edit:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				resource_id = edit.groups()[0]
				resource = session.query(Restaurant).get(resource_id)
				
				output = template.rename() % { 'name': resource.name }
				self.wfile.write(output)
				return

			delete = delete_path.match(self.path)
			if delete:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				resource_id = delete.groups()[0]
				resource = session.query(Restaurant).get(resource_id)
				
				output = template.delete() % { 'name': resource.name }
				self.wfile.write(output)
				return

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					
					fields=cgi.parse_multipart(self.rfile, pdict)
					name = fields.get('name')[0]
					new_restaurant = Restaurant(name=name)

					session.add(new_restaurant)
					session.commit()

				self.send_response(301)
				self.send_header("Location", "/restaurants")
				s.end_headers()
				return
			
			edit = edit_path.match(self.path)
			if edit:
				resource_id = edit.groups()[0]
				resource = session.query(Restaurant).get(resource_id)

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					name = fields.get('name')[0]
				
					resource.name = name

					session.add(resource)
					session.commit()

				self.send_response(301)
				self.send_header("Location", "/restaurants")
				s.end_headers()
				return

			delete = delete_path.match(self.path)
			if delete:
				resource_id = delete.groups()[0]
				resource = session.query(Restaurant).get(resource_id)
				
				session.delete(resource)
				session.commit()

				self.send_response(301)
				self.send_header("Location", "/restaurants")
				s.end_headers()
				return

		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()