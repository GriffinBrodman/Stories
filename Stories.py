#== Top Matter ===========================================================#
from flask import Flask, render_template, request
import json

app = Flask(__name__)

#== Routes ===============================================================#
@app.route("/", methods=['GET','POST'])
def root():
	if request.method == 'GET':
		render_write()
	else:
		post_story()

@app.route("/<id>")
def story():
	render_story(id)

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
	story = json.loads(readDB(id))
	title = story["title"]
	body_text = story["body_text"]
	#Render the read story template with the query data
	return render_template("story.html", title=title, body=body_text)

def post_story():
	title = request.form['title']
	body_text = request.form['body_text']
	#Generate a "unique" id
	iid = binascii.hexlify(os.urandom(4))
	#TODO: Check DB if the id exists. If so, genereate a new id.
	#while (readDB(iid)):
	#	iid = binascii.hexlify(os.urandom(4))

	#Insert the story into the db
	writeDB(title, body_text, iid)
	#Render the success page!
	render_success(id)

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

#== Main Function ========================================================#
if __name__ == "__main__":
	app.run()