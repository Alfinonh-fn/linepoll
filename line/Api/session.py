from requests.sessions import Session

import logging, json, urllib.parse, shutil, os

class Server:

    def __init__(self):
        self._session = Session()
        self.headers = {}
        self.timelineHeaders = {}

    def additionalHeaders(self, source, newSource):
        headerList={}
        headerList.update(source)
        headerList.update(newSource)
        return headerList

    def urlEncode(self, url, path, params=[]):
        return url + path + '?' + urllib.parse.urlencode(params)

    def getJson(self, url, allowHeader=False):
        if allowHeader is False:
            return json.loads(self._session.get(url).text)
        else:
            return json.loads(self._session.get(url, headers=self.headers).text)

    def optionsContent(self, url, headers=None, data=None):
        if headers is None:
            headers=self.headers

        return self._session.options(url, headers=headers, data=data)

    def postContent(self, url, headers=None, data=None, files=None, json=None):
        if headers is None:
            headers=self.headers

        return self._session.post(url, headers=headers, data=data, files=files, json=json)

    def getContent(self, url, headers=None):
        if headers is None:
            headers=self.headers

        return self._session.get(url, headers=headers, stream=True)

    def deleteContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.headers

        return self._session.delete(url, headers=headers, data=data)

    def putContent(self, url, headers=None, data=None):
        if headers is None:
            headers=self.headers

        return self._session.put(url, headers=headers, data=data)

    def saveFile(self, path, raw):
        with open(path, 'wb') as f:
            shutil.copyfileobj(raw, f)

    def deleteFile(self, path):
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False