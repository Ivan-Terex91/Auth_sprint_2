from flask_restx import fields

from api import api
from core.enums import Roles

ResponseGetUserRoles = api.model("ResponseGetUserRoles", {"roles": fields.String(required=True)})

RoleModel = api.model(
    "RoleModel",
    {
        "user_id": fields.String(required=True, as_uuid=True),
        "role_title": fields.String(required=True, enum=[role.value for role in Roles]),
    },
)