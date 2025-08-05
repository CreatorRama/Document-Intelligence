# gunicorn.conf.py
workers = 1  # Reduce workers (1 is safer for free tier)
timeout = 120  # Increase timeout
keepalive = 5
worker_class = "sync"  # Default (avoid async workers)