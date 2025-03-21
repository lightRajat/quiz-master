from utils.imports import *

app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Jwt Security
jwt = JWTManager(app)

# Api
api = Api(app)
api.add_resource(routes.SubjectApi, '/subjects')
api.add_resource(routes.ChapterApi, '/chapters')
api.add_resource(routes.QuestionApi, '/questions')
api.add_resource(routes.QuizApi, '/quizzes')
api.add_resource(routes.QuizQuestionApi, '/quiz-questions')
api.add_resource(routes.UserApi, '/user/<int:user_id>')
api.add_resource(routes.QuizAttemptApi, '/user/<int:user_id>/quiz-attempts')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    return_message = {"status": ""}
    return_code = 200

    admin_creds = commons.get_admin_creds()

    if email == admin_creds['username']:
        if password == admin_creds['password']:
            return_message['status'] = 'success'
            return_message['user'] = 'admin'
            return_message['token'] = create_access_token(identity='admin')

        else:
            return_message['status'] = 'failed'
            return_message['info'] = 'incorrect password'
            return_code = 401
    else:
        user = User.query.filter(or_(User.username == email, User.email == email)).first()
        if user:
            if user.check_password(password):
                return_message['status'] = 'success'
                return_message['user'] = user.username
                return_message['token'] = create_access_token(identity=user.id)
            else:
                return_message['status'] = 'failed'
                return_message['info'] = 'Incorrect Password'
                return_code = 401
        else:
            return_message['status'] = 'failed'
            return_message['info'] = 'User Not Found'
            return_code = 404
    
    return jsonify(return_message), return_code

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form

    user = User.query.filter(or_(User.username == data['email'], User.email == data['email'])).first()
    if user:
        return jsonify({'status': "failed", 'info': "user already exists"}), 409

    user = User(
        name = data['name'],
        email = data['email'],
        username = commons.get_username_from_email(data['email']),
        qualification = data['qualification'] if data['qualification'] else None,
        dob = commons.get_date_from_string(data['dob']) if data['dob'] else None
    )
    user.set_password(data['password'])
    print(request.files['image'])
    if request.files['image'].filename:
        commons.set_profile_pic(request.files['image'], user)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'status': 'success', 'user': user.username}), 201

if __name__ == '__main__':
    app.run(debug=True)