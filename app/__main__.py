from gevent.pywsgi import WSGIServer

from app.core import create_app

WSGIServer(
    listener=("", 8000),
    application=create_app(),
).serve_forever()
