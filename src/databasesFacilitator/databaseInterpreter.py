import sqlite3
import time
import pandas as pd
from abc import ABC, abstractmethod

class DatabaseManager(ABC):
    
    def __init__(self, database_name: str) -> None:
        super().__init__()
        self.database_name = database_name
        self._connection_status = False
        self._connection = None
        
    @property
    def connection_status(self) -> bool:
        return self._connection_status
        
    def load_database(self) -> None:
        print("Loading database...")
        try:
            self._connection = sqlite3.connect(self.database_name)
            print("Connection established")
            self._connection_status = True
        except Exception as e:
            print(f"Connection failed: {e}")
    
    def close_connection(self) -> None:
        print("Closing connection...")
        self._connection.close()
        print("Connection closed")
        self._connection_status = False
        
    @abstractmethod
    def populate_database(self) -> None:
        print("Populating database...") 
        pass
    
    @abstractmethod
    def quey_executor(self, query: str) -> None:
        pass


class DatabaseInterpreter(DatabaseManager):
    def __init__(self, database_name: str) -> None:
        super().__init__(database_name)
        self.__type = "SQLite"
        
    @property
    def type(self) -> str:
        return self.__type
        
    def quey_executor(self, query: str) -> None:
        if self.connection_status:
            print("Executing query...")
            start_time = time.time()
            cursor = self._connection.cursor()
            result_query_execution = cursor.execute(query)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Query executed")
            return result_query_execution, execution_time
        else:
            print("Connection not established please create a connection before executing queries")
            return None
           
        
class DatabaseInterpreterPandas(DatabaseManager):
    def __init__(self, database_name: str) -> None:
        super().__init__(database_name)
        self.__type = "Pandas"
        
    @property
    def type(self) -> str:
        return self.__type
        
    
    def quey_executor(self, query: str) -> None:
        if self._connection is not None:
            print("Executing query...")
            start_time = time.time()
            result_query_execution = pd.read_sql_query(query, self._connection)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Query executed")
            return result_query_execution, execution_time
        else:
            print("Connection not established please create a connection before executing queries")
            return None