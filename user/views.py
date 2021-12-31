from db.base import get_async_session
from db.user import User
from env import env
from sanic.blueprints import Blueprint
from sanic.response import json
from sanic_jwt import protected

bp = Blueprint("user", url_prefix="api/user/")


@bp.route("/add_user", methods=["POST"])
async def add_user(request):
    if request.method == "POST":
        async with get_async_session(env=env) as session:
            result = await User.add_user(session,
                                         request.json["email"],
                                         request.json["username"],
                                         request.json["password"])
            if result:
                return json({"status": "success"})
            else:
                return json({"status": "failure"})
    else:
        return json({"error": "invalid request"})


@bp.route("/delete_user", methods=["POST"])
async def add_user(request):
    if request.method == "POST":
        async with get_async_session(env=env) as session:
            result = await User.delete_user(session,
                                            request.json["email"])
            if result:
                return json({"status": "success"})
            else:
                return json({"status": "failure"})
    else:
        return json({"error": "invalid request"})


@bp.route("/protected")
@protected()
async def protected(request):
    return json({"message": "protected"})


@bp.route("/hello")
async def hello(request):
    return json({"message": "hello"})
