from flask_restful import Resource
from utils import models
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.commons import get_admin_creds

class SubjectApi(Resource):
    def get(self):
        results = models.Subject.query.all()
        all_subjects = []
        for result in results:
            subject = {
                'id': result.id,
                'name': result.name,
                'description': result.description
            }
            all_subjects.append(subject)
        
        return {'subject': all_subjects}, 200

class ChapterApi(Resource):
    def get(self):
        subject_id = request.args.get('subject_id')

        if subject_id:
            results = models.Chapter.query.filter_by(subject_id = subject_id).all()
        else:
            results = models.Chapter.query.all()
        
        chapters = []
        for result in results:
            chapter = {
                'id': result.id,
                'subject_id': result.subject_id,
                'name': result.name,
                'description': result.description
            }
            chapters.append(chapter)
        
        return {'chapters': chapters}, 200

class QuestionApi(Resource):
    def get(self):
        """Fetch questions, optionally filtered by chapter_id"""

        chapter_id = request.args.get('chapter_id')

        if chapter_id:
            results = models.Question.query.filter_by(chapter_id = chapter_id).all()
        else:
            results = models.Question.query.all()
        
        questions = []
        for result in results:
            question = {
                'id': result.id,
                'chapter_id': result.chapter_id,
                'question': result.question,
                'option_a': result.option_a,
                'option_b': result.option_b,
                'option_c': result.option_c,
                'option_d': result.option_d,
                'correct_option': result.correct_option,
                'score': result.score
            }
            questions.append(question)
        
        return {'questions': questions}, 200

class QuizApi(Resource):
    def get(self):
        """Fetch quizzes, optionally filtered by either chapter_id or subject_id (but not both)"""
        chapter_id = request.args.get('chapter_id')
        subject_id = request.args.get('subject_id')

        if chapter_id and subject_id:
            return {'status': 'failed', 'info': 'Provide only one filter: chapter_id or subject_id, but not both'}, 400

        if chapter_id:
            results = models.Quiz.query.filter_by(chapter_id=chapter_id).all()
        elif subject_id:
            results = models.Quiz.query.filter_by(subject_id=subject_id).all()
        else:
            results = models.Quiz.query.all()

        quizzes = []
        for result in results:
            quiz = {
                'id': result.id,
                'scope': result.scope,
                'chapter_id': result.chapter_id,
                'subject_id': result.subject_id,
                'time': result.time,
                'description': result.description
            }
            quizzes.append(quiz)

        return {'quizzes': quizzes}, 200

class QuizQuestionApi(Resource):
    """Fetch all quiz questions or filter by quiz_id (optional)"""
    def get(self):
        quiz_id = request.args.get('quiz_id')

        if quiz_id:
            results = models.QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
        else:
            results = models.QuizQuestion.query.all()

        quiz_questions = []
        for result in results:
            quiz_question = {
                'id': result.id,
                'quiz_id': result.quiz_id,
                'question_id': result.question_id,
                'order': result.order
            }
            quiz_questions.append(quiz_question)

        return {'quiz_questions': quiz_questions}, 200

class UserApi(Resource):
    @jwt_required()
    def get(self, user_id: int):
        token_user_id = get_jwt_identity()
        
        if token_user_id == get_admin_creds()['username']:
            result = models.User.query.get(user_id)
            if not result:
                return {'status': 'failed', 'info': "User not found"}, 404
        else:
            result = models.User.query.get(token_user_id)
            if result.id != user_id:
                return {'status': 'failed', 'info': "not authorized"}, 403

        user = {
            'id': result.id,
            'name': result.name,
            'email': result.email,
            'username': result.username,
            'date_joined': result.date_joined,
            'profile_pic': result.profile_pic,
            'qualification': result.qualification,
            'dob': result.dob,
            'date_account_deleted': result.date_account_deleted
        }

        return user, 200
        
class QuizAttemptApi(Resource):
    @jwt_required()
    def get(self, user_id):
        token_user_id = get_jwt_identity()

        if token_user_id == get_admin_creds()['username']:
            user = models.User.query.get(user_id)
            if not user:
                return {'status': 'failed', 'info': "User not found"}, 404
        else:
            if token_user_id != user_id:
                return {'status': 'failed', 'info': "Not authorized"}, 403
        
        results = models.QuizAttempt.query.filter_by(user_id=user_id).all()

        quiz_attempts = []
        for result in results:
            quiz_attempts.append({
                'id': result.id,
                'quiz_id': result.quiz_id,
                'date_attempted': result.date_attempted,
                'time_taken': result.time_taken,
                'score': result.score
            })

        return {'quiz_attempts': quiz_attempts}, 200