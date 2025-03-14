import sys
sys.path.append('../src')

from dataScripts.DataQuery import DataQuery, DataTable, DataManager

import ijson
import json
import os
from astEmbedding.sql_embedder import SQLEmbeddingComparer
from evaluation.Evaluator import tableEvaluator
from databasesFacilitator.databaseInterpreter import DatabaseInterpreterPandas
from collections import Counter
import time
from datetime import timedelta
import tqdm

SQL_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE",
    "CREATE", "TABLE", "ALTER", "ADD", "DROP", "TRUNCATE", "JOIN", "INNER", "LEFT",
    "RIGHT", "FULL", "OUTER", "GROUP", "BY", "ORDER", "HAVING", "UNION", "DISTINCT",
    "LIMIT", "OFFSET"
] 

def elementi_comuni_con_duplicati(lista1, lista2):
        # Creiamo un Counter per ciascuna lista
        counter1 = Counter(lista1)
        counter2 = Counter(lista2)
        # Troviamo l'intersezione dei due Counter
        comuni = counter1 & counter2
        # Calcoliamo il numero totale di elementi in comune, considerando i duplicati
        num_comuni = sum(comuni.values())
        
        return num_comuni / max(len(lista1), len(lista2))

def sql_similarity_score(sql1: str, sql2: str, compare_ast: bool = False):
    embedding_comparer = SQLEmbeddingComparer(trust_remote_code=True)
    similarity_score = embedding_comparer.compare_embeddings(sql1, sql2, compare_ast)
    return similarity_score

# def read_json_with_sql(json_file_path, sql_folder_path = None):
#     """
#     Reads a JSON file partially, yielding up to max_records items with added SQL information.
    
#     :param json_file_path: Path to the JSON file.
#     :param sql_folder_path: Path to the folder containing SQL files.
#     :param max_records: Maximum number of records to read from the JSON file.
#     :yield: Parsed JSON objects with added SQL information.
#     """
#     # Read SQL files
#     if sql_folder_path is not None:
#         sql_contents = read_sql_files(sql_folder_path)
#     i = 0
#     # Add SQL information to each item
#     if sql_folder_path is not None:
#         for sql_key, sql_lines in sql_contents.items():
#             print(sql_key)
#             with open(json_file_path, 'r') as f:
#                 for item in ijson.items(f, 'item'):
#                     print(i)
#                     item['sql_model'] = sql_key
#                     item['sql_generated'] = sql_lines[i]
#                     # print(sql_lines[i])
#                     i = i + 1
#                     yield item

# def read_sql_files(folder_path):
#     result = {}
    
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.sql'):
#             file_path = os.path.join(folder_path, filename)
            
#             with open(file_path, 'r') as file:
#                 lines = [line.strip() for line in file.readlines() if line.strip()]
                
#                 # print(f"Contents of {filename}:")
#                 # for line in lines:
#                     # print(line)
#                 # print()  # Empty line for separation
                
#                 result[filename.replace('.sql', '')] = lines
    
#     return result

if __name__ == "__main__":
    print("START")
    start_time = time.time()
    # Example usage
    folder_path_predicted = '/mnt/data/gpinna/sql_metric/sql_metric/data/raw_data/predict_from_models/bird_dev'
    file_path_DataManager = '/mnt/data/gpinna/sql_metric/sql_metric/data/raw_data/dev'
    my_data_manager = DataManager(file_path_DataManager, db_name = None, sql_generated_path = folder_path_predicted)
    print(len(my_data_manager.data_query))
    print("start comparing")
    metric_res = []
    tab_eval = tableEvaluator()
    for i in range(len(my_data_manager.data_query)):
        try:
            start_single = time.time()
            interpreter = DatabaseInterpreterPandas(my_data_manager.data_query[i].db_id, '/mnt/data/gpinna/sql_metric/sql_metric/data/raw_data/dev', dataManager= my_data_manager)
            interpreter.load_database(path = None, index=i)
            print(i)
            gold_table, gen_table, res_table, res_ves = tab_eval.evaluate(my_data_manager.data_query[i].SQL, my_data_manager.data_query[i].sql_generated, interpreter)
            sql_sim_score = sql_similarity_score(sql1=my_data_manager.data_query[i].SQL, sql2=my_data_manager.data_query[i].sql_generated)[0]
            # common_keywords = elementi_comuni_con_duplicati(extract_sql_keywords(sql_gold), extract_sql_keywords(sql_gen))
            if res_table < 0.1:
                final_score = res_table
            else:
                # print(sql_sim_score)
                # print("="*30)
                # print(type(sql_sim_score))
                final_score = (res_table * 0.5 + sql_sim_score * 0.5) #/ 2
            if final_score < 0:
                final_score = 0.0
        except:
            print(f'except {i} ')
            res_table = None
            res_ves = None
            sql_sim_score = None
            final_score = None
            
        end_single = time.time()
        exec_single = timedelta(seconds=end_single - start_single)
        metric_res.append({'model': my_data_manager.data_query[i].sql_model,
            'db': my_data_manager.data_query[i].db_id,
            'sql_gold': my_data_manager.data_query[i].SQL,
            'sql_gen': my_data_manager.data_query[i].sql_generated,
            'res_table': res_table, 'res_ves': res_ves, 'sql_sim_score':sql_sim_score, 'final_score':final_score,
            'exec_time': str(exec_single)})
    
    end_time = time.time()
    execution_time = timedelta(seconds=end_time - start_time)
    print(f"total time spend: {execution_time}")
    with open('metric_res.json', 'w') as outfile:
            json.dump(metric_res, outfile, indent=2)
    
    print("end comparing")
    print("END")

    
    