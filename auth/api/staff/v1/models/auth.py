from flask_restx import fields

from api import api

CheckTokenModel = api.model("CheckTokenModel", {"token": fields.String(required=True)})

CheckTokenResponseModel = api.model(
    "CheckTokenResponseModel",
    {
        "user_id": fields.String(),
        "first_name": fields.String(),
        "last_name": fields.String(),
    },
)
