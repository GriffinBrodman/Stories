from pymongo import MongoClient
client = MongoClient()

db = client.database_name
collection = db.our_collection

def writeDB(title, body_text, iid):
	post = {"title": title,
			"body_text": body_text,
			"id": iid}
	posts = db.posts
	posts.insert(post)

def readDB(iid):
	posts = db.posts
	return posts.find_one({"id": iid})