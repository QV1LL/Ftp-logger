import os
import threading
import time
from datetime import datetime
from Scripts.Services.FtpService import FtpService
from Scripts.Services.SettingsLoader import SettingsLoader

class LoggerService:
    _stop_event = threading.Event()
    _thread = None
    _logs_folder = "logs"
    _period = 60
    _ftp_config = {}

    @classmethod
    def start(self):
        SettingsLoader.load()

        self._logs_folder = SettingsLoader.get("logger.logs_folder", "logs")
        self._files_to_log_folder = SettingsLoader.get("logger.files_to_log_folder", "files")
        self._period = SettingsLoader.get("logger.period", 60)
        self._ftp_config = {
            "host": SettingsLoader.get("ftp.host"),
            "username": SettingsLoader.get("ftp.username"),
            "password": SettingsLoader.get("ftp.password")
        }

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print(f"Logger started. Scanning '{self._logs_folder}' every {self._period} seconds.")

    @classmethod
    def _run(self):
        while not self._stop_event.is_set():
            self._check_and_send_logs()
            time.sleep(self._period)

    @classmethod
    def _check_and_send_logs(self):
        try:
            full_logs_path = os.path.join(os.getcwd(), self._files_to_log_folder)
            if not os.path.isdir(full_logs_path):
                print(f"Logs folder not found: {self._files_to_log_folder}")
                return

            files = os.listdir(full_logs_path)
            if not files:
                print("No files found to log")
                return

            for filename in files:
                full_file_path = os.path.join(full_logs_path, filename)

                if not os.path.isfile(full_file_path):
                    continue

                remote_directory_path = f"/{self._logs_folder}"

                print(f"Sending file {full_file_path} to FTP as {remote_directory_path}")

                ftp = FtpService(
                    self._ftp_config["host"],
                    self._ftp_config["username"],
                    self._ftp_config["password"]
                )
                success = ftp.try_log_file(full_file_path, remote_directory_path)

                if success:
                    os.remove(full_file_path)

                print(f'Result of logging {filename}: {success}')
        except Exception as e:
            print(f"Error sending logs: {e}")

    @classmethod
    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
            print("Logger stopped.")
