import datetime
import os
import getpass

from flask import Flask, render_template, redirect, send_from_directory, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

import global_var as gv
import service_func as sf
from api_resources import Userget, Userlist, Auth, Tokens, Q, ChangePassAPI
from data import db_session
from data.classes import LoginForm, RegisterForm, AddDirsForm, ChangePassForm
from data.settings import Settings
from data.users import User

app = Flask(__name__)
# run_with_ngrok(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/catclient.sqlite")
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
#
login_manager = LoginManager()
login_manager.init_app(app)
sf.generateQR()
ip = sf.getIP()


def main():
    # db_session.global_init("db/blogs.sqlite")
    # app.register_blueprint(api_files.blueprint)

    app.run(
        port=gv.port,
        # host=gv.host
    )


def shutdown_server():
    print('shut down server ---------------')
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# ----------------------------- api ------------------------------


api = Api(app)
api.add_resource(Userlist, '/api/<token>/users')
api.add_resource(Userget, '/api/<token>/user/<user>')
api.add_resource(Auth, '/api/auth/<login>/<hash>')
api.add_resource(Tokens, '/api/token/<login>/<hash>')
api.add_resource(Q, '/api/<token>/q/<src>')
api.add_resource(ChangePassAPI, '/api/changepass/<user>/<old_pass>/<new_pass>')


# ----------------------------- other global var ------------------------------

dark = sf.get_theme(current_user)

# ----------------------------- service url ------------------------------


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# ------------------------------ admin url ------------------------------


def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return "Quitting..."


@app.route('/add_dirs', methods=['GET', 'POST'])
def add_dirs():
    if not current_user.is_authenticated or current_user.name != 'admin':
        return redirect('no_access/only admin account can give permissions')
    form = AddDirsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.name == form.name.data).first()
        if user:
            if not sf.checking_dir_when_adding(form.dir.data):
                return render_template('add_dirs.html',
                                       message="Название путя не корректно", title='Add Folder',
                                       form=form, ip=ip, dark=dark)
            if sf.does_this_directory_already_exist(form.name.data, form.dir.data):
                return render_template('add_dirs.html',
                                       message="Данная папка уже есть в доступе у пользователя", title='Add Folder',
                                       form=form, ip=ip, dark=dark)
            all_user_dirs = sf.available_user_addresses(form.name.data)
            appeandable = form.dir.data.replace(r'\\', '/').replace('\\', '/')
            all_user_dirs.append(appeandable)
            user.dirs = ','.join(all_user_dirs)
            session.commit()
            return redirect("/")
        return render_template('add_dirs.html',
                               message="Пользователя не существует", title='Add Folder',
                               form=form, ip=ip, dark=dark)
    return render_template('add_dirs.html', title='Add Folder', form=form, ip=ip, dark=dark)

# ------------------------------ login url -------------------------------


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
    global dark
    if current_user.is_authenticated:
        return redirect('no_access/Ты уже вошел в аккаунт, выйди и тогда заходи)')

    form = LoginForm()

    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            dark = sf.get_theme(current_user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, ip=ip, dark=dark)
    return render_template('login.html', title='Login', form=form, ip=ip, dark=dark)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if not current_user.is_authenticated or current_user.name != 'admin':
        return redirect('no_access/Только администраторы могу создать аккаунт, пожалуйста обратитесь к администратору')
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="Password mismatch", ip=ip, dark=dark)
        session = db_session.create_session()
        if session.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="This user already exists.", ip=ip, dark=dark)
        if not current_user.is_authenticated:
            return redirect('no_access/only registered users can create accounts')
        user = User(name=form.name.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        user_name = session.query(User).filter(User.name == form.name.data).first()
        settings = Settings(id=user_name.id)
        session.add(settings)
        session.commit()

        return redirect('/')
    return render_template('register.html', title='Register', form=form, ip=ip, dark=dark)


# ------------------------------ account manipulation ------------------------------


@app.route('/change_password', methods=['GET', 'POST'])
def change_pass():
    form = ChangePassForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if not session.query(User).filter(User.name == form.name.data).first():
            return render_template('change_pass.html', title='Register',
                                   form=form,
                                   message="This user does not exists.", ip=ip, dark=dark)
        hashed_old, hashed_new = [sf.hash_password(str(i)) for i in [str(form.password.data), str(form.password_new.data)]]
        res = sf.change_password(form.name.data, form.password.data, form.password_new.data)
        # print(res)
        if res:
            return redirect('/')
        else:
            return render_template('change_pass.html', title='Register',
                                   form=form,
                                   message="wrong credentials", ip=ip, dark=dark)

    return render_template('change_pass.html', title='changing password', form=form, ip=ip, dark=dark)


@app.route('/theme')
def change_theme():
    global dark
    sf.change_theme(current_user)
    dark = sf.get_theme(current_user)
    return redirect('/')


# ------------------------------ error url ------------------------------

@app.route('/no_access/')
@app.route('/no_access/<reason>')
def no_access(reason="None specified"):
    return render_template('no_access.html', reason=reason, ip=ip, dark=dark, title='No access')


# ------------------------------ quick url -----------------------------

@app.route('/q/')
@app.route('/q/<src>')
def quick(src=None):
    print(src)
    if src:  # если у нас надо получить какой-то конкретный файл или папку

        src = src.replace(gv.url_path_separation, '/')  # конвертируем C:;;dir;;dir2 в нормальный формат с /
        from sys import platform
        if platform in ("linux", "linux2"):
            src = src.replace('~', '/home/' + getpass.getuser())
        src = src.replace(';;', '/')
        sf.debugOutput("src requested is", src)
        src_split = os.path.split(src)
        # отделяем путь от конечный пункта, то есть имя папки или файла который надо открыть
        if current_user.is_authenticated:

            if not sf.available_user_addresses(current_user.name, address_dir=src):

                return redirect('/no_access/You have no access to this folder or file.')

            if src_split[-1] and os.path.isfile(src):  # если мы открываем файл дать его в чистом виде
                # print(*src_split, '---')
                return send_from_directory(*src_split)
            else:  # если зашло сюда значит мы открываем папку
                list_visible, list_invisible = sf.generate_dir(src)
                args = {
                    'path': src,  # путь папки
                    'list_visible': list_visible,  # ее содержимое в виде листа из кортежей.
                    'list_invisible': list_invisible,  # ее содержимое в виде листа из кортежей.
                    # пример кортежа ('/q/C:;;Users;;', 'Users')
                    'isq': True,
                    'fdrc': '/qs/' + sf.convert_path(src)
                }
                return render_template('folder.html', **args, ip=ip, dark=dark, title='Explorer', home_folder=gv.home_folder)  # рендерим папку
        else:  # если нету входа в аккаунт но мы лезем в файлы то выбрасываем на no_access
            return redirect('/no_access/only users with certain access can reach this file')
    else:  # если просто /q без аргумента
        return send_from_directory(*os.path.split(sf.quick_share()))


@app.route('/qs/<src>')
@app.route('/qs/')
def quickset(src=None):
    if src:  # если у нас надо получить какой-то конкретный файл или папку
        src = src.replace(gv.url_path_separation, '/')  # конвертируем C:;;dir;;dir2 в нормальный формат с /
        src_split = os.path.split(src)
        # отделяем путь от конечный пункта, то есть имя папки или файла который надо открыть

        if current_user.name == 'admin':
            if src_split[-1] and os.path.isfile(src):  # если мы открываем файл дать его в чистом виде
                sf.setqs(src)
                return redirect('/q/' + sf.convert_path(src_split[0]))
            else:  # если зашло сюда значит мы открываем папку
                list_visible, list_invisible = sf.generate_dir(src, qs=True)
                args = {
                    'path': src,  # путь папки
                    'list_visible': list_visible,  # ее содержимое в виде листа из кортежей.
                    'list_invisible': list_invisible,  # ее содержимое в виде листа из кортежей.
                    'isq': True,
                    'fdrc': '/q/' + sf.convert_path(src)
                }
                return render_template('qsfolder.html', **args, ip=ip, dark=dark, title='Set Q file')  # рендерим папку
        else:  # если нету входа в аккаунт но мы лезем в файлы то выбрасываем на no_access
            return redirect('/no_access/only admin has permission to perform this action')
    else:  # если просто /q без аргумента
        return redirect('/no_access/only admin has permission to perform this action')


# ------------------------------ main url ------------------------------


@app.route("/")
def index():
    global dark
    dark = sf.get_theme(current_user)
    args = {
        'quick_src': sf.quick_share(),
        'ip': sf.getIP(),
        'id_index': True,
        'avdirs': []
    }
    if current_user.is_authenticated:
        args['avdirs'] = [(sf.convert_path(i, link=True), i) for i in sf.available_user_addresses(current_user.name)]
    print(args['avdirs'])
    for key in gv.formats.keys():
        if sf.quick_share(ret='extension') in gv.formats[key]:
            args['quick_type'] = key
            print(key, '-', sf.quick_share())

    return render_template("index.html", **args, dark=dark, title='CatClient', home_folder=gv.home_folder)


if __name__ == '__main__':
    main()
