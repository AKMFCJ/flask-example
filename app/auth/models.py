# -*- coding: utf-8 -*-
# Created by AKM_FAN@163.com on 2017/11/6

import datetime
# JSON web token的库
import jwt

from app.server import app, db, bcrypt


class User(db.Model):
    """ User Model """
    __talbename__ = 'sys_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255), nullable=False, default='')
    registered_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    icon_url = db.Column(db.String, nullable=False, default='')
    # o 停用 1 正常
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, email, password, display_name='', icon_url=''):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.display_name = display_name
        self.icon_url = icon_url
        self.status = 1

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token 常用语Restful  API或跨域访问
        :param user_id:
        :return: string
        """

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=50),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get("SECRET_KEY"),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def __repr__(self):
        return '<User: %s>' % self.display_name

    def check_password(self,):
        pass

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """ Token Model for storing JWT tokens """
    __tablename__ = 'sys_blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}>'.format(self.token)

    @staticmethod
    def check_blakclist(auth_token):
        """ check whether auth token has been blacklisted """

        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        return False
