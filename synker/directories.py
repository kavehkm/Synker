# standard
import os
import re
# internal
from synker.exceptions import E409
from synker.files import File, LocalFile
# external


class LocalDirectory(object):
    """Local Directory"""
    def __init__(self, path, pattern):
        self.path = path
        self._pattern = pattern

    def get_files(self, mtime):
        dirs, files = [self.path], []
        while dirs:
            entries = os.scandir(dirs.pop())
            for entry in entries:
                if entry.is_dir():
                    dirs.append(entry.path)
                if entry.is_file() and entry.stat().st_mtime > mtime and re.match(self._pattern, entry.name):
                    files.append(LocalFile(entry.name,
                                           entry.path.replace(os.sep, '/'),
                                           entry.stat().st_mtime,
                                           entry.stat().st_size,
                                           self.path))
        return sorted(files, reverse=False)


class CloudDirectory(object):
    """Cloud Directory"""
    def __init__(self, provider, path, limit, mtime_file):
        self._provider = provider
        self.path = path
        self._limit = limit
        self._mtime_file = mtime_file
        self._files = None
        self._mtime = None

    @property
    def files(self):
        if self._files is None:
            files = []
            try:
                r = self._provider.get_files(self.path)
            except E409:
                pass
            else:
                for f in r:
                    files.append(File(**f, root=self.path))
            self._files = sorted(files, reverse=False)
        return self._files

    @property
    def mtime(self):
        if self._mtime is None:
            try:
                self._mtime = self._provider.download(self._mtime_file)
            except E409:
                self._mtime = 0.0
        return self._mtime

    @mtime.setter
    def mtime(self, mt):
        self._provider.upload(self._mtime_file, b'%f' % mt)
        self._mtime = mt

    def used_space(self):
        return sum(self.files)

    def available_space(self):
        return self._limit - self.used_space()

    def _space_adjustment(self, local_files):
        size = sum(local_files)
        while size > self._limit:
            size -= local_files.pop(0).size
        while size > self.available_space():
            self.delete(self.files[0])

    def upload(self, local_files):
        self._space_adjustment(local_files)
        for lf in local_files:
            res = self._provider.upload(self.path + lf.rel_path, lf.get_content())
            self.mtime = lf.mtime
            self.files.append(File(**res, root=self.path))

    def delete(self, cloud_file):
        self._provider.delete(cloud_file.full_path)
        self.files.remove(cloud_file)
