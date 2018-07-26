command = '/home/forge/.local/bin/gunicorn -w4 server:app'
bind = '127.0.0.1:9000'
workers = 3
user = 'forge'