#== Top Matter ===========================================================#
from flask import Flask, render_template, request, Markup, jsonify
import json
from pymongo import MongoClient
import binascii
import os
import markdown

client = MongoClient()

db = client.Stories

app = Flask(__name__)
app.config['DEBUG'] = True
#TODO: Replace with a valid url

#== Routes ===============================================================#
@app.route("/", methods=['GET','POST'])
def root():
	#Render the editor on a GET request and insert to db on a POST request
	if request.method == 'GET':
		return render_write()
	else:
		return post_story()

@app.route("/<id>")
def story(id):
	#Given an id, render the mapped story. 404 if the story DNE.
	return render_story(id)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_404()


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

#== Template Functions =====================================================#
def render_write():
	"""
	Function for rendering the default text editor.
	"""
	#Render the static template
	return render_template("write.html")

def render_story(id):
	"""
	Function for rendering individual stories from the database.
	"""
	#Load the story from the database using the story id
	story = readDB(id)
	#Just in case...
	if story:
		#Store the json data into local variables
		title = Markup(story["title"])
		body_text = Markup(story["body_text"])
		#Render the read story template with the json data
		return render_template("story.html", title=title, body_text=body_text)
	else:
		return render_404()

def render_success(id):
	"""
	Function for rendering the success page (eventually do with AJAX)
	"""
	url = id
	return render_template("success.html", url)

def render_404():
	"""
	Function for rendering a 404 page
	"""
	return render_template("404.html")

#== Database Functions =====================================================#
def writeDB(title, body_text, iid):
	post = {"title": title,
			"body_text": body_text,
			"id": iid}
	posts = db.posts
	posts.insert(post)

def readDB(iid):
	posts = db.posts
	return posts.find_one({"id": iid})

def post_story():
	"""
	Function for inserting a story into the database.
	"""
	#Put the post data into local variables
	title = markdown.markdown(request.get_json()['title'])
	body_text = markdown.markdown(request.get_json()['body_text']);

	#Generate a "unique" id
	iid = binascii.hexlify(os.urandom(4))
	"""while (!readDB(iid)):
		#If there is a collision, generate another id for the story
		iid = binascii.hexlify(os.urandom(4))"""

	#Insert the story into the db
	writeDB(title, body_text, iid)
	#Render the success page!
	return jsonify(id=iid)

#== Main Function ========================================================#
if __name__ == "__main__":
	app.run()
