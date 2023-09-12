
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mail import Mail

# file_path = os.path.abspath(os.getcwd())+"/todo.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/b3_app"
app.config['SQLALCHEMY_TRACK_MODFICATIONS'] = False

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='amgrcia97@gmail.com',
    MAIL_PASSWORD='eyilylsbrbokphdt',
))

mail = Mail(app)


engine = create_engine("mysql://root:@localhost/b3_app")

db = SQLAlchemy(app)

from b3_app import routes  # noqa: E402
