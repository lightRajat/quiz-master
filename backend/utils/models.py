from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, ForeignKey, UniqueConstraint, CheckConstraint
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_joined = db.Column(db.Date, default=lambda: datetime.utcnow().date(), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    date_account_deleted = db.Column(db.Date, nullable=True)
    qualification = db.Column(db.String(255), nullable=True)
    dob = db.Column(db.Date, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    __table_args__ = (UniqueConstraint('subject_id', 'name', name="unique_chapter"), )

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer, ForeignKey('chapter.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=True)
    option_d = db.Column(db.String(255), nullable=True)
    correct_option = db.Column(Enum('a', 'b', 'c', 'd', name='correct_option_enum'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    __table_args__ = (UniqueConstraint('chapter_id', 'question', name="unique_question"), )

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scope = db.Column(Enum('subject', 'chapter', name='quiz_scope_enum'), nullable=False)
    chapter_id = db.Column(db.Integer, ForeignKey('chapter.id'), nullable=True)
    subject_id = db.Column(db.Integer, ForeignKey('subject.id'), nullable=True)
    time = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    __table_args__ = (
        CheckConstraint("scope IN ('chapter', 'subject')", name="check_valid_scope"),
        CheckConstraint("(scope = 'subject' AND subject_id IS NOT NULL AND chapter_id IS NULL) OR (scope = 'chapter' AND chapter_id IS NOT NULL AND subject_id IS NULL)", name="check_scope_ids"),
    )

class QuizQuestion(db.Model):
    quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'), nullable=False, primary_key=True)
    question_id = db.Column(db.Integer, ForeignKey('question.id'), nullable=False, primary_key=True)

    __table_args__ = (UniqueConstraint('quiz_id', 'question_id', name="unique_quiz_question"), )

class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'), nullable=False)
    date_attempted = db.Column(db.Date, default=lambda: datetime.utcnow().date(), nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_time = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)

class AttemptQuestion(db.Model):
    attempt_id = db.Column(db.Integer, ForeignKey('attempt.id'), nullable=False, primary_key=True)
    question_id = db.Column(db.Integer, ForeignKey('question.id'), nullable=False, primary_key=True)
    selected_answer = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)