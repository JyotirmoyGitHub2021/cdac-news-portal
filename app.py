import os
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)

database_mock = [
    {"id": 1, "title": "দূরদর্শন কেন্দ্র কলকাতা নিয়োগ ২০২৬", "category": "West Bengal Jobs"},
    {"id": 2, "title": "সি-ড্যাক অল ইন্ডিয়া রিক্রুটমেন্ট ২০২৬", "category": "IT Jobs"}
]

# ১. টোকেন ভেরিফাই করার সিকিউরিটি ডেকোরেটর (M.Tech লেভেল সিকিউরিটি)
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        # আমরা একটি ডেমো সিক্রেট টোকেন ব্যবহার করছি
        if not token or token != "SecretAdminToken123":
            return jsonify({"status": "error", "message": "Unauthorized! আপনি অ্যাডমিন নন।"}), 401
        return f(*args, **kwargs)
    return decorated

# ২. অ্যাডমিন লগইন ভেরিফিকেশন এপিআই
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # এখানে আপনার গোপন ইউজারনেম এবং পাসওয়ার্ড সেট করা হলো
    if username == "admin" and password == "cdac2026":
        return jsonify({"status": "success", "token": "SecretAdminToken123"})
    else:
        return jsonify({"status": "error", "message": "ভুল ইউজারনেম বা পাসওয়ার্ড!"}), 401

# ৩. খবর রিড (সবাই পারবে) এবং ইনসার্ট (শুধু অ্যাডমিন পারবে)
@app.route('/news', methods=['GET', 'POST'])
def handle_news():
    if request.method == 'POST':
        # টোকেন চেক করার ফাংশন ম্যানুয়ালি কল করা হলো
        token = request.headers.get('Authorization')
        if token != "SecretAdminToken123":
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
            
        new_data = request.json
        new_id = len(database_mock) + 1
        new_article = {"id": new_id, "title": new_data.get('title'), "category": new_data.get('category')}
        database_mock.append(new_article)
        return jsonify({"status": "success", "message": "News added successfully!"})
    
    return jsonify({"status": "success", "data": database_mock})

# ৪. খবর ডিলিট (শুধু অ্যাডমিন পারবে)
@app.route('/news/<int:article_id>', methods=['DELETE'])
@admin_required
def delete_news(article_id):
    global database_mock
    database_mock = [item for item in database_mock if item['id'] != article_id]
    return jsonify({"status": "success", "message": "News deleted successfully!"})

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory(os.getcwd(), 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
