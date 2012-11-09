import MySQLdb
class DbRecord(object):
    def __init__(self):
        self.condorId = None
        self.dagNode = None
        self.submitTime = None
        self.executionHost = None
        self.executionStartTime = None
        self.executionStopTime = None
        self.userRunRemoteUsage = 0
        self.sysRunRemoteUsage = 0
        self.userRunLocalUsage = 0
        self.sysRunLocalUsage = 0
        self.bytesSent = 0
        self.bytesReceived = 0
        self.evicted = None
        self.terminationTime = None
        self.terminationCode = None
        self.terminationReason = None

    def printValues(self):
        members = [attr for attr in dir(DbRecord()) if not callable(getattr(DbRecord(),attr)) and not attr.startswith("__")]
        for mem in members:
            value = getattr(self, mem)
            print mem, "=", value

    def getInsertString(self, tableName):
        members = [attr for attr in dir(DbRecord()) if not callable(getattr(DbRecord(),attr)) and not attr.startswith("__")]
        cmd = "INSERT INTO %s (" % (tableName)
        first = True
        for mem in members:
            if first:
                add = mem
                first = False
            else:
                add = ", "+mem
            cmd = cmd+add
        cmd = cmd+") VALUES ("
        first = True
        for mem in members:
            value = getattr(self, mem)
            if value is None:
                value = ""
            if first:
                if type(value) == type(str()):
                    add = "'"+MySQLdb.escape_string(value)+"'"
                else:
                    add = str(value)
                first = False
            else:
                if type(value) == type(str()):
                    add = ", '"+MySQLdb.escape_string(value)+"'"
                else:
                    add = ", "+str(value)
            cmd = cmd+add
        cmd = cmd+")"
        return cmd
