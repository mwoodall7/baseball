import os
from datetime import datetime, timedelta


class RecordKeeper:

    def __init__(self, filePath, daysToKeep):
        self.filePath = filePath
        self.daysToKeep = timedelta(days=daysToKeep)
        self.recordsToRemove = []
        self.currentTime = datetime.now()


    def processRecords(self):
        self.findRecordsToRemove()
        self.removeOldRecords()


    def findRecordsToRemove(self):
        for (dirpath, _, files) in os.walk(self.filePath):
            for file in files:
                localFilePath = os.path.join(dirpath, file)
                modifiedTimeStamp = datetime.fromtimestamp(os.path.getmtime(localFilePath))
                if (self.currentTime - modifiedTimeStamp) > self.daysToKeep:
                    self.recordsToRemove.append(localFilePath)


    def removeOldRecords(self):
        if self.recordsToRemove:
            for record in self.recordsToRemove:
                os.remove(record)
                print("Removed {}".format(record))
        else:
            print("No records to remove.")
