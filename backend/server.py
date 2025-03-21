from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    print(data)
    return jsonify({'message': "Login Success"})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    image_name = request.files['image'].filename
    print(data, image_name)
    
    return jsonify({'message': 'Registered successfully'})

if __name__ == '__main__':
    app.run(debug=True)