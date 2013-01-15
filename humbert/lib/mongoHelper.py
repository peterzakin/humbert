#mongo mix in
import sys
sys.path.append('humbert/')
import pymongo
import constants.py

class mongoHelper():
     
    def connect(self):
        if self.ENVIRONMENT == 'test':
            return self._connect_on_dev()
        else:
            return self._connect_on_prod()

    def _connect_on_prod(self):
        mongo_uri = constants.mongo_uri
        connection = pymongo.Connection(mongo_uri)
        return connection 

    def _connect_on_dev(self):
        connection = pymongo.MongoClient()
        return connection 
 
