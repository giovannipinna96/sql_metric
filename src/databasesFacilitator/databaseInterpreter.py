import sys
sys.path.append('../src')
import sqlite3
import time
import pandas as pd
import pandasql as psql
from abc import ABC, abstractmethod
from dataScripts.DataQuery import DataManager
import os

class DatabaseManager(ABC):
    
    def __init__(self, database_name: str) -> None:
        super().__init__()
        self.database_name = database_name
        self._connection_status = False
        self._connection = None
        self.data_manager: DataManager | None = None

        
    @property
    def connection_status(self) -> bool:
        return self._connection_status
        
    def load_database(self, path: str) -> None:
        # print("Loading database...")
        try:
            self._connection = sqlite3.connect(path)
            # print("Connection established")
            self._connection_status = True
        except Exception as e:
            print(f"Connection failed: {e}")
                
                
    def close_connection(self) -> None:
        print("Closing connection...")
        self._connection.close()
        print("Connection closed")
        self._connection_status = False

    
    @abstractmethod
    def query_executor(self, query: str) -> None:
        pass


class DatabaseInterpreter(DatabaseManager):
    def __init__(self, database_name: str | None = None, dataManager: DataManager | None = None) -> None:
        if database_name is None and dataManager is None:
            raise ValueError("Please provide either a database name or a data table")
        super().__init__(database_name)
        self.data_manager = dataManager
        self.__type = "SQLite"
        
    @property
    def type(self) -> str:
        return self.__type
       
    def query_executor(self, query: str) -> None:
        if self.connection_status:
            # print("Executing query...")
            start_time = time.time()
            cursor = self._connection.cursor()
            result_query_execution = cursor.execute(query)
            end_time = time.time()
            execution_time = end_time - start_time
            # print("Query executed")
            return result_query_execution, execution_time
        else:
            print("Connection not established please create a connection before executing queries")
            return None
           
        
class DatabaseInterpreterPandas(DatabaseManager):
    def __init__(self, database_name: str | None = None, path: str | None = None, dataManager: DataManager | None = None) -> None:
        if database_name is not None and path is not None and dataManager is None:
            super().__init__(database_name)
            self.path = path
            self.data_manager = DataManager(database_name, path)
        elif database_name is None and path is None and dataManager is not None:
            super().__init__(dataManager.db_name)
            self.path = dataManager.path
            self.data_manager = dataManager
        elif database_name is None and path is not None and dataManager is None:
            self.path = path
            self.data_manager = DataManager("Not known", path)
            self.database_name = "Not known"
            print("ATTENTION you not provide a database name, for this reason the database name will be 'Not known'")
        else:
            self.path = path
            self.data_manager = dataManager
            self.database_name = database_name
            # raise ValueError("Please provide a database name and a path OR a data table OR a path")         
        self.__type = "Pandas"
    @property
    def type(self) -> str:
        return self.__type
    
    def load_database(self, path: str | None = None, index: int | None = None) -> None:
        if path is not None:
            super().load_database(path)
        else:
            print(os.path.join(self.path, "dev_databases", self.data_manager.data_query[index].db_id, f"{self.data_manager.data_query[index].db_id}.sqlite"))
            super().load_database(os.path.join(self.path, "dev_databases", self.data_manager.data_query[index].db_id, f"{self.data_manager.data_query[index].db_id}.sqlite"))
            
    
    def query_executor(self, query: str):
        if self._connection is not None:
            # print("Executing query...")
            start_time = time.time()
            result_query_execution = pd.read_sql_query(query, self._connection)
            end_time = time.time()
            execution_time = end_time - start_time
            # print("Query executed")
            return result_query_execution, execution_time
        else:
            print("Connection not established please create a connection before executing queries")
            return None
   