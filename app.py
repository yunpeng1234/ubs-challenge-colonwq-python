from flask import Flask
from routes.challenge1.lazydev import lazydev

# app = Flask(__name__)


# @app.route("/")
# def hello_world():
#     return "Hello, World!"


# import socket
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/", methods=["GET"])
def default_route():
    return "Python Template"


app.register_blueprint(lazydev)

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# if __name__ == "__main__":
#     logging.info("Starting application ...")
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.bind(("localhost", 8080))
#     port = sock.getsockname()[1]
#     sock.close()
#     app.run(port=port)