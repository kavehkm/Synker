class File(object):
    """File"""
    def __init__(self, name, full_path, mtime, size, root):
        self.name = name
        self.full_path = full_path
        self.mtime = mtime
        self.size = size
        self.root = root
        self._rel_path = None

    @property
    def rel_path(self):
        if self._rel_path is None:
            self._rel_path = self.full_path[len(self.root):]
        return self._rel_path

    def __eq__(self, other):
        return self.mtime == other.mtime

    def __ne__(self, other):
        return self.mtime != other.mtime

    def __gt__(self, other):
        return self.mtime > other.mtime

    def __ge__(self, other):
        return self.mtime >= other.mtime

    def __lt__(self, other):
        return self.mtime < other.mtime

    def __le__(self, other):
        return self.mtime <= other.mtime

    def __add__(self, other):
        return self.size + other

    def __radd__(self, other):
        return self.size + other

    def __repr__(self):
        return self.full_path


class LocalFile(File):
    """Local File"""
    def get_content(self, frmt='b'):
        with open(self.full_path, 'r' + frmt) as f:
            c = f.read()
        return c

    def set_content(self, c, frmt='b'):
        with open(self.full_path, 'w' + frmt) as f:
            f.write(c)
