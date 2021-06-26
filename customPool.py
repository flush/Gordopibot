import mariadb
class CustomPool:
    def __init__(self, dbconfig):
        self.dbconfig = dbconfig

    def get_connection(self):
            return mariadb.connect(**self.dbconfig)


