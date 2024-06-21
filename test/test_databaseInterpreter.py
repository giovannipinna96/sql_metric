import sys
sys.path.append('../src')

from databasesFacilitator.databaseInterpreter import DatabaseInterpreterPandas, DatabaseInterpreter

if "__main__" == __name__:
    print("Test DatabaseInterpreterPandas")
    interpreter = DatabaseInterpreterPandas("california_schools", '/mnt/data/gpinna/lisbona_sql_metric/sql_metric/data/raw_data/dev')
    print(interpreter.type)
    print(interpreter.connection_status)
    print("Loading database...")
    interpreter.load_database()
    print(interpreter.connection_status)
    # interpreter.populate_database()
    print(interpreter.data_manager.tables_info.keys())
    print("Tray to execute a query")
    query = "SELECT * FROM satscores ORDER BY AvgScrWrite DESC LIMIT 5"
    result_query_execution, execution_time = interpreter.quey_executor(query)
    print(result_query_execution)
    print(type(result_query_execution))
    print(execution_time)
    interpreter.close_connection()
    
    print("Test DataInterpreter")
    # TODO
    