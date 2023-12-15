from werkzeug.security import generate_password_hash, check_password_hash

import global_var as gv


def hash_password(password):
    hashed_password = generate_password_hash(password)
    return hashed_password


def check_password(password, hash):
    return check_password_hash(hash, password)


def quick_share(ret=None):
    if ret == 'extension':
        return quick_share().split('.')[-1]
    return gv.quick_src if gv.quick_src else gv.no_image


def debugOutput(*args, **kwargs):
    if gv.debug:
        from datetime import datetime
        print(datetime.now(), ' - ', *args, **kwargs)


def getIP():
    return 'debian11-2023-12-2.hamlet-chimera.ts.net'

def available_user_addresses(user_name, address_dir=None):
    from data import db_session
    from data.users import User
    if user_name.lower() is "admin":
        return True

    if address_dir:
        '''
        It displays that the user has access to the folder (parameters are taken from the db)
        '''
        session = db_session.create_session()
        user = session.query(User).filter(User.name == user_name).first()
        if user.dirs:
            dirs_user = [i.replace(r'\\', '/').replace('\\', '/') for i in user.dirs.split(',')]
            debugOutput("tried to access:", address_dir, "; has access to:", dirs_user)
            for dir in dirs_user:

                if dir in address_dir:
                    return True
        return False
    else:
        '''
        Displays the entire list of dir that the user has access to
        '''
        session = db_session.create_session()
        user = session.query(User).filter(User.name == user_name).first()
        if user.dirs:
            dirs_user = [i.replace(r'\\', '/').replace('\\', '/') for i in user.dirs.split(',')]

            return dirs_user
        return []


def does_this_directory_already_exist(user_name, address_dir):
    """

    """
    from data import db_session
    from data.users import User

    session = db_session.create_session()
    user = session.query(User).filter(User.name == user_name).first()
    if user.dirs:
        dirs_user = user.dirs.split(',')
        for dir in dirs_user:
            if dir in address_dir:
                return True
    return False


def checking_dir_when_adding(address_dir):
    """
    Stupidly checks if the full address
    """
    from sys import platform
    if platform in ("linux", "linux2"):
        return address_dir.count('/')
    elif platform == "win32":
        address_dir = address_dir.replace('/', '\\')
        return address_dir[1] == ':' and address_dir[0] == address_dir[0].upper() and address_dir[2] == '\\'
    elif platform == "darwin":
        debugOutput(r"""you're running MacOS, i'm not gonna support that shit.""")  # sorry
    return False

def getDefaultHome():
    """

    """
    from sys import platform
    if platform in ("linux", "linux2"):
        return "~;;"
    elif platform == "win32":
        return "C:;;"
    elif platform == "darwin":
        debugOutput(r"""you're running MacOS, i'm not gonna support that shit.""")  # sorry
    assert ValueError
    return None


def generateQR():
    import qrcode

    img = qrcode.make('https://' + getIP())
    img.save("static/img/qr.png")


def convert_path(path, link=False):
    ll = path.replace('/', gv.url_path_separation).replace('\\', gv.url_path_separation)
    if link:
        if link == 'qs':
            return '/qs/' + ll
        else:
            return '/q/' + ll
    return ll


def generate_dir(path, qs=False):
    import os
    prefix = '/qs/' if qs else '/q/'
    try:
        list_dir = os.listdir(path)
    except PermissionError as e:
        return [(prefix + convert_path(os.path.split(path)[0]),
                 'Sorry, you have no permissions. Click here to go back')],[]
    except FileNotFoundError as e:
        return [(prefix + convert_path(os.path.split(path)[0]),
                 'Sorry, this file does not exist. Click here to go back')],[]

    ret, hidden_files = [], []

    split_path = os.path.split(path)

    upperfolderAllowed = True
    try:
        tmp = os.listdir('/'.join(split_path[:-1]))
    except PermissionError as e:
        upperfolderAllowed = False

    if split_path[-1] and upperfolderAllowed:
        ret.append((
            prefix + convert_path('/'.join(split_path[:-1])),
            '...'
        ))

    for i in list_dir:
        if i[0] == '.':
            hidden_files.append((
                prefix + convert_path(os.path.join(path, i)),
                i
            ))
        else:
            ret.append((
                prefix + convert_path(os.path.join(path, i)),
                i
            ))
    return ret, hidden_files


def qsgenerate_dir(path):
    pass

def setqs(src):
    import os
    import sys
    from shutil import copyfile
    cwd = os.getcwd()
    path, filename = os.path.split(src)
    extension = filename.split('.')[-1]
    dst = str(sys.path[0]) + '/static/qs.' + extension
    with open(dst, 'w+'):
        pass
    copyfile(src, dst)
    gv.quick_src = '/static/qs.' + extension


def generate_token():
    import secrets
    return secrets.token_urlsafe(16)


def compToken(login, token):
    true_token = get_token(login)
    return true_token == token


def id_to_login(id):
    from data import db_session
    from data.users import User
    session = db_session.create_session()
    login = session.query(User).filter(User.id == id).first()
    if not login:
        return 'error'
    return login.name


def login_to_id(login):
    from data import db_session
    from data.users import User
    session = db_session.create_session()
    id = session.query(User).filter(User.name == login).first().id
    print('id', type(id))
    return id if id else 'error'


def change_token(login, new_token, old_token=None):
    from data import db_session
    from data.settings import Settings
    session = db_session.create_session()
    if old_token:
        user_set = session.query(Settings).filter(Settings.id == login_to_id(login),
                                                  Settings.token == old_token).first()
        if not user_set:
            return 'error'
        user_set.token = new_token
        session.commit()
        return 'ok'
    else:
        user_set = session.query(Settings).filter(Settings.id == login_to_id(login)).first()
        if not user_set:
            return 'error'
        user_set.token = new_token
        session.commit()
        return 'ok'


def get_token(login):
    from data import db_session
    from data.settings import Settings
    session = db_session.create_session()
    users = session.query(Settings).filter(Settings.id == login_to_id(login))
    print('users', users, type(users))
    user = users.first()
    print(user)
    return user.token if user else 'error'


def token_to_login(token):
    from data import db_session
    from data.settings import Settings

    session = db_session.create_session()

    ids = session.query(Settings).filter(Settings.token == token)
    if ids:
        id = ids[0].id
        return id_to_login(id)
    else:
        return None


def get_user(id_user):
    from data import db_session
    session = db_session.create_session()
    from data.users import User
    user = session.query(User).get(id_user)
    return user


def change_password(user_name=None, pass_old=None, pass_new=None):
    if user_name and pass_new and pass_old:
        try:
            from data import db_session
            session = db_session.create_session()
            from data.users import User

            user = session.query(User).filter(User.name == user_name).first()

            print('pass_old', pass_old)
            print('user.hashed_password', user.hashed_password)

            if user.check_password(pass_old):
                print('changed password for user')
                user.set_password(pass_new)
                session.commit()
                return True
            else:
                return False
        except Exception:
            return False

    else:
        return False


def get_theme(cur_user=None):
    if not cur_user or cur_user.is_authenticated == False:
        return True

    id = cur_user.id
    from data import db_session
    session = db_session.create_session()
    from data.settings import Settings
    sett = session.query(Settings).filter(Settings.id == id).first()
    print(id)
    if sett.theme == "dark":
        return True
    else:
        return False


def change_theme(cur_user=None):
    if not cur_user:
        return False
    from data import db_session
    session = db_session.create_session()
    from data.settings import Settings
    sett = session.query(Settings).filter(Settings.id == cur_user.id).first()
    if sett:
        if sett.theme == 'dark':
            sett.theme = 'light'
        else:
            sett.theme = 'dark'
        session.commit()
        return True
    return False
