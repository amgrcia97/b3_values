# from flask import render_template, request  # , redirect, url_for
from b3_app import app
# from b3_app.models import User, UserAsset, AssetType
# from b3_app import db


# @app.route('/')
# def index():
#     users = User.query.all()
#     a_types = AssetType.query.all()
#     assets = UserAsset.query.all()
#     # complete = Todo.query.filter_by(complete=True).all()
#     print(users, a_types, assets)
#     print(dir(request))
#     return render_template('index.html')


# @app.route('/add', methods=['POST'])
# def add():
#     # todo = Todo(text=request.form['todoitem'], complete=False)
#     # db.session.add(todo)
#     # db.session.commit()

#     return redirect(url_for('index'))


# @app.route('/complete/<id>')
# def complete(id):

#     # todo = Todo.query.filter_by(id=int(id)).first()
#     # todo.complete = True
#     # db.session.commit()

#     return redirect(url_for('index'))

from flask import render_template, redirect, request, session
# The Session instance is not used for direct access, you should always use flask.session
from flask_session import Session

# app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    print('OPAAA')
    if not session.get("name"):
        return redirect("/login")
    return render_template('index.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    print('LOGIN-->>', request.method)
    print('INFO-->>', request.form)
    # if request.method == "POST":
    #     session["name"] = request.form.get("name")
    #     return redirect("/")
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    print('signup-->>', request.method)
    print('INFO-->>', request.form)
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        print('INFO-->>', username, email, password, confirm_password)
    #     session["name"] = request.form.get("name")
    #     return redirect("/")
    return render_template("signup.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")
