from werkzeug.security import generate_password_hash, check_password_hash

import global_var as gv


def generate_password(password):
    hashed_password = generate_password_hash(password)
    return hashed_password


def check_password(password, hash):
    return check_password_hash(hash, password)


def quick_share(quick_sync=None, ret=None):
    if ret == 'extension':
        return quick_share().split('.')[-1]
    if quick_sync:
        gv.quick_sync = quick_sync
    return gv.quick_src if gv.quick_src else gv.no_image


def debugOutput(text):
    if gv.debug:
        from datetime import datetime
        print(datetime.now(), ' - ', text)


def getIP():
    """
    nothing special just returns IPv4 of this pc (mac is not a pc!)
    (c) Lunar
    """
    import socket
    from sys import platform
    if platform in ("linux", "linux2", "win32"):
        if socket.gethostbyname(socket.gethostname()).split('.')[0] != '172':
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        else:
            return '0.0.0.0'

    elif platform == "darwin":
        debugOutput(r"""you're running MacOS, i'm not gonna support that shit.""")  # sorry


def available_user_addresses(user_name, address_dir=''):
    from data import db_session
    from data.users import User

    if address_dir:
        '''
        It displays that the user has access to the folder (parameters are taken from the db)
        '''
        session = db_session.create_session()
        user = session.query(User).filter(User.name == user_name).first()
        if user.dirs:
            dirs_user = user.dirs.split(',')
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
            dirs_user = user.dirs.split(',')
            return dirs_user
        return []


def does_this_directory_already_exist(user_name, address_dir):
    """
        Does this directory already exist? (Yes, it is the same as the previous function)
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


def generateQR():
    import qrcode

    img = qrcode.make('http://' + getIP() + ':' + str(gv.port))
    img.save("static/img/qr.png")


def convert_path(path):
    return path.replace('/', gv.url_path_separation).replace('\\', gv.url_path_separation)


def generate_dir(path):
    import os
    try:
        list_dir = os.listdir(path)
    except PermissionError as e:
        return [('/q/' + convert_path(os.path.split(path)[0]),
                 'Sorry, you have no permissions. Click here to go back')]
    ret = []

    split_path = os.path.split(path)
    if split_path[-1]:
        ret.append((
            '/q/' + convert_path('/'.join(split_path[:-1])),
            '...'
        ))

    for i in list_dir:
        template = (
            '/q/' + convert_path(os.path.join(path, i)),
            i
        )
        ret.append(template)
    return ret
