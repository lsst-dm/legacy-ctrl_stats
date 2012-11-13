import MySQLdb
class DbRecord(object):

    def printValues(self, obj):
        members = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
        for mem in members:
            value = getattr(self, mem)
            print mem, "=", value

    def getInsertString(self, tableName):
        members = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
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
