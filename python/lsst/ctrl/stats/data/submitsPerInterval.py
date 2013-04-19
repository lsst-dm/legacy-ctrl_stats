import datetime
class SubmitsPerInterval:

    def __init__(self, dbm, interval):
        self.dbm = dbm

        query = "select UNIX_TIMESTAMP(submitTime), count(*) as count from submissions where dagNode !='A' and dagNode != 'B' group by submitTime;"

        results = self.dbm.execCommandN(query)
        startTime = results[0][0]
        count = results[0][1]

        self.values = []
        # cycle through the seconds, counting the number of cores being used
        # during each interval
        last = startTime
        submits = 0
        for data in results:
            dataStartTime = data[0]
            dataSubmits = data[1]
            if dataStartTime - last < interval:
                d = datetime.datetime.fromtimestamp(dataStartTime).strftime('%Y-%m-%d %H:%M:%S')
                submits = submits + dataSubmits
            else:
                self.values.append([last,submits])
                last = dataStartTime
                submits = dataSubmits
            
        self.values.append([last,submits])
        

        # TODO: handle last elements case

    def getValues(self):
        return self.values
