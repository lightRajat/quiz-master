from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.http_response import Response
from flask import request
from utils.models import db
from sqlalchemy.exc import IntegrityError, StatementError

class UpdateMixin:
    @jwt_required()
    def put(self, model, resource_id):
        user = get_jwt_identity()
        if user != 'admin':
            return Response.UNAUTHORIZED

        resource = model.query.get(resource_id)

        if not resource:
            return Response.RESOURCE_NOT_FOUND

        data = request.get_json()

        try:
            for key, value in data.items():
                setattr(resource, key, value)
            db.session.commit()
            return Response.RESOURCE_UPDATED
        except IntegrityError as e:
            error_msg = str(e.orig)
            if 'FOREIGN KEY constraint failed' in error_msg:
                return Response.INVALID_FOREIGN_KEY
            elif 'UNIQUE constraint failed' in error_msg:
                return Response.RESOURCE_ALREADY_EXISTS
            else:
                return Response.INVALID_DATA
        except StatementError:
            return Response.INVALID_DATA
        except Exception as e:
            print(f"Error updating resource: {e}")
            return Response.INTERNAL_SERVER_ERROR
        finally:
            db.session.rollback()

class PostMixin:
    @jwt_required()
    def post(self, model):
        # check if admin
        user = get_jwt_identity()
        if user != 'admin':
            return Response.UNAUTHORIZED

        data = request.get_json()
        try:
            resource = model(**data)
            db.session.add(resource)
            db.session.commit()

            return Response.RESOURCE_CREATED
        except IntegrityError as e:
            error_msg = str(e.orig)
            if 'FOREIGN KEY constraint failed' in error_msg:
                return Response.INVALID_FOREIGN_KEY
            elif 'UNIQUE constraint failed' in error_msg:
                return Response.RESOURCE_ALREADY_EXISTS
            elif 'CHECK constraint failed' in error_msg:
                return Response.INVALID_DATA
            else:
                return Response.INVALID_DATA
        except StatementError:
            return Response.INVALID_DATA
        except Exception as e:
            print(f"Error creating resource: {e}")
            return Response.INTERNAL_SERVER_ERROR
        finally:
            db.session.rollback()

class DeleteMixin:
    @jwt_required()
    def delete(self, model, resource_id):
        user = get_jwt_identity()
        if user != 'admin':
            return Response.UNAUTHORIZED

        resource = model.query.get(resource_id)

        if not resource:
            return Response.RESOURCE_NOT_FOUND

        try:
            db.session.delete(resource)
            db.session.commit()
            return Response.RESOURCE_DELETED
        except IntegrityError:
            return Response.FOREIGN_KEY_DEPENDENT
        except Exception as e:
            print(f"Error deleting resource: {e}")
            return Response.INTERNAL_SERVER_ERROR
        finally:
            db.session.rollback()