from logging.config import dictConfig
from time import perf_counter

from flask import Flask
from flask import g
from flask import jsonify

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            },
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            },
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    },
)

app = Flask(__name__)
app.config.from_prefixed_env()
log = app.logger


@app.before_request
def start_request_timer():
    g.request_start_time = perf_counter()


@app.after_request
def add_server_timing(response):
    duration_ms = (perf_counter() - g.request_start_time) * 1000
    timing = f"app;dur={duration_ms:.2f}"
    existing_timing = response.headers.get("Server-Timing")
    response.headers["Server-Timing"] = f"{existing_timing}, {timing}" if existing_timing else timing
    return response


@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!"}), 200


if __name__ == "__main__":
    app.run()
