from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.commons import get
from utils.http_response import Response
from utils.mixins import *

class SubjectApi(Resource, UpdateMixin, PostMixin, DeleteMixin):
    def get(self, id=None):
        if id:
            result = models.Subject.query.get(id)
            if not result:
                return Response.RESOURCE_NOT_FOUND
            subject = {
                'id': result.id,
                'name': result.name,
                'description': result.description
            }
            return Response.RESOURCE_FETCHED(subject)
        else:
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
    def get(self, id=None):
        if id:
            result = models.Chapter.query.get(id)
            if not result:
                return Response.RESOURCE_NOT_FOUND
            chapter = {
                'id': result.id,
                'subject_id': result.subject_id,
                'name': result.name,
                'description': result.description
            }
            return Response.RESOURCE_FETCHED(chapter)
        else:
            subject_id = request.args.get('subject_id')
            if subject_id:
                results = models.Chapter.query.filter_by(subject_id=subject_id).all()
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
    def get(self, id=None):
        if id:
            result = models.Question.query.get(id)
            if not result:
                return Response.RESOURCE_NOT_FOUND
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
            return Response.RESOURCE_FETCHED(question)
        else:
            chapter_id = request.args.get('chapter_id')
            if chapter_id:
                results = models.Question.query.filter_by(chapter_id=chapter_id).all()
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
    def get(self, id=None):
        if id:
            result = models.Quiz.query.get(id)
            if not result:
                return Response.RESOURCE_NOT_FOUND
            quiz = {
                'id': result.id,
                'scope': result.scope,
                'chapter_id': result.chapter_id,
                'subject_id': result.subject_id,
                'time': result.time,
                'description': result.description
            }
            return Response.RESOURCE_FETCHED(quiz)
        else:
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

class QuizQuestionApi(Resource):
    def get(self):
        quiz_id = request.args.get('quiz_id')

        if quiz_id:
            results = models.QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
        else:
            results = models.QuizQuestion.query.all()

        quiz_questions = []
        for result in results:
            quiz_question = {
                'quiz_id': result.quiz_id,
                'question_id': result.question_id,
            }
            quiz_questions.append(quiz_question)

        return Response.RESOURCE_FETCHED(quiz_questions)
    
    def post(self):
        data = request.get_json()

        # delete all previous associations
        models.db.session.execute(models.db.delete(models.QuizQuestion).where(models.QuizQuestion.quiz_id == data['quiz_id']))

        # add new associations
        for question_id in data['question_ids']:
            quiz_question = models.QuizQuestion(quiz_id=data['quiz_id'], question_id=question_id)
            models.db.session.add(quiz_question)
        models.db.session.commit()
        
        return Response.QUIZ_QUESTIONS_UPDATED

class UserApi(Resource):
    @jwt_required()
    def get(self, user_id: int = None):
        token_user_id = get_jwt_identity()
        
        # if admin
        if token_user_id == 'admin':
            # if requested for one user
            if user_id:
                result = models.User.query.get(user_id)
            else:
                results = models.User.query.all()
                users = []
                for result in results:
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
                    users.append(user)
                return Response.RESOURCE_FETCHED(users)
        else:
            # if requested for one user
            if user_id:
                # check if not requested for himself
                if user_id != token_user_id:
                    return Response.UNAUTHORIZED
                else:
                    result = models.User.query.get(user_id)
            else:
                return Response.UNAUTHORIZED

        if not result:
            return Response.USER_NOT_FOUND
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
        
class AttemptApi(Resource):
    @jwt_required()
    def get(self, id: int = None):
        token_user_id = get_jwt_identity()
        
        # if admin
        if token_user_id == 'admin':
            # if requested for attempt with key id
            if id:
                # check if exists
                result = models.Attempt.query.get(id)
                if result:
                    quiz_attempt = {
                        'id': result.id,
                        'quiz_id': result.quiz_id,
                        'user_id': result.user_id,
                        'date_attempted': get(result.date_attempted),
                        'time_taken': result.time_taken,
                        'score': result.score,
                        'total_time': result.total_time,
                        'total_score': result.total_score
                    }
                    return Response.RESOURCE_FETCHED(quiz_attempt)
                else:
                    return Response.RESOURCE_NOT_FOUND
            else:
                # if requested for one user
                user_id = request.args.get('user_id')
                if user_id:
                    results = models.Attempt.query.filter_by(user_id=user_id).all()
                else:
                    results = models.Attempt.query.all()
        else:
            # if requested for attempt with key id
            if id:
                # check auth
                result = models.Attempt.query.get(id)
                if result and result.user_id == token_user_id:
                    quiz_attempt = {
                        'id': result.id,
                        'quiz_id': result.quiz_id,
                        'user_id': result.user_id,
                        'date_attempted': get(result.date_attempted),
                        'time_taken': result.time_taken,
                        'score': result.score,
                        'total_time': result.total_time,
                        'total_score': result.total_score
                    }
                    return Response.RESOURCE_FETCHED(quiz_attempt)
                else:
                    return Resource.UNAUTHORIZED
            else:
                # if requested for one user
                user_id = request.args.get('user_id')
                if user_id:
                    # check auth
                    if token_user_id != user_id:
                        return Response.UNAUTHORIZED
                    else:
                        results = models.Attempt.query.filter_by(user_id=user_id).all()
                else:
                    return Response.UNAUTHORIZED

        quiz_attempts = []
        for result in results:
            quiz_attempt = {
                'id': result.id,
                'user_id': result.user_id,
                'quiz_id': result.quiz_id,
                'date_attempted': get(result.date_attempted),
                'time_taken': result.time_taken,
                'score': result.score,
                'total_time': result.total_time,
                'total_score': result.total_score
            }
            quiz_attempts.append(quiz_attempt)

        return Response.RESOURCE_FETCHED(quiz_attempts)
    
    def post(self):
        data = request.form
        try:
            resource = models.Attempt(**data)
            models.db.session.add(resource)
            models.db.session.commit()

            created_resource = {**data, 'id': resource.id, 'date_attempted': resource.date_attempted}
            return Response.RESOURCE_CREATED(created_resource)
        except IntegrityError as e:
            error_msg = str(e.orig)
            if 'FOREIGN KEY constraint failed' in error_msg:
                return Response.INVALID_FOREIGN_KEY
            else:
                return Response.INVALID_DATA
        except StatementError:
            return Response.INVALID_DATA
        except Exception as e:
            print(f"Error creating resource: {e}")
            return Response.INTERNAL_SERVER_ERROR
        finally:
            models.db.session.rollback()