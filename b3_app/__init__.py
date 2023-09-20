import socket
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mail import Mail

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='amgrcia97@gmail.com',
    MAIL_PASSWORD='eyilylsbrbokphdt',
))

if socket.gethostname() == 'Andrs':
    app.config["DEBUG"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/b3_app"
    engine = create_engine("mysql://root:@localhost/b3_app")

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b3market:password.1234@b3market.mysql.pythonanywhere-services.com/b3market$b3_market'
    engine = create_engine("mysql://b3market:password.1234@b3market.mysql.pythonanywhere-services.com/b3market$b3_market")

app.config['SQLALCHEMY_TRACK_MODFICATIONS'] = False

mail = Mail(app)

db = SQLAlchemy(app)

from b3_app import routes  # noqa: E402
