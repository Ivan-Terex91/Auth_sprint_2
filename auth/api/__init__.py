from flask_restx import Api

from core.exceptions import AuthError, EmailUsedError, NotFound

api = Api(title="Auth")


@api.errorhandler(NotFound)
def handle_not_found_error(error):
    return {"message": f"{error!s}"}, 404


@api.errorhandler(AuthError)
def handle_permission_error(error):
    return {"message": f"{error!s}"}, 401


@api.errorhandler(EmailUsedError)
def handle_email_used_error(error):
    return {"message": f"{error}"}, 409
