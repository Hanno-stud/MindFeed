from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
try:
    client.server_info()  # Test connection
    print("MongoDB Connected")
except Exception as e:
    print("MongoDB Connection Failed:", e)

db = client["MindFeed_Sample"]
saved_articles_collection = db["savedArticles"]

@app.route("/save-article", methods=["POST"])
def save_article():
    try:
        data = request.json
        user_id = data["userId"]
        article = data["article"]

        # Save the article as a single document
        saved_articles_collection.insert_one({
            "user_id": user_id,
            "article": article
        })

        return jsonify({"message": "Article saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete-article", methods=["POST"])
def delete_article():
    try:
        data = request.json
        user_id = data["userId"]
        article = data["article"]

        # Delete the article from the user's collection
        saved_articles_collection.delete_one({
            "user_id": user_id,
            "article.url": article["url"]  # Match by URL
        })

        return jsonify({"message": "Article deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-saved-articles", methods=["GET"])
def get_saved_articles():
    try:
        user_id = request.args.get("user_Id")
        saved_articles = saved_articles_collection.find({"user_id": user_id})

        articles = []
        for article in saved_articles:
            articles.append(article["article"])

        return jsonify({"savedArticles": articles}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "<h1>Server is Running</h1>"


@app.route("/routes", methods=["GET"])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "url": str(rule)
        })
    return jsonify(routes)


if __name__ == "__main__":
    app.run(debug=True)