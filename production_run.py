from gevent.pywsgi import WSGIServer

from main import *


def run():
    print('staring production server')
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()
