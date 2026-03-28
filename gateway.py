from flask import Flask, request, jsonify

app = Flask(__name__)

# Bakka SMS itti kuufamu (Data Store)
latest_sms = {
    "body": "SMS hin jiru. Hordoffiin eegalameera...",
    "from": "Unknown"
}

@app.route('/')
def home():
    return "Gateway is Running on Codespaces!"

# SMS bilbila kee irraa dhufe simachuuf (Webhook)
@app.route('/sms', methods=['POST'])
def receive_sms():
    global latest_sms
    data = request.json
    if data:
        latest_sms['body'] = data.get('body', 'Kutaa duwwaa')
        latest_sms['from'] = data.get('from', 'Unknown Sender')
        print(f"📩 SMS Haaraa Galmeeffame: {latest_sms['body']}")
        return jsonify({"status": "success", "message": "SMS received"}), 200
    return jsonify({"status": "error", "message": "No data"}), 400

# Bot-ichi koodii kana dubbisuuf fayyadama
@app.route('/get_latest', methods=['GET'])
def get_latest():
    return jsonify(latest_sms), 200

if __name__ == '__main__':
    # Codespaces irratti port 5000 fayyadamna
    app.run(host='0.0.0.0', port=5000)
