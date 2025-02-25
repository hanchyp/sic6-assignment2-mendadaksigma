from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Koneksi ke MongoDB
uri = "mongodb+srv://mendadaksigma:gO4pAeOumqiYm7SM@cluster-mendadaksigma-s.uyl1v.mongodb.net/?appName=Cluster-MendadakSigma-SIC6"

try:
    client = MongoClient(uri)
    # Pilih database dan collection
    db = client['MendadakSigmaDatabase']
    collection = db['sensor_data']
    client.admin.command("ping")
except Exception as e:
    print("Gagal terhubung dengan MongoDB: ", e)

@app.route('/sensor', methods=['POST'])
def receive_sensor_data():
    data = request.json
    if not data:
        return jsonify({"error": "Datanya nggak ada kocak"}), 400

    try:
        collection.insert_one(data)
        return jsonify({"message": "Data berhasil dikirim!"}), 201
    except Exception as e:
        return jsonify({f"error": {e}}), 500
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)