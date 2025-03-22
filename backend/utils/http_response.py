from json import dumps

class Response:
    USER_NOT_FOUND = dumps({"status": "failed", "info": "User Not Found"}), 401
    INCORRECT_PASSWORD = dumps({"status": "failed", "info": "Incorrect Password"}), 401
    USER_ALREADY_EXISTS = dumps({"status": "failed", "info": "User Already Exists"}), 409

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