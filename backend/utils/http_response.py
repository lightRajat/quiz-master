from json import dumps

class Response:
    USER_NOT_FOUND = dumps({"status": "failed", "info": "User Not Found"}), 401
    INCORRECT_PASSWORD = dumps({"status": "failed", "info": "Incorrect Password"}), 401
    USER_ALREADY_EXISTS = dumps({"status": "failed", "info": "User Already Exists"}), 409
    RESOURCE_ALREADY_EXISTS = dumps({"status": "failed", "info": "Resource Already Exists"}), 409
    UNAUTHORIZED = dumps({"status": "failed", "info": "Unauthorized"}), 403
    INVALID_FOREIGN_KEY = dumps({"status": "failed", "info": "Invalid Foreign Key"}), 400
    INVALID_PARAMETERS = dumps({'status': 'failed', 'info': 'Invalid Query Paramters'}), 400
    INVALID_DATA = dumps({'status': 'failed', 'info': 'Invalid Data'}), 400
    RESOURCE_DELETED = dumps({'status': 'success', 'info': 'Resource Successfully Deleted'}), 200
    RESOURCE_NOT_FOUND = dumps({'status': 'failed', 'info': 'Resource Not Found'}), 404
    FOREIGN_KEY_DEPENDENT = dumps({'status': 'failed', 'info': 'Has Foreign Key Dependencies'}), 409
    RESOURCE_UPDATED = dumps({'status': 'success', 'info': 'Resource Successfully Updated'}), 200
    INTERNAL_SERVER_ERROR = dumps({'status': 'failed', 'info': 'Internal Server Error'}), 500
    QUESTIONS_UPDATED = dumps({'status': 'success', 'info': 'Questions Updated'}), 200
    PROFILE_UPDATED = dumps({'status': 'success', 'info': 'Profile Successfully Updated'}), 200
    EMAIL_ALREADY_EXISTS = dumps({'status': 'failed', 'info': 'Email or Username Already Exists'}), 409

    @staticmethod
    def USER_LOGGED(user, token):
        response = {
            'status': "success",
            'info': "User Successfully Logged In",
            'user': user,
            'token': token
        }
        return dumps(response), 200
    
    @staticmethod
    def USER_REGISTERED(user):
        response = {
            'status': "success",
            'info': "User Successfully Registered",
            'user': user
        }
        return dumps(response), 201
    
    @staticmethod
    def RESOURCE_FETCHED(resource_list):
        response = {
            'status': "success",
            'data': resource_list
        }
        response['info'] = "Resource Successfully Fetched" if resource_list else "No Resource Were Found"
        return dumps(response), 200

    @staticmethod
    def RESOURCE_CREATED(resource):
        response = {
            'status': "success",
            'data': resource,
            'info': "Resource Created Successfully",
        }
        return dumps(response), 201