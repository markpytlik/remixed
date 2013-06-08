import tornado.web
from tornado.options import options
import hmac, sha
import base64
import json
from datetime import date, datetime, time, timedelta
import os
import hashlib
import mimetypes

from app.helper import Helper

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def sp(self):
        return self.application.sp

    def get_user_by_email(self, email):
        user = self.db.get("SELECT * FROM User WHERE email = %s", str(email))
        if user is None:
            return None
        return user

    def get_current_user(self):
        user_id = self.get_current_user_email()
        if not user_id: return None
        return self.get_user_by_email(user_id)

    def get_current_user_email(self):
        return self.get_secure_cookie("remixed_user")

    def login(self, email):
        self.set_secure_cookie("remixed_user", email)

    def logout(self):
        self.clear_cookie("remixed_user")
        self.redirect("/")

    def session_expired(self):
        user = self.get_current_user()
        if user is None:
            return True

        return True if datetime.now() > user.last_fetch + timedelta(days = 1) else False

    def resp(self, data, success = True):
        return Helper.resp_http(self, data, success)

    def clean_json_resp(self, data):
        return Helper.json_resp_only(self, data)
