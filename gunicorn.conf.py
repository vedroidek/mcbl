wsgi_app = "microblog:create_app('dev')"
bind = "127.0.0.1:5000"
workers = 2
reload = True

workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
backlog = 512
timeout = 15  # Workers silent for more than this many seconds are killed and restarted.

loglevel = "info"
errorlog = "./logs/gunicorn_error.log"
accesslog = "./logs/gunicorn_access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

limit_request_field_size = 4096
limit_request_fields = 80
limit_request_line = 2048
