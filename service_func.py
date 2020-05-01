from werkzeug.security import generate_password_hash, check_password_hash
import global_var as gv



def generate_password(password):
    hashed_password = generate_password_hash(password)
    return hashed_password


def check_password(password, hash):
    return check_password_hash(hash, password)


def quick_image():
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
        debugOutput(r"""you're running MacOS, i'm not gonna support this shit.""")   # sorry


def available_user_addresses(user_name, address_dir=''):
    from data import db_session
    from data.users import User

    if address_dir:
        '''
        It displays that the user has access to the folder (parameters are taken from the db)
        © Veseha
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
         © Veseha
        '''
        session = db_session.create_session()
        user = session.query(User).filter(User.name == user_name).first()
        if user.dirs:
            dirs_user = user.dirs.split(',')
            return dirs_user
        return []


def does_this_directory_already_exist(user_name, address_dir):
    '''
        Does this directory already exist? (Yes, it is the same as the previous function)
        © Veseha
    '''
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
    '''
    Stupidly checks if the full address (on Windows)
    © Veseha
    '''
    if address_dir[1] == ':' and address_dir[0] == address_dir[0].upper() and address_dir[2] == '\\':
        return True
    return False
