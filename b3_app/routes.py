from b3_app import app, engine
from functools import wraps
from flask import render_template, redirect, flash, url_for, request, session
from b3_app.models import User  # , UserAsset, AssetType
# The Session instance is not used for direct access, you should always use flask.session
from flask_session import Session
from passlib.hash import sha256_crypt
from sqlalchemy import text, insert
import yfinance as yf
from datetime import datetime

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@login_required
def index():
    actions = ['CMIN3.SA', 'KLBN4.SA', 'MXRF11.SA', 'XPCA11.SA']

    actions = [
        {'name': 'CMIN3.SA', 'qty_u': 10, 'qty_m': 41.40},
        {'name': 'KLBN4.SA', 'qty_u': 1, 'qty_m': 4.49},
        {'name': 'MXRF11.SA', 'qty_u': 15, 'qty_m': 162.75},
        {'name': 'XPCA11.SA', 'qty_u': 20, 'qty_m': 188.60},

    ]
    ptrm = 0
    qty_t = 0
    invested_t = 0
    actives_list = []
    tickers = yf.Tickers(' '.join(action['name'] for action in actions))
    for action in actions:
        last_update = tickers.tickers[action['name']].history(period="1d", interval="1m", rounding=True)['Close']
        last_update_price = last_update.iloc[-1]
        last_update_time = last_update.index[-1].strftime('%H:%M %d/%m/%Y')
        act = tickers.tickers[action['name']].info
        actives_list.append({
            'name': act['underlyingSymbol'].replace('.SA', ''),
            'qty': action['qty_u'],
            'invested': action['qty_m'],
            'average_price': 'R$ {}'.format(round(action['qty_m'] / action['qty_u'], 2)),
            'actual_price': 'R$ {}'.format(last_update_price),
            'last_update': last_update_time,
        })
        ptrm += action['qty_u'] * last_update_price
        qty_t += action['qty_u']
        invested_t += action['qty_m']

    actives_list.append({
        'name': 'TOTAL',
        'qty': qty_t,
        'invested': invested_t,
        'average_price': '',
        'actual_price': '',
        'last_update': datetime.now().strftime('%H:%M %d/%m/%Y'),
    })
    ptrm = round(ptrm, 2)
    invested_t = round(invested_t, 2)
    rend_p = round(ptrm - invested_t, 2) if ptrm >= invested_t else None
    rend_n = round(ptrm - invested_t, 2)*(-1) if invested_t > ptrm else None
    return render_template('index.html', user=session["username"], actives=actives_list, ptrm=ptrm, invested_t=invested_t, rend_p=rend_p, rend_n=rend_n)


@app.route("/about")
@login_required
def about():
    return render_template('about.html')


@app.route("/contact")
@login_required
def contact():
    return render_template('contact.html')


@app.route("/my-profile")
@login_required
def my_profile():
    return render_template('my_profile.html')


@app.route("/settings")
@login_required
def settings():
    return render_template('settings.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if request.method == "POST":
        with engine.connect() as connection:
            result = connection.execute(text("SELECT password, username FROM users WHERE email='{email}'".format(email=email)))
            result_data = result.fetchone()
            if result.returns_rows and result.rowcount > 0:
                passwor_data = result_data[0]
                if sha256_crypt.verify(password, passwor_data):
                    session["email"] = email
                    session["username"] = result_data[1]
                    flash("You are now logged in!!", "success")
                    return redirect(url_for('index'))  # to be edited from here do redict to either svm or home
            flash('Usuário ou senha incorreta', 'danger')
            return render_template('login.html')
    else:
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
    session['_flashes'].clear()
    return redirect('login')
