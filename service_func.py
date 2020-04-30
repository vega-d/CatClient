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
        debugOutput(r"""you're running MacOS, i'm not gonna support this thing.""")