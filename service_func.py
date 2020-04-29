from werkzeug.security import generate_password_hash, check_password_hash


def set_password(password):
    hashed_password = generate_password_hash(password)
    return hashed_password


def check_password(password, hash):
    return check_password_hash(hash, password)


print(set_password('123'))