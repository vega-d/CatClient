import os

from flask import Flask, send_from_directory, render_template


def quick_share(app, path, address=None):
    """
    quickly host given file at given address
    :type app: Flask
    :type address: str
    :type path: str
    :param app: Flask kind object
    :param address: address to host at (yourdomain.com/address)
    :param path: path where to get file from
    :return:
    """
    try:
        splitted_path = os.path.split(path)
    except Exception as e:
        raise ValueError
    try:
        @app.route(address)
        def quick_host():
            try:
                return send_from_directory(*splitted_path)
            except Exception as e:
                print(e)
                return render_template('error.html', stack=e)
    except Exception as e:
        raise ValueError
