from b3_app import app, engine
from flask import render_template, redirect, flash, url_for, request, session
from b3_app.models import User  # , UserAsset, AssetType
# The Session instance is not used for direct access, you should always use flask.session
from flask_session import Session
from passlib.hash import sha256_crypt
from sqlalchemy import text, insert

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if not session.get("email"):
        return redirect("/login")
    return render_template('index.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if request.method == "POST":
        with engine.connect() as connection:
            result = connection.execute(text("SELECT password FROM users WHERE email='{email}'".format(email=email)))
            if result.returns_rows:
                passwor_data = result.fetchone()[0]
                if sha256_crypt.verify(password, passwor_data):
                    session["email"] = email
                    flash("You are now logged in!!", "success")
                    return redirect(url_for('index'))  # to be edited from here do redict to either svm or home
                else:
                    flash('Usuário ou senha incorreta', 'danger')
                    return render_template('login.html')
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        confirm_password = request.form.get('confirm_password', None)
        secure_password = sha256_crypt.encrypt(str(password))
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM users WHERE email='{email}'".format(email=email)))
            if result.rowcount == 0 and password == confirm_password:
                stmt = insert(User).values(username=username, email=email, password=secure_password, status='1')
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()
                flash(f'Bem vindo {username}!, você já está cadastrado e agora pode entrar na plataforma', 'success')
                return redirect(url_for('login'))
            else:
                flash(f'Usuário com e-mail "{email}" já existe', 'error')
                return redirect(url_for('signup'))
    else:
        return render_template("signup.html")


@app.route("/recuperar-senha", methods=["POST", "GET"])
def recuperar_senha():
    # TODO: Implemetar método
    flash('Foi enviado um email com as instruções para recuperar a senha', 'success')
    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session["email"] = None
    return redirect(url_for('login'))


# from b3_app.models import User, UserAsset, AssetType
# from b3_app import db


# @app.route('/')
# def index():
#     users = User.query.all()
#     a_types = AssetType.query.all()
#     assets = UserAsset.query.all()
#     # complete = Todo.query.filter_by(complete=True).all()
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
