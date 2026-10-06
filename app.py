import os
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ডেমো ডেটাবেস
database_mock = [
    {"id": 1, "title": "দূরদর্শন কেন্দ্র কলকাতা নিয়োগ ২০২৬", "category": "West Bengal Jobs"},
    {"id": 2, "title": "সি-ড্যাক অল ইন্ডিয়া রিক্রুটমেন্ট ২০২৬", "category": "IT Jobs"}
]

# ১. খবর রিড (GET) এবং নতুন খবর ইনসার্ট (POST) করার রুট
@app.route('/news', methods=['GET', 'POST'])
def handle_news():
    if request.method == 'POST':
        new_data = request.json
        new_id = len(database_mock) + 1
        new_article = {
            "id": new_id,
            "title": new_data.get('title'),
            "category": new_data.get('category')
        }
        database_mock.append(new_article)
        print(f"\n[LOG]: নতুন খবর যুক্ত হয়েছে -> {new_article['title']}")
        return jsonify({"status": "success", "message": "News added successfully!"})
    
    return jsonify({"status": "success", "data": database_mock})

# ২. খবর ডিলিট (DELETE) করার নতুন এপিআই রুট
@app.route('/news/<int:article_id>', methods=['DELETE'])
def delete_news(article_id):
    global database_mock
    # নির্দিষ্ট ID-র খবরটি খুঁজে বের করে তালিকা থেকে বাদ দেওয়া
    initial_length = len(database_mock)
    database_mock = [item for item in database_mock if item['id'] != article_id]
    
    if len(database_mock) < initial_length:
        print(f"\n[LOG]: ID {article_id} নম্বরের খবরটি ডিলিট করা হয়েছে।")
        return jsonify({"status": "success", "message": "News deleted successfully!"})
    else:
        return jsonify({"status": "error", "message": "Article not found!"}), 404

# ৩. ফ্রন্টএন্ড সাপ্লাই করার রুট
@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory(os.getcwd(), 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
