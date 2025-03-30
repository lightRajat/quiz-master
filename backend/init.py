from flask import Flask
from utils.models import *
import csv
import os, shutil
from utils.commons import get_date_from_string
from getpass import getpass
import json

def initialize_database():
    with app.app_context():
        db.create_all()

def add_sample_data():
    sample_folder = "data/sample-data"
    with app.app_context():
        with open(f'{sample_folder}/user.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                date_account_deleted = None if row[6] == '' else get_date_from_string(row[6])
                qualification = None if row[7] == '' else row[7]
                dob = None if row[8] == '' else get_date_from_string(row[8])
                profile_pic = None if row[5] == '' else row[5]

                user = User(
                    name = row[0],
                    email = row[1],
                    username = row[2],
                    date_joined = get_date_from_string(row[4]),
                    profile_pic = profile_pic,
                    date_account_deleted = date_account_deleted,
                    qualification = qualification,
                    dob = dob
                )
                user.set_password(row[3])
                db.session.add(user)
        
        with open(f'{sample_folder}/subject.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                name = row[0]
                description = row[1] if row[1] != '' else None

                subject = Subject(
                    name = name,
                    description = description
                )

                db.session.add(subject)
        db.session.commit()
        
        with open(f'{sample_folder}/chapter.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                subject_name = row[0]
                name = row[1]
                description = row[2] if row[2] != '' else None

                subject = Subject.query.filter_by(name = subject_name).first()
                
                chapter = Chapter(
                    subject_id = subject.id,
                    name = name,
                    description = description
                )

                db.session.add(chapter)
        db.session.commit()

        with open(f'{sample_folder}/question.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                chapter_name = row[1]
                question_text = row[2]
                option_a = row[3]
                option_b = row[4]
                option_c = row[5] if row[5] != '' else None
                option_d = row[6] if row[6] != '' else None
                correct_option = row[7]
                score = int(row[8])

                chapter = Chapter.query.filter_by(name = chapter_name).first()

                question = Question(
                    chapter_id = chapter.id,
                    question = question_text,
                    option_a = option_a,
                    option_b = option_b,
                    option_c = option_c,
                    option_d = option_d,
                    correct_option = correct_option,
                    score = score
                )

                db.session.add(question)
        
        with open(f'{sample_folder}/quiz.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                scope = row[1]
                chapter_name = row[2]
                subject_name = row[3]
                time = int(row[4])
                description = row[5] if row[5] != '' else None

                if scope == 'chapter':
                    chapter_id = Chapter.query.filter_by(name = chapter_name).first().id
                    subject_id = None
                else:
                    chapter_id = None
                    subject_id = Subject.query.filter_by(name = subject_name).first().id

                quiz = Quiz(
                    scope = scope,
                    chapter_id = chapter_id,
                    subject_id = subject_id,
                    time = time,
                    description = description
                )

                db.session.add(quiz)
        db.session.commit()
        
        with open(f'{sample_folder}/quiz_question.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                quiz_id = int(row[0])
                question_id = int(row[1])

                quiz_question = QuizQuestion(
                    quiz_id = quiz_id,
                    question_id = question_id,
                )

                db.session.add(quiz_question)
        
        with open(f'{sample_folder}/quiz_attempt.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                user_name = row[0]
                quiz_id = int(row[1])
                date_attempted = get_date_from_string(row[2])
                time_taken = int(row[3])
                score = int(row[4])

                user = User.query.filter_by(username = user_name).first()
                quiz = Quiz.query.get(quiz_id)
                
                quiz_attempt = Attempt(
                    user_id = user.id,
                    quiz_id = quiz_id,
                    date_attempted = date_attempted,
                    time_taken = time_taken,
                    score = score,
                    total_time = quiz.time,
                    total_score = score,
                )

                db.session.add(quiz_attempt)
        db.session.commit()
    
    add_sample_binaries()

def add_sample_binaries():
    src_folder = "data/sample-data/profile-pics"
    dest_folder = "data/profile-pics"

    for file_name in os.listdir(src_folder):
        src_path = os.path.join(src_folder, file_name)
        dest_path = os.path.join(dest_folder, file_name)

        shutil.copy(src_path, dest_path)

def add_mail_creds():
    email = input("Mail Username: ")
    password = getpass("Enter Password: ")
    mail_creds = {"email": email, "password": password}

    with open("data/mail-creds.json", "w") as f:
        f.write(json.dumps(mail_creds))

# check if already initialized
if os.path.exists('data/data.db'):
    print("Project already initialized\nGo run server.py now\n\n")
    exit(0)

app = Flask(__name__)
db_path = os.path.join(os.getcwd(), 'data/data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

initialize_database()
add_sample_data()
add_mail_creds()

print("Project initialized!\nRun server.py now\n\n")