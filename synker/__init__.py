# standard
# internal
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
            raise Exception('cloud directory is not set')
        return self._cloud_directory

    @cloud_directory.setter
    def cloud_directory(self, cs):
        cloud_path = cs.get('cloud_path')
        cloud_limit = cs.get('cloud_limit')
        mtime_file = cs.get('mtime_file')
        token = cs.get('token')
        dp = DropboxProvider()
        dp.set_token(token)
        cd = CloudDirectory(dp, cloud_path, cloud_limit, mtime_file)
        self._cloud_directory = cd

    @property
    def local_directory(self):
        if self._local_directory is None:
            raise Exception('local directory is not set')
        return self._local_directory

    @local_directory.setter
    def local_directory(self, ls):
        directory_path = ls.get('directory_path')
        pattern = ls.get('pattern')
        ld = LocalDirectory(directory_path, pattern)
        self._local_directory = ld

    def run(self):
        current_mtime = self.cloud_directory.mtime
        new_files = self.local_directory.get_files(current_mtime)
        self.cloud_directory.upload(new_files)
