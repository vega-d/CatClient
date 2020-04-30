from werkzeug.security import generate_password_hash, check_password_hash
import global_var as gv


def generate_password(password):
    hashed_password = generate_password_hash(password)
    return hashed_password


def check_password(password, hash):
    return check_password_hash(hash, password)


def quick_image():
    return gv.quick_src if gv.quick_src else gv.no_image
