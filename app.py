from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"msg": "BC4M"}), 200

@app.route('/health', methods=['GET'])
def health():
    # Uygulamanin sagligini kontrol eden endpoint
    return jsonify({"health": "ok"}), 200

@app.route('/', methods=['POST'])
def echo_data():
    # Bodyde gelen datayi aynen geri dondurur
    data = request.get_json()
    return jsonify(data), 200

if __name__ == '__main__':
    # Flask uygulamamizi 0.0.0.0 IP ve 5000 portunda calistirir
    app.run(host='0.0.0.0', port=5000)