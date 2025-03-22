from utils.imports import *

app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Jwt Security
app.config['SECRET_KEY'] = "rajat-vue-app"
jwt = JWTManager(app)

# Api
app.config['UPLOADS_FOLDER'] = 'data/profile-pics'
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
    admin_creds = commons.get_admin_creds()

    if email == admin_creds['username']:
        if password == admin_creds['password']:
            return Response.USER_LOGGED('admin', create_access_token(identity='admin'))

        else:
            return Response.INCORRECT_PASSWORD
    else:
        user = User.query.filter(or_(User.username == email, User.email == email)).first()
        if user:
            if user.check_password(password):
                return Response.USER_LOGGED(user.username, create_access_token(identity=user.id))
            else:
                return Response.INCORRECT_PASSWORD
        else:
            return Response.USER_NOT_FOUND

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form

    # if user already exists
    user = User.query.filter(or_(User.username == data['email'], User.email == data['email'])).first()
    if user or commons.get_username_from_email(data['email']) == 'admin':
        return Response.USER_ALREADY_EXISTS

    user = User(
        name = data['name'],
        email = data['email'],
        username = commons.get_username_from_email(data['email']),
        qualification = data['qualification'] if data['qualification'] else None,
        dob = commons.get_date_from_string(data['dob']) if data['dob'] else None
    )
    user.set_password(data['password'])
    if request.files['image'].filename:
        commons.save_profile_pic(request.files['image'], user)
    
    db.session.add(user)
    db.session.commit()
    
    return Response.USER_REGISTERED(user.username)

@app.route('/uploads/<string:path>')
@jwt_required()
def send_image_file(path: str):
    token_user_id = get_jwt_identity()

    if token_user_id == commons.get_admin_creds()['username']:
        if path not in os.listdir(app.config['UPLOADS_FOLDER']):
            return {'status': 'failed', 'info': "file not found"}, 404
    else:
        user = User.query.get(token_user_id)
        if user.profile_pic != path:
            return {'status': 'failed', 'info': "not authorized"}, 403

    return send_file(f"{app.config['UPLOADS_FOLDER']}/{path}")

if __name__ == '__main__':
    app.run(debug=True)