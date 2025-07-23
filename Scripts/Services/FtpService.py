from datetime import datetime
from ftplib import FTP

class FtpService:
    def __init__(self, host_name: str, login: str, password: str):
        self.ftp = FTP(host=host_name, timeout=10)
        self.ftp.login(user=login, passwd=password)
        self.ftp.set_pasv(False)

    def _ensure_dir(self, path: str):
        directories = path.strip('/').split('/')
        current_path = ''
        for directory in directories:
            current_path += f'/{directory}'
            try:
                self.ftp.cwd(current_path)
            except Exception:
                try:
                    self.ftp.mkd(current_path)
                    self.ftp.cwd(current_path)
                except Exception as e:
                    print(f"Failed to create or change into directory {current_path}: {e}")
                    raise

    def try_log_file(self, file_path: str, remote_directory_path: str = None):
        remote_directory_path += f'/{datetime.now().strftime("%Y_%m_%d")}'
        timestamp = datetime.now().strftime("%H%M%S_%f")
        log_file_name = f"{timestamp}_log.txt"
        self._ensure_dir(remote_directory_path)

        return self.ftp.storbinary(f'STOR /{remote_directory_path}/{log_file_name}', open(file_path, 'rb'))