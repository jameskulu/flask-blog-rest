from flask import Flask
import json
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from db import db
from resources.users import Register, Login, ActivateAccount, ForgotPassword, ResetPassword, LoggedInUser
from config import postgresqlConfig
from models.users import UserModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db, compare_type=True)
app.config["JWT_SECRET_KEY"] = "asdajjk3b43kjb4k34b"

jwt = JWTManager(app)
api = Api(app)

from models import users


# @app.before_first_request
# def create_tables():
#     from app.db import db
#     db.init_app(app)
#     db.create_all()

# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=json.loads(identity).get('id')).one_or_none()

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(ActivateAccount, '/activate-account')
api.add_resource(ForgotPassword, '/forgot-password')
api.add_resource(ResetPassword, '/reset-password')
api.add_resource(LoggedInUser, '/user')

if __name__ == '__main__':
    app.run(debug=True)