from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def login():
    return jsonify({'name': "Rajat"})

if __name__ == '__main__':
    app.run(debug=True)