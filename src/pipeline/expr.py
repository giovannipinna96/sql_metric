import sys
sys.path.append('../src')

import argparse

from dataScripts.DataQuery import DataQuery, DataTable, DataManager
from datetime import timedelta
import ijson
import json
import os
from astEmbedding.sql_embedder import SQLEmbeddingComparer
from evaluation.Evaluator_err import tableEvaluator
from databasesFacilitator.databaseInterpreter import DatabaseInterpreterPandas
from collections import Counter
import time
from datetime import timedelta
import tqdm
from multiprocessing import Pool, cpu_count
from functools import partial

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

def sql_similarity_score(sql1: str, sql2: str, embedding_comparer, compare_ast: bool = False):
    # embedding_comparer = SQLEmbeddingComparer(model_name=model_name, trust_remote_code=True)
    similarity_score = embedding_comparer.compare_embeddings(sql1, sql2, compare_ast)
    return similarity_score

def process_single_query(i, args, my_data_manager, tab_eval, embedding_comparer):
    start_single = time.time()
    try:
        interpreter = DatabaseInterpreterPandas(my_data_manager.data_query[i].db_id, '/mnt/data/gpinna/sql_metric/sql_metric/data/raw_data/dev', dataManager=my_data_manager)
        interpreter.load_database(path=None, index=i)
        
        gold_table, gen_table, res_table, res_ves, best_permutation, reorderedlist_result_query_execution_gold, transpost_list_result_query_execution_gold, transpost_list_result_query_execution_gen, row_score, column_score = tab_eval.evaluate(
            my_data_manager.data_query[i].SQL,
            my_data_manager.data_query[i].sql_generated,
            interpreter,
            max_extra_information_percentage=args.max_extra_information_percentage
        )
        
        sql_sim_score = sql_similarity_score(
            sql1=my_data_manager.data_query[i].SQL,
            sql2=my_data_manager.data_query[i].sql_generated,
            embedding_comparer=embedding_comparer
        )[0]
        
        weight_final_score_sim = 1 - args.weight_final_score_table
        if res_table < 0.1:
            final_score = res_table
        else:
            final_score = (res_table * args.weight_final_score_table + sql_sim_score * weight_final_score_sim)
        
        if final_score < 0:
            final_score = 0.000
        
    except Exception as e:
        print(f'Exception in query {i}: {e}')
        res_table = res_ves = sql_sim_score = final_score = None
        gold_table = gen_table = None
    
    end_single = time.time()
    exec_single = timedelta(seconds=end_single - start_single)
    
    try:
        return {
            'model': my_data_manager.data_query[i].sql_model,
            'db': my_data_manager.data_query[i].db_id,
            'num': i,
            'sql_gold': my_data_manager.data_query[i].SQL,
            'sql_gen': my_data_manager.data_query[i].sql_generated,
            'gold_shape': str(gold_table.shape) if gold_table is not None else None,
            'gen_shape': str(gen_table.shape) if gen_table is not None else None,
            'res_table': res_table,
            'res_ves': res_ves,
            'sql_sim_score': sql_sim_score,
            'final_score': final_score,
            'exec_time': str(exec_single),
            'best_permutation': best_permutation, 'reorderedlist_result_query_execution_gold':reorderedlist_result_query_execution_gold,
            'transpost_list_result_query_execution_gold':transpost_list_result_query_execution_gold,
            'transpost_list_result_query_execution_gen':transpost_list_result_query_execution_gen,
            'row_score':row_score, 'column_score':column_score
        }
    except:
        return {
        'model': my_data_manager.data_query[i].sql_model,
        'db': my_data_manager.data_query[i].db_id,
        'num': i,
        'sql_gold': my_data_manager.data_query[i].SQL,
        'sql_gen': my_data_manager.data_query[i].sql_generated,
        'gold_shape': str(gold_table.shape) if gold_table is not None else None,
        'gen_shape': str(gen_table.shape) if gen_table is not None else None,
        'res_table': res_table,
        'res_ves': res_ves,
        'sql_sim_score': sql_sim_score,
        'final_score': final_score,
        'exec_time': str(exec_single),
        'best_permutation': None, 'reorderedlist_result_query_execution_gold':None,
        'transpost_list_result_query_execution_gold':None,
        'transpost_list_result_query_execution_gen':None,
        'row_score':None, 'column_score':None, 'error':True
    }

def main():
    parser = argparse.ArgumentParser(description='Process some float inputs.')
    parser.add_argument('--max_extra_information_percentage', type=float, help='over that percentage the score will be zero')
    parser.add_argument('--model_name', type=str, help='model to create embedding of the SQLs')
    parser.add_argument('--weight_final_score_table', type=float, help='weight for table score to be given in final score', default=0.5)
    args = parser.parse_args()
    
    print("START")
    start_time = time.time()
    
    folder_path_predicted = '/mnt/data/gpinna/sql_metric/sql_metric/data/raw_data/predict_from_models/bird_dev'
    file_path_DataManager = '/mnt/data/gpinna/sql_metric/sql_metric/data/raw_data/dev'
    my_data_manager = DataManager(file_path_DataManager, db_name=None, sql_generated_path=folder_path_predicted)
    
    print(f"Number of queries: {len(my_data_manager.data_query)}")
    print("Start comparing")
    
    tab_eval = tableEvaluator()
    embedding_comparer = SQLEmbeddingComparer(model_name=args.model_name, trust_remote_code=True)
    
    # Partial function to fix some arguments
    process_func = partial(process_single_query, args=args, my_data_manager=my_data_manager, tab_eval=tab_eval, embedding_comparer=embedding_comparer)
    
    # Use all available cores
    num_cores = cpu_count()
    print(f"Using {num_cores} cores")
    
    with Pool(num_cores) as pool:
        metric_res = pool.map(process_func, range(len(my_data_manager.data_query)))
    
    end_time = time.time()
    execution_time = timedelta(seconds=end_time - start_time)
    print(f"Total time spent: {execution_time}")
    
    output_filename = f'a_Parallel_metric_res_{args.weight_final_score_table}_{args.max_extra_information_percentage}_{args.model_name.split("/")[-1]}.json'
    with open(output_filename, 'w') as outfile:
        json.dump(metric_res, outfile, indent=2)
    
    print("End comparing")
    print("END")

if __name__ == "__main__":
    main()