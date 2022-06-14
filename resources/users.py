import secrets
from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt_identity
from models.users import UserModel
from util.encoder import AlchemyEncoder
import json
from werkzeug.security import  generate_password_hash, check_password_hash
from util.logz import create_logger


class Login(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('email', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = Login.parser.parse_args()
        email = data['email']
        password = data['password']

        user = UserModel.query.filter_by(email=email).one_or_none()
        if not user or not user.check_password(password):
            return {'message': 'Invalid Credentials.'}, 401
        access_token = create_access_token(
            identity=json.dumps(user, cls=AlchemyEncoder))
        return jsonify(access_token=access_token)


class Register(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()
    parser.add_argument('first_name', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('last_name', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('email', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = Register.parser.parse_args()
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        email = data['email']
        password = data['password']

        if UserModel.find_by_username(username):
            return {'message': 'User with that username already exists'}, 400

        if UserModel.find_by_email(email):
            return {'message': 'User with that email already exists'}, 400

        token = secrets.token_hex(16)
        user = UserModel(first_name, last_name, username, email, generate_password_hash(password))
        user.email_token = token
        user.save_to_db()

        return {'message': 'User has been created successfully.'}, 201


class ActivateAccount(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = ActivateAccount.parser.parse_args()
        token = data['token']
        
        user = UserModel.query.filter_by(email_token=token).first()

        if not user:
            return {'message': 'Invalid Token'}, 400

        user.email_token = None
        user.is_verified = True
        user.save_to_db()

        return {'message': 'Account has been successfully activated.'}, 200
    

class ForgotPassword(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = ForgotPassword.parser.parse_args()
        email = data['email']
        
        user = UserModel.find_by_email(email)
        
        if not user:
            return {'message': 'User not found'}, 400
        
        token = secrets.token_hex(16)

        user.reset_token = token
        user.save_to_db()

        return {'message': 'Reset email password has been sent.'}, 200


class ResetPassword(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()
    parser.add_argument('token', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = ResetPassword.parser.parse_args()
        token = data['token']
        password = data['password']
        
        user = UserModel.query.filter_by(reset_token=token).first()
        
        if not user:
            return {'message': 'Invalid token'}, 400
        
        user.reset_token = None
        user.password = generate_password_hash(password)
        user.save_to_db()

        return {'message': 'Password has been changed.'}, 200
    

class LoggedInUser(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required() 
    def get(self):
        return jsonify(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
        )