# Server Socket
import multiprocessing

bind = "0.0.0.0:8000"
module = "wsgi:application"

backlog = 2048
workers = multiprocessing.cpu_count() * 2 + 1
threads = 10

keepalive = 2  # Keep connections alive for 2s

# Worker Restart Settings
max_requests = 1000  # Restart workers after processing 1000 requests
max_requests_jitter = 50  # Add randomness to avoid mass restarts

# Logging Settings
accesslog = "-"  # Log to stdout
errorlog = "-"  # Log errors to stdout
loglevel = "info"  # Set log verbosity (debug, info, warning, error, critical)
