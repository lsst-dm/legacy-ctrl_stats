class SubmissionTimes:

    def __init__(self, host, port, database):
        #
        # get database authorization info
        #
        dbAuth = DbAuth()
        user = dbAuth.username(host, str(port))
        password = dbAuth.password(host,str(port))
    
        # connect to the database
        dbm = DatabaseManager(host, port, user, password)
    
    
        dbm.execCommand0('use '+database)
    
    
        q0 = 'select dagNode, executionHost, slotName, UNIX_TIMESTAMP(executionStartTime), UNIX_TIMESTAMP(executionStopTime) from submissions;'
    
        results = dbm.execCommandN(q0)
    
        entries = []
        for res in results:
            dbEnt = DbEntry(res)
            entries.append(dbEnt)
    

    def getEntries(self):
        return entries
