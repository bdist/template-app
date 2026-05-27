# see http://docs.gunicorn.org/en/latest/configure.html#configuration-file

from os import getenv

wsgi_app = getenv("WSGI_APP", "wsgi:app")
bind = getenv("WSGI_BIND", f"0.0.0.0:{getenv('PORT', '8080')}")
workers = int(getenv("WSGI_NUM_WORKERS", 1))
worker_tmp_dir = getenv("WSGI_WORKER_TMP_DIR", "/dev/shm")
accesslog = "-"
errorlog = "-"
loglevel = getenv("WSGI_LOG_LEVEL", "info")
worker_class = getenv("GUNICORN_WORKER_CLASS", "gthread")
threads = int(getenv("WSGI_THREADS", 2))
reload = getenv("DEV", "false").strip().lower() in ("1", "true")
# improve fairness
reuse_port = getenv("WSGI_REUSE_PORT", "true").strip().lower() in ("1", "true")
keepalive = int(getenv("WSGI_KEEP_ALIVE", 60))
timeout = int(getenv("WSGI_TIMEOUT", 30))
graceful_timeout = int(getenv("WSGI_GRACEFUL_TIMEOUT", 10))
max_requests = int(getenv("WSGI_MAX_REQUESTS", 1300))
max_requests_jitter = int(getenv("WSGI_MAX_REQUESTS_JITTER", 30))
control_socket_disable = True
