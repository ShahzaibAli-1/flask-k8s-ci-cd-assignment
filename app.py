from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Service is running'})


@app.route('/ready')
def readiness_check():
    """Readiness check endpoint."""
    return jsonify({'status': 'ready', 'message': 'Service is ready to accept traffic'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
