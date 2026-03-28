from flask import Flask, request, jsonify

app = Flask(__name__)
latest_sms = {"body": "SMS hin jiru", "from": "Unknown"}

@app.route('/sms', methods=['POST'])
def receive_sms():
    global latest_sms
    data = request.json
    latest_sms = {"body": data.get('body'), "from": data.get('from')}
    print(f"📩 SMS Haaraa: {latest_sms['body']}")
    return jsonify({"status": "success"}), 200

@app.route('/get_latest', methods=['GET'])
def get_latest():
    return jsonify(latest_sms), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
