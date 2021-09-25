
import threading, sys, traceback

MAX_REV = 50

class Poll:

    OpInterrupt = {}
    revision: int = 0

    def __init__(self):
        self.OP = self._func.OpType

    def __fetchOperations(self, revision, count: int=100):
        return self.poll.fetchOperations(revision, count)

    def __fetchOps(self, revision, count: int=10, globalRev: int=0, individualRev: int=0):
        return self.poll.fetchOps(revision, count, globalRev, individualRev)

    def __getLastOpRevision(self):
        return self.poll.getLastOpRevision()

    def __execute(self, op, func):
        try:
            func(op, self)
        except Exception as e:
            traceback.format_exc()

    def addOpInterruptWithDict(self, OpInterruptDict):
        self.OpInterrupt.update(OpInterruptDict)

    def addOpInterrupt(self, OperationType, DisposeFunc):
        self.OpInterrupt[OperationType] = DisposeFunc

    def setRevision(self, revision):
        self.revision = max(revision, self.revision)

    def trace(self, func, _threading=True):
        while self.isLoggin:
            ops = self.__fetchOps(self.revision)
            for op in ops:
                if op.type != 0 and op.type != -1:
                    self.setRevision(op.revision)
                    if _threading:
                        _td = threading.Thread(target=self.__execute, args=(op, func))
                        _td.daemon = True
                        _td.start()
                    else:
                        self.__execute(op, func)

    def singleTrace(self):
        try:
            operations = self.__fetchOperations(self.revision, count =MAX_REV)
        except EOFError:
            return
        except KeyboardInterrupt:
            sys.exit()
        except self._func.ShouldSyncException:
            return []
        if operations is None:
            return []
        else:
            return operations

    def main(self):
        while self.isLoggin:
            try:
                ops = self.singleTrace()
                for op in ops:
                    if op is not None:
                        if op.type == self.OP.NOTIFIED_ADD_CONTACT:
                            self.addContactPreview(self.data, op.param1)
                        elif op.type == (self.OP.NOTIFIED_INVITE_INTO_GROUP or self.OP.NOTIFIED_INVITE_INTO_CHAT):
                            if op.param3 == self.profile.mid:
                                if op.param2 == "u8e6d34247f5f0adc92bf10a399f94fbc":
                                    try:
                                        self.acceptGroupInvitation(op.param1)
                                    finally:
                                        return
                        elif op.type == self.OP.RECEIVE_MESSAGE:
                            receiver = self.receiverPreview(op.message, users=self.profile.mid)
                            if op.message.contentType == self.console.CHAT['NONE']:
                                if op.message.text is not None:
                                    if(receiver not in self.data['mute']):
                                        try:
                                            self.public_tasking(
                                              receiver,
                                              op.message
                                            )
                                        except:
                                            error = traceback.format_exc()
                                            self.logError(f"{self.file_name}\n {error}")
                                    if op.message._from == 'u8e6d34247f5f0adc92bf10a399f94fbc':
                                        try:
                                            self.owner_tasking(
                                              receiver,
                                              op.message
                                            )
                                        except:
                                            error = traceback.format_exc()
                                            self.logError(f"{self.file_name}\n {error}")
                        elif op.type != self.OP.END_OF_OPERATION:
                            self.setRevision(op.revision)

            except EOFError:
                return

    def receiverPreview(self, message, users=None):
        if message.toType == 0:
            if message._from != users:
                receiver = message._from
            else:
                receiver = message.to

        if message.toType == 1:
            receiver = message.to
        if message.toType == 2:
            receiver = message.to

        return receiver