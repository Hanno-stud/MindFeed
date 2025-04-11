#We will create two Flask endpoints: 
# 1. for saving articles and 
# 2. for deleting articles.

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["news_database"]
saved_articles_collection = db["saved_articles"]

@app.route("/save-article", methods=["POST"])
def save_article():
    try:
        data = request.json
        user_id = data["userId"]
        article = data["article"]

        # Save the article as a single document in the user's collection
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
            "article.title": article["title"]  # Match by title
        })

        return jsonify({"message": "Article deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)