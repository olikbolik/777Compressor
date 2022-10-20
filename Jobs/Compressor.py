import os
import gzip
import shutil
from datetime import date

from Common.Constants import LOGS_PATH, HELPER_INFO_FILE


class FileCompressor:
    script_running_frequency = 30

    def __init__(self):
        self.helper_info_path = os.path.join(LOGS_PATH, HELPER_INFO_FILE)
        self.today_date_str = date.today().strftime("%Y%m%d_")

    def compress(self) -> None:
        if self.compression_should_be_started():
            for file, full_path in self.files_to_compress():
                with open(full_path, 'rb') as orig_file:
                    with gzip.open(os.path.join(LOGS_PATH, self.today_date_str + file) + '.gz', 'wb') as gz_file:
                        shutil.copyfileobj(orig_file, gz_file)
                os.remove(full_path)
        else:
            print('Nothing compressed today')

    def files_to_compress(self) -> list:
        return [(file, os.path.join(LOGS_PATH, file)) for file in os.listdir(LOGS_PATH) if file.endswith('.log')]

    def compression_should_be_started(self) -> bool:
        try:
            with open(self.helper_info_path, 'r') as file:
                file.seek(0)
                days_since_last_compression = int(file.read())
            days_since_last_compression += 1
        except IOError:
            days_since_last_compression = -1
        finally:
            if 0 <= days_since_last_compression < self.script_running_frequency:
                with open(self.helper_info_path, 'w+') as file:
                    file.write(str(days_since_last_compression))
                print('Logs were compressed less than 30 day ago')
                return False
            with open(self.helper_info_path, 'w+') as file:
                file.write('0')
            return True
