import sys
sys.path.append('../src')

import os
import json
import re
from tqdm import tqdm

def order_table_evaluation(best_permutation, reorderedlist_result_query_execution_gold, transpost_list_result_query_execution_gold, transpost_list_result_query_execution_gen, row_score, column_score, weight, penalty, max_extra_information_percentage=0.25):
    w2 = 1 - weight
    if round(len(transpost_list_result_query_execution_gold[0]) * (1 + max_extra_information_percentage)) > len(transpost_list_result_query_execution_gen[0]) or round(len(transpost_list_result_query_execution_gold) * (1 + max_extra_information_percentage)) > len(transpost_list_result_query_execution_gen): 
        if row_score == 0 or column_score == 0:
            score = 0
        else:
            if len(transpost_list_result_query_execution_gold[0]) > len(transpost_list_result_query_execution_gen[0]) or len(transpost_list_result_query_execution_gold) > len(transpost_list_result_query_execution_gen):
                score = (row_score * weight + column_score * w2) * penalty
            else:
                score = (row_score * weight + column_score * w2)
    else:
        score = 0
    return score
        
def is_exact_substring(substring, main_string):
        """
        Check if a substring is exactly present within another string.
        Ensures that the substring is a whole word match.

        Parameters:
        substring (str): The substring to find.
        main_string (str): The string to search within.

        Returns:
        bool: True if the substring is found as a whole word in the main string, False otherwise.
        """
        # \b matches word boundaries
        pattern = re.compile(r'\b' + re.escape(substring) + r'\b')
        return bool(pattern.search(main_string))
    
def delete_inside_parentheses(text):
        result = []
        depth = 0
        for char in text:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            elif depth == 0:
                result.append(char)
        return ''.join(result)
    

folder_path = "../results_metric2"
# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created successfully.")
else:
    print(f"Folder '{folder_path}' already exists.")
    

embedding_folder = '../src/embed_sft-sql-embedding.json'
with open(embedding_folder, 'r') as ef:
    embedding_data = json.load(ef)  
      
embedding_folder2 = '../src/embed_UAE-Code-Large-V1.json'
with open(embedding_folder2, 'r') as ef2:
    embedding_data2 = json.load(ef2)    
    
ordered_folder = '../src/just_ORDERED_metric_res_0.5_0.0_all-MiniLM-RAGSQL-code.json'
with open(ordered_folder, 'r') as of:
    ordered_data = json.load(of)
    
base_metric_folder = '../results/metric_res_0.25_0.0_all-MiniLM-RAGSQL-code.json'
with open(base_metric_folder, 'r') as bf:
    base_metric_data = json.load(bf)
    

res_folder = '../results_metric2'

for embed_model_name in tqdm(['all-MiniLM-RAGSQL-code', 'sft-sql-embeddings', 'UAE-Code-Large-V1']):
    if not os.path.exists(os.path.join(res_folder, embed_model_name)):
        os.makedirs(os.path.join(res_folder, embed_model_name))
        # print(f"Folder '{os.path.join(res_folder, embed_model_name)}' created successfully.")
    
    for weight_final_score_table in tqdm([x / 100.0 for x in range(25, 100, 25)]):
        if not os.path.exists(os.path.join(res_folder, embed_model_name)):
            os.makedirs(os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table)))
            # print(f"Folder '{os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table))}' created successfully.")
    
        for max_extra_information_percentage in tqdm([x / 100.0 for x in range(10, 100, 10)]):
            if not os.path.exists(os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table), 'max_extra_information_percentage_'+ str(max_extra_information_percentage))):
                os.makedirs(os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table), 'max_extra_information_percentage_'+ str(max_extra_information_percentage)))
                # print(f"Folder '{os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table), 'max_extra_information_percentage_'+ str(max_extra_information_percentage))}' created successfully.")
                
                for weight in [x / 100.0 for x in range(20, 100, 20)]:
                    if not os.path.exists(os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table), 'max_extra_information_percentage_'+ str(max_extra_information_percentage), 'weight_'+ str(weight))):
                        os.makedirs(os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table), 'max_extra_information_percentage_'+ str(max_extra_information_percentage), 'weight_'+ str(weight)))
                        # print(f"Folder '{os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table), 'max_extra_information_percentage_'+ str(max_extra_information_percentage), 'weight_'+ str(weight))}' created successfully.")
            
                    for penalty in [x / 100.0 for x in range(20, 100, 20)]:
                        if not os.path.exists(os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table), 'max_extra_information_percentage_'+ str(max_extra_information_percentage), 'weight_'+ str(weight),'penalty_'+ str(penalty))):
                            os.makedirs(os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table), 'max_extra_information_percentage_'+ str(max_extra_information_percentage), 'weight_'+ str(weight), 'penalty_'+ str(penalty)))
                            # print(f"Folder '{os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table), 'max_extra_information_percentage_'+ str(max_extra_information_percentage), 'weight_'+ str(weight), 'penalty_'+ str(penalty))}' created successfully.")
                        
                        new_data = []
                        for idx_basic_data, basic_data in enumerate(base_metric_data):
                            
                            # if ordered_data[idx_basic_data]['best_permutation'] is None or ordered_data[idx_basic_data]['reorderedlist_result_query_execution_gold'] is None or ordered_data[idx_basic_data]['transpost_list_result_query_execution_gold'] is None or ordered_data[idx_basic_data]['transpost_list_result_query_execution_gen'] is None or ordered_data[idx_basic_data]['row_score'] is None or ordered_data[idx_basic_data]['column_score'] is None:
                                # print(idx_basic_data)
                                # print('='*30)
                            try:
                            
                                # print(f"{idx_basic_data} -> {ordered_data[idx_basic_data]['best_permutation']}")
                                # if ordered_data[idx_basic_data]['best_permutation'] is not None:
                                if is_exact_substring('ORDER BY', delete_inside_parentheses(basic_data['sql_gold'].upper())):
                                    for orde in ordered_data:
                                        if orde['model'] == basic_data['model'] and orde['sql_gold'] == basic_data['sql_gold'] and orde['sql_gen'] == basic_data['sql_gen']: 
                                            res_table = order_table_evaluation(orde['best_permutation'], orde['reorderedlist_result_query_execution_gold'],
                                                                            orde['transpost_list_result_query_execution_gold'],
                                                                            orde['transpost_list_result_query_execution_gen'],
                                                                            orde['row_score'], orde['column_score'],
                                                                            weight, penalty, max_extra_information_percentage)
                                # else:
                                else:
                                    res_table = basic_data['res_table']
                                
                                try:
                                    final_score_teory = (res_table * weight_final_score_table) + (basic_data['sql_sim_score'] * (1 - weight_final_score_table))
                                    new_data.append({
                                        "model": basic_data['model'],
                                        "db": basic_data['db'],
                                        "num": basic_data['num'],
                                        "sql_gold": basic_data['sql_gold'],
                                        "sql_gen": basic_data['sql_gen'],
                                        "gold_shape": basic_data['gold_shape'],
                                        "gen_shape": basic_data['gen_shape'],
                                        "res_table": res_table,
                                        "res_ves": basic_data['res_ves'],
                                        "sql_sim_score": basic_data['sql_sim_score'] if embed_model_name == 'all-MiniLM-RAGSQL-code' else embedding_data2[idx_basic_data]['sql_sim_score'] if embed_model_name == 'UAE-Code-Large-V1' else embedding_data[idx_basic_data]['sql_sim_score'],
                                        "final_score_teory": final_score_teory,
                                        "final_score": final_score_teory if res_table >= 0.1 else 0,
                                        "exec_time": basic_data['exec_time'],
                                        'error': False, 
                                        'equal_sql': True if basic_data['sql_gold'] == basic_data['sql_gen'] else False
                                    })
                                except:
                                    new_data.append({
                                        "model": basic_data['model'],
                                        "db": basic_data['db'],
                                        "num": basic_data['num'],
                                        "sql_gold": basic_data['sql_gold'],
                                        "sql_gen": basic_data['sql_gen'],
                                        "gold_shape": basic_data['gold_shape'],
                                        "gen_shape": basic_data['gen_shape'],
                                        "res_table": None,
                                        "res_ves": basic_data['res_ves'],
                                        "sql_sim_score": basic_data['sql_sim_score'] if embed_model_name == 'all-MiniLM-RAGSQL-code' else embedding_data2[idx_basic_data]['sql_sim_score'] if embed_model_name == 'UAE-Code-Large-V1' else embedding_data[idx_basic_data]['sql_sim_score'],
                                        "final_score_teory": None,
                                        "final_score": None,
                                        "exec_time": basic_data['exec_time'],
                                        'error': True,
                                        'equal_sql': True if basic_data['sql_gold'] == basic_data['sql_gen'] else False 
                                    })
                            # new_data.append({'test': idx_basic_data})
                            except:
                                new_data.append({
                                            "model": None,
                                            "db": None,
                                            "num": None,
                                            "sql_gold": None,
                                            "sql_gen": None,
                                            "gold_shape": None,
                                            "gen_shape": None,
                                            "res_table": None,
                                            "res_ves": None,
                                            "sql_sim_score": None,
                                            "final_score_teory": None,
                                            "final_score": None,
                                            "exec_time": None,
                                            'error': True,
                                            'equal_sql': None 
                                        })
                        
                        # time.sleep(0.2)

                        save_json_folder = os.path.join(res_folder, embed_model_name, 'weight_final_score_table_'+ str(weight_final_score_table), 'max_extra_information_percentage_'+ str(max_extra_information_percentage), 'weight_'+ str(weight), 'penalty_'+ str(penalty))    
                        save_json = os.path.join(save_json_folder, f'metric_res_{embed_model_name}_weight_final_score_table_{weight_final_score_table}_max_extra_information_percentage_{max_extra_information_percentage}_weight_{weight}_penalty_{penalty}.json')
                        with open(save_json, 'w') as file_to_save:
                            json.dump(new_data, file_to_save, indent=4)