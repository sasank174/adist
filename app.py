from flask import Flask, flash, redirect, render_template, session, request
from flask_mail import Mail, Message
import db
import tokens
import encrypt
import randad
from flask_recaptcha import ReCaptcha
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
mail= Mail(app)
app.secret_key = os.getenv('SECRET_KEY')
recaptcha = ReCaptcha(app=app)

app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY'),
    RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY'),
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)


db_connection = db.db_connect()

# =============================================================================================================

def mailing(tomail,username,token,no):
	if no == 1:
		x,y = "conformation Email","confirm_email"
	elif no == 2:
		x,y = "reset password","reset_password"
	try:
		app.config['MAIL_SERVER']='smtp.gmail.com'
		app.config['MAIL_PORT'] = 465
		app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
		app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
		app.config['MAIL_USE_TLS'] = False
		app.config['MAIL_USE_SSL'] = True
		mail = Mail(app)
		msg = Message('Hello', sender = os.getenv('EMAIL'), recipients = [tomail])
		msg.body = "<h1>Hello Flask message sent from Flask-Mail</h1>"
		msg.subject = x
		link = "https://adist.herokuapp.com/{}/{}".format(y,token)
		msg.html = "<div><h1>change password</h1><h1><a href='"+link+"'}>click me</a></h1></div>"
		msg.html = '''<div
		style="text-align:center;max-width:600px;background:rgba( 255, 255, 255, 0.25 );box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );backdrop-filter: blur( 4px );border-radius: 10px;border: 1px solid rgba( 255, 255, 255, 0.18 );">
			<h1>Adist</h1>
			<h2>Verification mail</h2>
			<h2>hi {} click the link below to conform your mail</h2>
			<h3><a href='{}' >Click Here</a></h3>
			<p>Copy paste in browser if the above link is not working: {}</p>
		</div>'''.format(username,link,link)
		mail.send(msg)
		return True
	except:
		return False

# =============================================================================================================

@app.route("/")
@app.route("/home")
def home():
	if not db_connection:
		return "<h1>error in connection to db try later<h1>"	
	if "user" in session:
		#  D S M B
		q = "SELECT points FROM users WHERE email = '{}'".format(session["user"][1])
		points = db.select(q)
		points = points[0][0]
		return render_template("index.html",user = session["user"],points = points)
	else:
		return redirect("/signin")

# =============================================================================================================
@app.route("/signin", methods = ['POST', 'GET'])
def signin():
	if request.method == 'GET':
		if "user" in session:return redirect("/")
		else:return render_template("signin.html")
	if request.method == 'POST':
		values = request.form.to_dict()
		email = values["email"]
		q = "SELECT email,username,hashed,conform_mail FROM users WHERE email = '{}'".format(email)
		result = db.select(q)
		if len(result) == 0:
			flash('invalid email')
			return redirect("/signin")
		elif len(result) == 1:
			result = result[0]
			if result[3] == "#":
				if encrypt.validate(values["password"],result[2]):
					session["user"] = (result[1],result[0])
					return redirect("/")
				else:
					flash('incorrect password')
					return redirect("/signin")
			else:
				flash('please confirm your mail')
				return redirect("/signin")
		else:
			flash('internal error')
			return redirect("/signin")

# =============================================================================================================

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
	if request.method == 'GET':
		if "user" in session:return redirect("/")
		else:return render_template("signup.html")
	if request.method == 'POST':
		values = request.form.to_dict()
		username = values["username"]
		email = values["email"]

		result = db.select("SELECT email FROM users WHERE email = '{}'".format(email))

		if len(result) == 0:
			result = db.select("SELECT username FROM users WHERE username = '{}'".format(username))
			if len(result) == 0:
				salt,hashed = encrypt.create(values["password"])
				token = tokens.create([email,username,salt,hashed],os.getenv('EMAIL_CONFIRMATION_TOKEN'))
				if mailing(email,username,token,1):
					q = "INSERT INTO users (username,email,salt,hashed,conform_mail,password_mail,points,created_on) VALUES ('{}','{}','{}','{}','{}','#','0',CURRENT_TIMESTAMP)".format(username,email,salt,hashed,token)
					if db.insert(q):
						flash('please confirm your mail')
						return redirect("/signup")
					else:
						flash('internal error')
						return redirect("/signup")
				else:
					flash('error in sending mail')
					return redirect("/signup")
			elif len(result) == 1:
				flash('username already in use')
				return redirect("/signup")
			else:
				flash('internal error')
				return redirect("/signup")
		elif len(result) == 1:
			flash('email already in use')
			return redirect("/signup")
		else:
			flash('internal error')
			return redirect("/signup")

# =============================================================================================================

@app.route('/confirm_email/<token>')
def confirm_email(token):
	res = tokens.check(token,os.getenv('EMAIL_CONFIRMATION_TOKEN'))
	if res == "invalid":
		return "invalid url"
	if res[-1] == "valid":
		email,username,salt,hashed = res[0],res[1],res[2],res[3]
		q = "SELECT conform_mail,email FROM users WHERE email = '{}'".format(email)
		result = db.select(q)
		if len(result) == 1:
			result = result[0]
			if result[0] == token:
				q = "UPDATE users SET conform_mail = '#',salt = '{}',hashed = '{}' WHERE email = '{}'".format(salt,hashed,email)
				if db.insert(q):
					flash('email verified')
					return redirect("/signin")
				else:
					flash('error in db')
					return redirect("/signin")
			elif result[0] == "#":
				flash('email already verified')
				return redirect("/signin")
			else:
				flash('invalid token')
				return redirect("/signin")
		elif len(result) == 0:
			flash('email not found')
			return redirect("/signin")
		else:
			flash('internal error')
			return redirect("/signin")
	
	if res[-1] == "expired":
		email,username,salt,hashed = res[0],res[1],res[2],res[3]
		q = "SELECT conform_mail,email FROM users WHERE email = '{}'".format(email)
		result = db.select(q)
		if len(result) == 1:
			result = result[0]
			if result[0] == "#":
				flash('already confirmed')
				return redirect("/signin")
			elif result[0] == token:
				flash("token expired")
				return render_template("send_again.html",token = token,confirm = "confirm")
			else:
				flash("invalid token")
				return redirect("/signin")
		elif len(result) == 0:
			flash('invalid token')
			return redirect("/signin")
		else:
			flash('internal error')
			return redirect("/signin")

@app.route('/send_again', methods = ['POST', 'GET'])
def send_again():
	if request.method == 'GET':
		return redirect("/")
	if request.method == 'POST':
		values = request.form.to_dict()
		confirm = values["confirm"]
		token = values["token"]

		if confirm == "confirm":
			res = tokens.get(token,os.getenv('EMAIL_CONFIRMATION_TOKEN'))
			if res == "invalid":
				return "invalid url"
			else:
				email,username = res[0],res[1]
				token = tokens.create(res,os.getenv('EMAIL_CONFIRMATION_TOKEN'))
				if mailing(email,username,token,1):
					q = "UPDATE users SET conform_mail = '{}' WHERE username = '{}'".format(token,username)
					if db.insert(q):
						flash('please confirm your mail')
						return redirect("/signup")
					else:
						flash('error in db')
						return redirect("/signup")
				else:
					flash('error in sending mail')
					return redirect("/signup")
		elif confirm == "password":
			res = tokens.get(token,os.getenv('PASSWORD_CONFIRMATION_TOKEN'))
			if res == "invalid":
				return "invalid url"
			else:
				email,username = res[0],res[1]
				token = tokens.create(res,os.getenv('PASSWORD_CONFIRMATION_TOKEN'))
				if mailing(email,username,token,2):
					q = "UPDATE users SET password_mail = '{}' WHERE username = '{}'".format(token,username)
					if db.insert(q):
						flash('please confirm your mail')
						return redirect("/signin")
					else:
						flash('error in db')
						return redirect("/signin")
				else:
					flash('error in sending mail')
					return redirect("/signin")
		else:
			flash('invalid request')
			return redirect("/signup")


# =============================================================================================================

@app.route('/passwordchange', methods = ['POST', 'GET'])
def password_change():
	if request.method == 'GET':
		return render_template("passwordchange.html")
	if request.method == 'POST':
		values = request.form.to_dict()
		email = values["email"]
		password = values["password"]

		result = db.select("SELECT email,username,hashed,conform_mail FROM users WHERE email = '{}'".format(email))
		if len(result) == 1:
			result = result[0]
			email,username,hashed,conform_mail = result[0],result[1],result[2],result[3]
			if conform_mail == "#":
				if encrypt.validate(password,hashed):
					flash("old and new passwords cannot be same")
					return redirect("/passwordchange")
				else:
					salt,hashed = encrypt.create(password)
					token = tokens.create([email,username,salt,hashed],os.getenv('PASSWORD_CONFIRMATION_TOKEN'))
					if mailing(email,username,token,2):
						q = "UPDATE users SET password_mail = '{}' WHERE username = '{}'".format(token,username)
						if db.insert(q):
							flash('verify mail')
							return redirect("/passwordchange")
						else:
							flash('error in db')
							return redirect("/passwordchange")
					else:
						flash('error in sending mail')
						return redirect("/passwordchange")
			else:
				flash('please confirm your mail to make changes')
				return redirect("/passwordchange")
		elif len(result) == 0:
			flash('email not found')
			return redirect("/passwordchange")
		else:
			flash('internal error')
			return redirect("/passwordchange")

# =============================================================================================================

@app.route('/reset_password/<token>')
def reset_password(token):
	res = tokens.check(token,os.getenv('PASSWORD_CONFIRMATION_TOKEN'))
	if res == "invalid":
		return "invalid url"
	if res[-1] == "valid":
		email,username,salt,hashed = res[0],res[1],res[2],res[3]
		q = "SELECT password_mail,email FROM users WHERE email = '{}'".format(email)
		result = db.select(q)
		if len(result) == 1:
			result = result[0]
			if result[0] == token:
				q = "UPDATE users SET password_mail = '#',salt = '{}',hashed = '{}' WHERE email = '{}'".format(salt,hashed,email)
				if db.insert(q):
					flash('email verified')
					return redirect("/signin")
				else:
					flash('error in db')
					return redirect("/signin")
			elif result[0] == "#":
				flash('link expired or already updated')
				return redirect("/signin")
			else:
				flash('invalid token')
				return redirect("/signin")
		elif len(result) == 0:
			flash('email not found')
			return redirect("/signin")
		else:
			flash('internal error')
			return redirect("/signin")
	if res[-1] == "expired":
		email,username,salt,hashed = res[0],res[1],res[2],res[3]
		q = "SELECT password_mail,email FROM users WHERE email = '{}'".format(email)
		result = db.select(q)
		if len(result) == 1:
			result = result[0]
			if result[0] == "#":
				flash('invalid url')
				return redirect("/signin")
			elif result[0] == token:
				flash("token expired")
				return render_template("send_again.html",token = token,confirm = "password")
			else:
				flash("invalid token")
				return redirect("/signin")
		elif len(result) == 0:
			flash('invalid token')
			return redirect("/signin")
		else:
			flash('internal error')
			return redirect("/signin")


# =============================================================================================================
@app.route("/profile", methods = ['POST', 'GET'])
def profile():
	if request.method == 'GET':
		if 'user' in session:
			q = "SELECT username,email,points FROM users WHERE email = '{}'".format(session['user'][1])
			result = db.select(q)
			if len(result) == 1:
				result = result[0]
				username,email,points = result[0],result[1],result[2]
				return render_template("profile.html",username = username,email = email,points = points)
			elif len(result) == 0:
				flash('invalid login')
				return redirect("/signin")
			else:
				flash('internal error')
				return redirect("/signin")
		else:
			flash('please login first')
			return redirect("/signin")
	if request.method == 'POST':
		if 'user' in session:
			values = request.form.to_dict()
			password = values["password"]
			email = session['user'][1]
			salt,hashed = encrypt.create(password)
			q = "UPDATE users SET salt = '{}',hashed = '{}' WHERE email = '{}'".format(salt,hashed,email)
			if db.insert(q):
				flash('password updated')
				return redirect("/profile")
			else:
				flash('error in db')
				return redirect("/profile")
		else:
			flash('please login first')
			return redirect("/signin")
			

# =============================================================================================================
@app.route("/ad", methods = ['POST', 'GET'])
def ad():
	if request.method == 'GET':
		return redirect("/")
	if request.method == 'POST':
		if 'user' in session:
			values = request.form.to_dict()
			v = values['v']
			if v == "1":
				duration = '30'
			elif v == "2":
				duration = '60'
			elif v == "3":
				duration = '15'
			else:
				flash('invalid type')
				return redirect("/")
			token = tokens.adcreate([duration,session['user'][1]])
			return "https://adist.herokuapp.com/adview/{}".format(token)
		else:
			flash('please login first')
			return redirect("/signin")
# =============================================================================================================
@app.route("/adview/<token>", methods = ['POST', 'GET'])
def adview(token):
	if request.method == 'GET':
		if 'user' in session:
			result = tokens.advalidate(token)
			if result == "invalid" or result == "expired":
				flash('invalid ad')
				return redirect("/")
			else:
				duration,email = result
			q = "SELECT email FROM users WHERE email = '{}'".format(email)
			result = db.select(q)
			if len(result) == 1:
				result = result[0]
				randlis = randad.randomlist()
				return render_template("adview.html",duration = duration,randlis = randlis)
			elif len(result) == 0:
				flash('invalid login')
				return redirect("/")
			else:
				flash('internal error')
				return redirect("/")
	if request.method == 'POST':
		flash('invalid request')
		return redirect("/")

@app.route("/adview", methods = ['POST', 'GET'])
def adviewpoast():
	if request.method == 'GET':
		flash('invalid request')
		return redirect("/")
	if request.method == 'POST':
		if 'user' in session:
			if recaptcha.verify():
				flash('Captcha Verified')
				values = request.form.to_dict()
				duration = values['duration']
				p=0
				if duration == "15":
					p = 0.5
				elif duration == "30":
					p = 1
				elif duration == "60":
					p = 2
				else:
					flash('invalid type')
					return redirect("/")
				q = "SELECT email,points FROM users WHERE email = '{}'".format(session['user'][1])
				result = db.select(q)
				if len(result) == 1:
					result = result[0]
					points = str(float(result[1]) + float(p))
					q = "UPDATE users SET points = '{}' WHERE email = '{}'".format(points,session['user'][1])
					if db.insert(q):
						flash('points added')
						return redirect("/")
					else:
						flash('error in db')
						return redirect("/")
				elif len(result) == 0:
					flash('invalid login')
					return redirect("/")
				else:
					flash('internal error')
					return redirect("/")
			else:
				flash('Captcha Not Verified')
				return redirect('/')
# =============================================================================================================
@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")

@app.route("/future")
def future():
	return "These will be implemented in future"

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


if __name__ == '__main__':
	app.run(debug=True,port=8000)