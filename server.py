from flask import Flask, render_template, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired,BadTimeSignature

app = Flask(__name__)

s = URLSafeTimedSerializer('Thisisasecret!')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
    if request.method == 'POST':
        # email = request.form['email']
        email = [1,2,3]
        token = s.dumps(email, salt='email-confirm')
        return '<h3>The email you entered is {}. The token is {}</h3>'.format(email, token)

@app.route('/send_again/<token>', methods = ['POST', 'GET'])
def send_again(token):
    if request.method == 'GET':
        try:
            print("=======================================================================")
            email = s.loads(token, salt='email-confirm', max_age=3600)
            print(email)
            print(type(email))
            print("valid")
        except SignatureExpired:
            emails = s.loads(token, salt='email-confirm')
            print(emails)
            print("expired")
            # print(type(email))
            return '<h1>The token is expired!</h1>'
        except BadTimeSignature:
            print("invalid")
            return '<h1>The token is invalid!</h1>'
        return render_template("send_again.html",token = token)
        return '<h1>The token works! {}</h1>'.format(email)
    if request.method == 'POST':
        return "posted"

@app.route('/send_again', methods = ['POST', 'GET'])
def sends_again():
    if request.method == 'POST':
        return "posted"

if __name__ == '__main__':
    app.run(debug=True)