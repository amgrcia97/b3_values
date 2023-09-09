
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# file_path = os.path.abspath(os.getcwd())+"/todo.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/b3_app"
app.config['SQLALCHEMY_TRACK_MODFICATIONS'] = False

engine = create_engine("mysql://root:@localhost/b3_app")

db = SQLAlchemy(app)

from b3_app import routes  # noqa: E402
