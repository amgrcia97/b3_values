
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# file_path = os.path.abspath(os.getcwd())+"/todo.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/b3_app"
app.config['SQLALCHEMY_TRACK_MODFICATIONS'] = False

db = SQLAlchemy(app)

from b3_app import routes  # noqa: E402
