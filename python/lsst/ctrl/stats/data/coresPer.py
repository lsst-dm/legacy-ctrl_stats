import datetime
class CoresPer:

    def calculateMax(self):
        # count the number of cores used at maximum
        # also calculate the first time that many cores were used
        # and the last time that many cores were used.
        maximumCores = -1
        timeFirstUsed = None
        timeLastUsed = None
        for j in range(len(self.values)):
            val = self.values[j]
            timeValue = val[0]
            cores = val[1]
            # this counts the times the maximum cores
            # were first used
            if cores > maximumCores:
                maximumCores = cores
                timeFirstUsed = timeValue
            # this extra conditional also tallies the
            # last time all the cores were used
            if cores == maximumCores:
                timeLastUsed = timeValue
        return maximumCores, timeFirstUsed, timeLastUsed
    
    def getValues(self):
        return self.values

    def getMaximumCores(self):
        return self.maximumCores

    def maximumCoresFirstUsed(self):
        return self.timeFirstUsed

    def maximumCoresLastUsed(self):
        return self.timeLastUsed

