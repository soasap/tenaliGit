# importing libraries
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'qa.veni@gmail.com'
app.config['MAIL_PASSWORD'] = 'vhjbbk'

mail = Mail(app)
