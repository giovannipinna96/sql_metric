import sys
sys.path.append('../src')

import gradio as gr
from collections import Counter
import re
import json

from evaluation.Evaluator import tableEvaluator
from databasesFacilitator.databaseInterpreter import DatabaseInterpreterPandas

from astEmbedding.sql_embedder import SQLEmbeddingComparer

ALL_DB = ["california_schools", "card_games", "codebase_community", "debit_card_specializing", "european_football_2", "financial", "formula_1",
     "student_club", "superhero", "thrombosis_prediction", "toxicology"]


def sql_similarity_score(sql1: str, sql2: str, compare_ast: bool = False):
    if sql1 == sql2:
        return [1.0]
    else:
        embedding_comparer = SQLEmbeddingComparer(trust_remote_code=True)
        similarity_score = embedding_comparer.compare_embeddings(sql1, sql2, compare_ast)
        return similarity_score
    
def process_inputs(sql_gold, sql_gen, dropdown_value):
    # dropdown_value = ALL_DB[dropdown_value]
    tab_eval = tableEvaluator()
    interpreter = DatabaseInterpreterPandas(dropdown_value, '/mnt/data/gpinna/sql_metric/sql_metric/data/raw_data/dev')
    interpreter.load_database()
    gold_table, gen_table, res_table, res_ves, is_order, more = tab_eval.evaluate(sql_gold, sql_gen, interpreter)
    common_keywords = sql_similarity_score(sql1=sql_gold, sql2=sql_gen)[0]
    # common_keywords = elementi_comuni_con_duplicati(extract_sql_keywords(sql_gold), extract_sql_keywords(sql_gen))
    if res_table < 0.1:
        final_score = res_table
    else:
        final_score = (res_table * 0.5 + common_keywords * 0.5) #/ 2
    
    if final_score < 0:
        final_score = 0.0
        
    return gold_table, gen_table, res_table, res_ves, common_keywords, final_score


gold = "SELECT T2.MailStreet FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode ORDER BY T1.`FRPM Count (K-12)` DESC LIMIT 1"
queries_lim = ['SELECT mailstreet, mailstrabr, mailcity, mailzip FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 1);',
               'SELECT mailstreet, mailstrabr, mailcity, mailzip FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 2);',
               'SELECT mailstreet, mailstrabr, mailcity, mailzip FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 3);',
               'SELECT mailstreet, mailstrabr, mailcity, mailzip FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 4);'
               ]
queries_same_col_change_lim = ['SELECT mailstreet FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 1);',
                               'SELECT mailstreet FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 2);',
                               'SELECT mailstreet FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 3);',
                               'SELECT mailstreet FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 4);'
                               ]

queries_more_col = ['SELECT mailstreet FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 1);',
                    'SELECT mailstreet, mailstrabr FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 1);',
                    'SELECT mailstreet, mailstrabr, mailcity FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 1);',
                    'SELECT mailstreet, mailstrabr, mailcity, mailzip FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 1);'
                    ]

queries_more_col_more_lim = ['SELECT mailstreet FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 1);',
                             'SELECT mailstreet, mailstrabr FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 2);',
                             'SELECT mailstreet, mailstrabr, mailcity FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 3);',
                             'SELECT mailstreet, mailstrabr, mailcity, mailzip FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 4);'
                            ]

queries_change_order = ['SELECT mailstreet FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" ASC LIMIT 1);',
                        'SELECT mailstreet FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" ASC LIMIT 2);',
                        'SELECT mailstreet FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" ASC LIMIT 3);',
                        'SELECT mailstreet FROM schools WHERE cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" ASC LIMIT 4);'
                        ]

queryes_other = ['SELECT MailStreet FROM schools WHERE CDSCode == 19648731936749',
                 'SELECT T2.mailstreet FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" ASC LIMIT 1);', # NONE
                 'SELECT T2.mailstreet FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.cdscode IN (SELECT cdscode FROM frpm ORDER BY "frpm count (k-12)" DESC LIMIT 1);', # MORE_COMPLEX
                 'SELECT T2.MailStreet FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode ORDER BY T1.`FRPM Count (K-12)` DESC LIMIT 2' # SAME
                 ]

res_list = []
for idx, queries in enumerate([queries_lim, queries_same_col_change_lim, queries_more_col, queries_more_col_more_lim, queries_change_order, queryes_other]):
    for internal, q in enumerate(queries):
        gold_table, gen_table, res_table, res_ves, sql_cos_sim, final_score = process_inputs(gold, q, 'california_schools')
        res_list.append({
            'idx': idx,
            'internal':internal,
            'sql_gold': gold,
            'sql_gen': q,
            'gold_table': str(gold_table),
            'gen_table': str(gen_table),
            'res_table': res_table,
            'res_ves': res_ves,
            'sql_cos_sim': sql_cos_sim,
            'final_score': final_score
        })
    
print('saving')    
save_path_test = '/mnt/data/gpinna/sql_metric/sql_metric/test/test_sql.json'

with open(save_path_test, 'w') as json_file:
    json.dump(res_list, json_file, indent=4)
    
print('END')

