import datetime
import os

from flask import Flask, render_template, redirect, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import global_var as gv
import service_func as sf
from data import db_session
from data.classes import LoginForm, RegisterForm
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/catclient.sqlite")
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    app.run(port=8080, host='0.0.0.0')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if not current_user.is_authenticated:
        return redirect('no_access/only registered users can create accounts')
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="Password mismatch")
        session = db_session.create_session()
        if session.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="This user already exists.")
        if not current_user.is_authenticated:
            return redirect('no_access/only registered users can create accounts')
        user = User(
            name=form.name.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)


@app.route('/no_access/')
@app.route('/no_access/<reason>')
def no_access(reason="None specified"):
    return render_template('no_access.html', reason=reason)


@app.route("/")
def index():
    args = {'quick_src': sf.quick_image(), 'ip': sf.getIP()}

    return render_template("index.html", **args)


if __name__ == '__main__':
    main()
