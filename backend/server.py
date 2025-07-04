from utils.imports import *

app = Flask(__name__)

# Mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
mail_creds = commons.get_mail_creds()
app.config['MAIL_USERNAME'] = mail_creds['email']
app.config['MAIL_DEFAULT_SENDER'] = mail_creds['email']
app.config['MAIL_PASSWORD'] = mail_creds['password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail.init_app(app)

# Database
db_path = os.path.join(os.getcwd(), 'data/data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    @event.listens_for(db.engine, "connect")
    def enable_foreign_key_constraint(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.close()

# Jwt Security
app.config['SECRET_KEY'] = "rajat-vue-app"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

# Api
app.config['UPLOADS_FOLDER'] = 'data/profile-pics'
api = Api(app)
api.add_resource(routes.SubjectApi, '/subjects', '/subject/<int:id>')
api.add_resource(routes.ChapterApi, '/chapters', '/chapter/<int:id>')
api.add_resource(routes.QuestionApi, '/questions', '/question/<int:id>')
api.add_resource(routes.QuizApi, '/quizzes', '/quiz/<int:id>')
api.add_resource(routes.QuizQuestionApi, '/quiz-questions')
api.add_resource(routes.UserApi, '/users', '/user/<int:user_id>')
api.add_resource(routes.AttemptApi, '/attempts', '/attempt/<int:id>')
api.add_resource(routes.AttemptQuestionApi, '/attempt-questions')

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
                return Response.USER_LOGGED(user.id, create_access_token(identity=user.id))
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

@app.route('/admin-creds', methods=['GET', 'POST'])
@jwt_required()
def admin_creds():
    token_user_id = get_jwt_identity()
    if token_user_id != commons.get_admin_creds()['username']:
        return Response.UNAUTHORIZED

    if request.method == 'GET':
        return Response.RESOURCE_FETCHED(commons.get_admin_creds())
    else:
        commons.update_admin_password(request.get_json()['password'])
        return Response.PROFILE_UPDATED

@app.route('/uploads/<string:path>')
@jwt_required()
def send_image_file(path: str):
    token_user_id = get_jwt_identity()

    if token_user_id == commons.get_admin_creds()['username']:
        if path not in os.listdir(app.config['UPLOADS_FOLDER']):
            return Response.RESOURCE_NOT_FOUND
    else:
        user = User.query.get(token_user_id)
        if user.profile_pic != path:
            return Response.UNAUTHORIZED

    return send_file(f"{app.config['UPLOADS_FOLDER']}/{path}")

if __name__ == '__main__':
    app.run(debug=True)