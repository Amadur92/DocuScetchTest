from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]

@app.route('/api/data', methods=['GET', 'POST', 'PUT'])
def handle_data():
    if request.method == 'GET':
        key = request.args.get('key')
        data = db.data.find_one({'key': key})
        return jsonify(data) if data else jsonify({"message": "Key not found"}), 404

    if request.method == 'POST':
        data = request.get_json()
        db.data.insert_one(data)
        return jsonify({"message": "Data created successfully"}), 201

    if request.method == 'PUT':
        key = request.args.get('key')
        new_value = request.get_json().get('value')
        result = db.data.update_one({'key': key}, {'$set': {'value': new_value}})
        return jsonify({"message": "Data updated successfully"}), 200 if result.modified_count > 0 else 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
