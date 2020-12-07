# standard
from datetime import datetime
# internal
from synker import exceptions as se
# external
from requests import post
from requests.exceptions import RequestException


class DropboxProvider(object):
    """Dropbox Provider"""
    _datetime_format = '%Y-%m-%dT%H:%M:%SZ'
    _urls = {
        'acc_info': 'https://api.dropboxapi.com/2/users/get_current_account',
        'files':    'https://api.dropboxapi.com/2/files/list_folder',
        'delete':   'https://api.dropboxapi.com/2/files/delete',
        'upload':   'https://content.dropboxapi.com/2/files/upload',
        'download': 'https://content.dropboxapi.com/2/files/download'}

    def __init__(self):
        self._token = None

    def _file_format(self, i):
        return {
            'name': i['name'],
            'size': i['size'],
            'full_path': i['path_display'],
            'mtime': datetime.strptime(i['client_modified'], self._datetime_format).timestamp()}

    def _send_request(self, p, token=None):
        if token is None:
            token = self._token
        headers = p.get('headers', {})
        headers['Authorization'] = 'Bearer {}'.format(token)
        p['headers'] = headers
        try:
            r = post(**p)
        except RequestException:
            raise se.E000
        else:
            sc = r.status_code
            if sc == 200:
                return r
            elif sc == 400:
                raise se.E400(details=r.text)
            elif sc == 401:
                raise se.E401(details=r.text)
            elif sc == 403:
                raise se.E403(details=r.text)
            elif sc == 409:
                raise se.E409(details=r.text)
            elif sc == 429:
                raise se.E429(details=r.text)
            else:
                raise se.E5XX(details=r.text)

    def set_token(self, t):
        p = {
            'url': self._urls['acc_info']
        }
        r = self._send_request(p, t).json()
        self._token = t
        return {
            'email': r['email'],
            'name': r['name']['display_name']
        }

    def get_files(self, path, recursive=True):
        p = {
            'url': self._urls['files'],
            'headers': {
                'Content-Type': 'application/json'
            },
            'json': {
                'path': path,
                'recursive': recursive
            }
        }
        r = self._send_request(p).json()
        files = []
        for entry in r.get('entries', []):
            if entry.get('.tag') == 'file':
                files.append(self._file_format(entry))
        return files

    def upload(self, path, content, mode='overwrite'):
        p = {
            'url': self._urls['upload'],
            'headers': {
                'Dropbox-API-Arg': json.dumps({
                    'path': path,
                    'mode': mode
                }),
                'Content-Type': 'application/octet-stream'
            },
            'data': content
        }
        r = self._send_request(p).json()
        return self._file_format(r)

    def download(self, path, frmt='j'):
        p = {
            'url': self._urls['download'],
            'headers': {
                'Dropbox-API-Arg': json.dumps({
                    'path': path
                })
            }
        }
        r = self._send_request(p)
        if frmt == 'b':
            r = r.content
        elif frmt == 'j':
            r = r.json()
        elif frmt == 't':
            r = r.text
        return r

    def delete(self, path):
        p = {
            'url': self._urls['delete'],
            'json': {'path': path},
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        r = self._send_request(p).json()
        return self._file_format(r)
