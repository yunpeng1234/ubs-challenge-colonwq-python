from flask import Flask
from routes.challenge1.lazydev import lazydev
from routes.challenge2.greedymonkey import greedymonkey
from routes.challenge3.digitalcolony import digitalcolony
from routes.airport import airport
from routes.swissbtye import swissbyte
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/", methods=["GET"])
def default_route():
    return "Python Template"


app.register_blueprint(lazydev)
app.register_blueprint(greedymonkey)
app.register_blueprint(digitalcolony)
app.register_blueprint(airport)
app.register_blueprint(swissbyte)

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    logging.info("Starting application ...")
    app.run(port=8080, debug=True)
