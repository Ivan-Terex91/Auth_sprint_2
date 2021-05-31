from flask import g
from flask_restx import Namespace

from api.staff.v1.models.auth import CheckTokenModel, CheckTokenResponseModel
from core.api import Resource

ns = Namespace("Staff Auth Namespace")


@ns.route("/check_token/")
class CheckToken(Resource):
    @ns.expect(CheckTokenModel, validate=True)
    @ns.marshal_with(CheckTokenResponseModel, code=200)
    def post(self):
        token = self.api.payload["token"]
        access_token = self.services.token_service.decode_access_token(token)

        return {
            "user_id": str(access_token.user_id),
            "first_name": "first",
            "last_name": "last",
        }
