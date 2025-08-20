from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Flask Docker Demo",
        "status": "success"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy"
    })

if __name__ == '__main__':
    # Run on all interfaces (0.0.0.0) to be accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)