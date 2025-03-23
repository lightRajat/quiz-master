from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.commons import get
from utils.http_response import Response
from utils.mixins import *

class SubjectApi(Resource, UpdateMixin, PostMixin, DeleteMixin):
    def get(self):
        results = models.Subject.query.all()
        subjects = []
        for result in results:
            subject = {
                'id': result.id,
                'name': result.name,
                'description': result.description
            }
            subjects.append(subject)
        
        return Response.RESOURCE_FETCHED(subjects)
    
    def post(self):
        return super().post(models.Subject)
    
    def delete(self, id):
        return super().delete(models.Subject, id)

    def put(self, id):
        return super().put(models.Subject, id)

class ChapterApi(Resource, UpdateMixin, PostMixin, DeleteMixin):
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
        
        return Response.RESOURCE_FETCHED(chapters)
    
    def post(self):
        return super().post(models.Chapter)
    
    def delete(self, id):
        return super().delete(models.Chapter, id)

    def put(self, id):
        return super().put(models.Chapter, id)

class QuestionApi(Resource, UpdateMixin, PostMixin, DeleteMixin):
    def get(self):
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
        
        return Response.RESOURCE_FETCHED(questions)
    
    def post(self):
        return super().post(models.Question)
    
    def delete(self, id):
        return super().delete(models.Question, id)
    
    def put(self, id):
        return super().put(models.Question, id)

class QuizApi(Resource, UpdateMixin, PostMixin, DeleteMixin):
    def get(self):
        chapter_id = request.args.get('chapter_id')
        subject_id = request.args.get('subject_id')

        if chapter_id and subject_id:
            return Response.INVALID_PARAMETERS

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

        return Response.RESOURCE_FETCHED(quizzes)
    
    def post(self):
        return super().post(models.Quiz)
    
    def delete(self, id):
        return super().delete(models.Quiz, id)
    
    def put(self, id):
        return super().put(models.Quiz, id)

class QuizQuestionApi(Resource, UpdateMixin, PostMixin, DeleteMixin):
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

        return Response.RESOURCE_FETCHED(quiz_questions)
    
    def post(self):
        return super().post(models.QuizQuestion)
    
    def delete(self, id):
        return super().delete(models.QuizQuestion, id)
    
    def put(self, id):
        return super().put(models.QuizQuestion, id)

class UserApi(Resource):
    @jwt_required()
    def get(self, user_id: int):
        token_user_id = get_jwt_identity()
        
        if token_user_id == 'admin':
            result = models.User.query.get(user_id)
            if not result:
                return Response.USER_NOT_FOUND
        else:
            result = models.User.query.get(token_user_id)
            if result.id != user_id:
                return Response.UNAUTHORIZED

        user = {
            'id': result.id,
            'name': result.name,
            'email': result.email,
            'username': result.username,
            'date_joined': get(result.date_joined),
            'qualification': result.qualification,
            'dob': get(result.dob),
            'date_account_deleted': get(result.date_account_deleted),
            'profile_pic': ''
        }
        if result.profile_pic:
            user['profile_pic'] = f"uploads/{result.profile_pic}"

        return Response.RESOURCE_FETCHED(user)
        
class QuizAttemptApi(Resource):
    @jwt_required()
    def get(self, user_id):
        token_user_id = get_jwt_identity()

        if token_user_id == 'admin':
            user = models.User.query.get(user_id)
            if not user:
                return Response.USER_NOT_FOUND
        else:
            if token_user_id != user_id:
                return Response.UNAUTHORIZED
        
        results = models.QuizAttempt.query.filter_by(user_id=user_id).all()

        quiz_attempts = []
        for result in results:
            quiz_attempts.append({
                'id': result.id,
                'quiz_id': result.quiz_id,
                'date_attempted': get(result.date_attempted),
                'time_taken': result.time_taken,
                'score': result.score
            })

        return Response.RESOURCE_FETCHED(quiz_attempts)