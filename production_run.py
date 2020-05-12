from gevent.pywsgi import WSGIServer
import wsgiserver

from main import *

http_server = ''


# def run():
#     # d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
#     # server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 80), d)
#     # server.start()
#     #
#     main.main()
#
#     def stop():
#         main.quit()


def run():
    global http_server
    print('staring production server')
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()


# # - func not work -
# def close():
#     global http_server
#     print('tut')
#     http_server = ''