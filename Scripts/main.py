import time
from Scripts.Services.LoggerService import LoggerService

if __name__ == '__main__':
    LoggerService.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        LoggerService.stop()