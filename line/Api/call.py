from typing import List

from ..curve.console import Console
listen = Console.line_thrift

class Call:

    def __init__(self):
        if self.isLoggin:
            if self.mod == "binary": path = "/V3"
            else: path = self.endpoint.CALL
            self.call = self._connect(host=self.host,
                                         path= path,
                                         Headers= self.headers,
                                         service= self.console.CallService,
                                         method = self.mod
            )

    def getUserStatus(self, mid: str):
        return self.call.getUserStatus(0,mid)

    def acquireGroupCallRoute(self, chatMid: str, mediaType: listen.GroupCallMediaType):
        return self.call.acquireGroupCallRoute(0,chatMid, mediaType)

    def inviteIntoGroupCall(self, chatMid: str, memberMids: List[str], mediaType: listen.GroupCallMediaType):
        return self.call.inviteIntoGroupCall(0, chatMid, memberMids, mediaType)
     
    def getGroupCall(self, chatMid: str) -> listen.GroupCall:
        return self.call.getGroupCall(0, chatMid)