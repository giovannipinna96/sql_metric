import sys
sys.path.append('../src')

from dataScripts.DataQuery import DataQuery, DataTable, DataManager

import ijson


def read_json_partial(file_path, max_records=10):
    """
    Reads a JSON file partially, yielding up to max_records items.
    
    :param file_path: Path to the JSON file.
    :param max_records: Maximum number of records to read from the JSON file.
    :yield: Parsed JSON objects.
    """
    records_read = 0

    with open(file_path, 'r') as f:
        # Assuming the JSON file contains an array of objects
        for item in ijson.items(f, 'item'):
            yield item
            records_read += 1
            if records_read >= max_records:
                break

# Example usage
if __name__ == "__main__":
    print("Test DataQuery")
    file_path_DataQuery = '/mnt/data/gpinna/lisbona_sql_metric/sql_metric/data/raw_data/dev/dev.json' # Also valid for dev_tired_append.json
    data_query_list = []
    for record in read_json_partial(file_path_DataQuery, max_records=5):
        data_query_list.append(DataQuery(**record, path = file_path_DataQuery))        
    print(data_query_list[0])
    print("End Test DataQuery")
    print("="*30)
    print("Test DataTable")
    file_path_DataTable = '/mnt/data/gpinna/lisbona_sql_metric/sql_metric/data/raw_data/dev/dev_tables.json'
    data_table_list = []
    for record in read_json_partial(file_path_DataTable, max_records=5):
        data_table_list.append(DataTable(**record, path = file_path_DataTable))        
    print(data_table_list[0])
    print("End Test DataTable")
    print("="*30)
    print("Test DataManager")
    file_path_DataManager = '/mnt/data/gpinna/lisbona_sql_metric/sql_metric/data/raw_data/dev'
    db_name_DataManager = 'california_schools'
    my_data_manager = DataManager(db_name_DataManager, file_path_DataManager)
    print(my_data_manager.db_name)
    print(my_data_manager.path)
    print(my_data_manager)
    print("*"*30)
    print(my_data_manager.data_query[0])
    print("*"*30)
    print(my_data_manager.data_table[0])
    print("*"*30)
    print(my_data_manager.tables_info.keys())
    print("*"*30)
    print(my_data_manager.tables_info['schools.csv'].head(2))
    print("*"*30)
    print("End Test DataManager")
