import pg8000
import os

# import pyodbc

# Used for testing
default_db_host = ""
default_db_name = ""
default_db_user = ""
default_db_pass = ""

def get_postgres_provider():
    return PostGresProvider(__get_database_info_from_env())


def __get_database_info_from_env():
    return DatabaseInfo(os.getenv('DB_HOST', default_db_host), os.getenv('DB_NAME', default_db_name),
                        os.getenv('DB_USER', default_db_user), os.getenv('DB_PASS', default_db_pass))


class DatabaseInfo(object):
    def __init__(self, db_host_name, db_name, db_user_name, db_password):
        self.db_host_name = db_host_name
        self.db_name = db_name
        self.db_user_name = db_user_name
        self.db_password = db_password


class DBProvider(object):
    def __new_connection(self, host_name, db_name, db_user, db_pass): pass

    def get_connection(self): pass

    def cursor(self): pass

    def execute(self, query): pass


class PostGresProvider(DBProvider):

    def __init__(self, database_info):
        self.database_info = database_info

    def __new_connection(self, host_name, db_name, db_user, db_pass):
        return pg8000.connect(db_user, host=host_name, unix_sock=None, port=5432, database=db_name, password=db_pass,
                              ssl=True, timeout=None, application_name=None)

    def get_connection(self):
        # self.connection =
        return self.__new_connection(self.database_info.db_host_name, self.database_info.db_name,
                                     self.database_info.db_user_name, self.database_info.db_password)


'''
class MSSqlProvider(DBProvider):
    DRIVER= '{ODBC Driver 17 for SQL Server}'
    def __init__(self, database_info):
        self.database_info = database_info

    def __new_connection(self,host_name,db_name,db_user,db_pass):
        return pyodbc.connect('DRIVER='+self.DRIVER+';PORT=1433;SERVER='+host_name+';PORT=1443;DATABASE='+db_name+';UID='+db_user+';PWD='+ db_pass)

    def get_connection(self):
        return self.__new_connection(self.database_info.db_host_name,self.database_info.db_name,self.database_info.db_user_name,self.database_info.db_password)
'''