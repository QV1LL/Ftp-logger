import time
import atexit
import signal
import sys
from Scripts.Services.LoggerService import LoggerService

def shutdown_handler(signum=None, frame=None):
    print("\nShutting down...")
    LoggerService.stop()
    sys.exit(0)

if __name__ == '__main__':
    LoggerService.start()

    atexit.register(LoggerService.stop)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        while True:
            time.sleep(1)
    except Exception as ex:
        print(f"Unhandled exception: {ex}")
    finally:
        LoggerService.stop()
