# standard
import os
# internal
from synker.exceptions import EXXX
from synker.providers import DropboxProvider
from synker.directories import CloudDirectory, LocalDirectory
# external


class Synker(object):
    def __init__(self):
        self._cloud_directory = None
        self._local_directory = None

    @property
    def cloud_directory(self):
        if self._cloud_directory is None:
            raise EXXX('ابر تنظیم نشده است')
        return self._cloud_directory

    def set_cloud(self, cloud_path, cloud_limit, mtime_file, token):
        error = ''
        # validation
        if not cloud_path:
            error = 'مسیر ابر اشتباه است'
        elif not cloud_limit or not isinstance(cloud_limit, int):
            error = 'محدودیت حجم باید مقداری عددی و صحیح باشد'
        elif not mtime_file:
            error = 'فایل مهر زمانی معتبر نیست'
        elif not token:
            error = 'توکن معتبر نیست'
        if error:
            raise EXXX(error)
        dp = DropboxProvider()
        dp.set_token(token)
        cd = CloudDirectory(dp, cloud_path, cloud_limit, mtime_file)
        self._cloud_directory = cd

    @property
    def local_directory(self):
        if self._local_directory is None:
            raise EXXX('مسیر بکاپ تنظیم نشده است')
        return self._local_directory

    def set_local(self, directory_path, pattern):
        error = ''
        # validation
        if not pattern:
            error = 'الگوی بکاپ اشتباه است'
        elif not os.access(directory_path, 7):
            error = 'مسیر بکاپ اشتباه است یا دسترسی به آن امکان پذیر نیست: {}'.format(directory_path)
        if error:
            raise EXXX(error)
        ld = LocalDirectory(directory_path, pattern)
        self._local_directory = ld

    def run(self):
        current_mtime = self.cloud_directory.mtime
        new_files = self.local_directory.get_files(current_mtime)
        self.cloud_directory.upload(new_files)
