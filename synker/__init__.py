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
            raise EXXX('cloud is not set')
        return self._cloud_directory

    @cloud_directory.setter
    def cloud_directory(self, cs):
        error = ''
        cloud_path = cs.get('cloud_path')
        cloud_limit = cs.get('cloud_limit')
        mtime_file = cs.get('mtime_file')
        token = cs.get('token')
        # validation
        if not cloud_path:
            error = 'invalid cloud path'
        elif not cloud_limit or not isinstance(cloud_limit, int):
            error = 'invalid cloud limit'
        elif not mtime_file:
            error = 'invalid mtime file'
        elif not token:
            error = 'invalid token'
        if error:
            raise EXXX(error)
        dp = DropboxProvider()
        dp.set_token(token)
        cd = CloudDirectory(dp, cloud_path, cloud_limit, mtime_file)
        self._cloud_directory = cd

    @property
    def local_directory(self):
        if self._local_directory is None:
            raise EXXX('local directory is not set')
        return self._local_directory

    @local_directory.setter
    def local_directory(self, ls):
        error = ''
        directory_path = ls.get('directory_path')
        pattern = ls.get('pattern')
        # validation
        if not pattern:
            error = 'invalid pattern'
        elif not os.access(directory_path, 7):
            error = 'access denied for directory: {}'.format(directory_path)
        if error:
            raise EXXX(error)
        ld = LocalDirectory(directory_path, pattern)
        self._local_directory = ld

    def run(self):
        current_mtime = self.cloud_directory.mtime
        new_files = self.local_directory.get_files(current_mtime)
        self.cloud_directory.upload(new_files)
