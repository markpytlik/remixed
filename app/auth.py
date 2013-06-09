
from app.client import GoogleClient
import app.base
from app.helper import Helper
import datetime
from datetime import date
from datetime import timedelta
from datetime import datetime
import requests
import thread

class LogoutHandler(app.base.BaseHandler):
	def check_xsrf_cookie(self):
		pass

	def get(self):
		self.logout()

class LoginHandler(app.base.BaseHandler):

	def check_xsrf_cookie(self):
		pass

	def post(self):
		passw = self.get_argument('Passwd', None)
		email = self.get_argument('Email', None)

		user = self.db.get("SELECT * from User WHERE email = %s", str(email))

		sesh = requests.Session()

		values = {
		        'service':'sj',
		        'Passwd' : passw,
		        'Email' : email
		}

		login_url = 'https://accounts.google.com/ClientLogin'
		user_login_params = dict()
		user_login_params['url'] = login_url
		user_login_params['headers'] = {'Content-Type' : 'application/x-www-form-urlencoded'}
		user_login_params['method'] = 'POST'
		user_login_params['data'] = values

		try:
		    user_login_resp = sesh.request(**user_login_params)
		except:
		    return self.resp({"message" : "Failed to login"}, False)

		ret = dict()
		ret['Auth'] = None

		print user_login_resp.text

		if "Info=WebLoginRequired" in user_login_resp.text:
			return self.resp({"message" : "Please visit https://accounts.google.com/DisplayUnlockCaptcha to allow access"}, False)

		for line in user_login_resp.text.split('\n'):
		    if '=' in line:
		        var, val = line.split('=', 1)
		        ret[var] = val

		if ret['Auth'] is None:
			return self.resp({"message" : "Login failed, sorry!"}, False)

		auth = ret['Auth']

		cookie_url = 'https://play.google.com/music/listen?hl=en&u=0'
		get_cookie_params = dict()
		get_cookie_params['method'] = 'GET'
		get_cookie_params['url'] = cookie_url
		get_cookie_params['headers'] = {'Authorization' : 'GoogleLogin auth='+ ret['Auth']}

		get_cookie_resp = sesh.request(**get_cookie_params)

		xt = None

		try:
			if get_cookie_resp.cookies['xt'] is None:
			    return self.resp( {"message" : "xt cookie not found"}, False )
			else:
			    xt = get_cookie_resp.cookies['xt']
		except:
			return self.resp({"message" : "XSRF Token not found - " + user_login_resp.text})
					
		if user is None:
		    user_id = self.db.execute("INSERT INTO User (email, auth, xt, sjaid, last_fetch) VALUES(%s, %s, %s, %s, UTC_TIMESTAMP)", 
		        email, 
		        auth, 
		        xt,
		        "")
		else:
		    user_id = self.db.execute("UPDATE User SET auth = %s, xt = %s, last_fetch = UTC_TIMESTAMP WHERE email = %s", auth, xt, email)

		if user_id is None:
		    return self.resp( {"message" : "Failed to query user"}, False)

		self.login(email)
		
		return self.resp({
		    'email' : email,
		    'xt' : xt,
		    'auth' : auth,
		    'message' : 'welcome, ' + email + ' you will be redirected shortly',
		    'next' : '/'
		}, True)		
