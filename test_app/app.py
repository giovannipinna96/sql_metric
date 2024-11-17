import sys
sys.path.append('../src')

import gradio as gr
from collections import Counter
import re

from evaluation.Evaluator import tableEvaluator
from databasesFacilitator.databaseInterpreter import DatabaseInterpreterPandas

from astEmbedding.sql_embedder import SQLEmbeddingComparer

SQL_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE",
    "CREATE", "TABLE", "ALTER", "ADD", "DROP", "TRUNCATE", "JOIN", "INNER", "LEFT",
    "RIGHT", "FULL", "OUTER", "GROUP", "BY", "ORDER", "HAVING", "UNION", "DISTINCT",
    "LIMIT", "OFFSET"
] 


def sql_similarity_score(sql1: str, sql2: str, compare_ast: bool = False):
    if sql1 == sql2:
        return [1.0]
    else:
        embedding_comparer = SQLEmbeddingComparer(trust_remote_code=True)
        similarity_score = embedding_comparer.compare_embeddings(sql1, sql2, compare_ast)
        return similarity_score

# def elementi_comuni_con_duplicati(lista1, lista2):
#         # Creiamo un Counter per ciascuna lista
#         counter1 = Counter(lista1)
#         counter2 = Counter(lista2)
#         # Troviamo l'intersezione dei due Counter
#         comuni = counter1 & counter2
#         # Calcoliamo il numero totale di elementi in comune, considerando i duplicati
#         num_comuni = sum(comuni.values())
        
#         return num_comuni / max(len(lista1), len(lista2))

# def extract_sql_keywords(SQL: str): # ! here yuriy AST code
#         # Convert the query to uppercase to match keywords case-insensitively
#         sql_query_upper = SQL.upper()
    
#         # Use a set to store found keywords to avoid duplicates
#         found_keywords = set()
    
#         # Loop through the list of SQL keywords and check if they are present in the query
#         for keyword in SQL_KEYWORDS:
#             # Use regular expression to find whole words only
#             if re.search(r'\b' + keyword + r'\b', sql_query_upper):
#                 found_keywords.add(keyword)
#         print(found_keywords)
#         return list(found_keywords)
    

# Funzione che elabora gli input e produce sei output
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

ALL_DB = ["california_schools", "card_games", "codebase_community", "debit_card_specializing", "european_football_2", "financial", "formula_1",
     "student_club", "superhero", "thrombosis_prediction", "toxicology"]
# ALL_DB: dict[str, str] = {
#     'california schools': "california_schools",
#     'card games': "card_games",
#     'codebase community': "codebase_community",
#     'debit card specializing': "debit_card_specializing",
#     'european football': "european_football_2",
#     'financial': "financial",
#     'formula 1': "formuala_1",
#     'student club': "student_club",
#     'superhero': "superhero",
#     'thrombosis prediction': "thrombosis_prediction",
#     'toxicology': "toxicology",     
# }

# Creazione dell'interfaccia Gradio
with gr.Blocks() as demo:
    gr.Markdown("## SQL evaluation a new metric")
    
    with gr.Row():
        sql_gold = gr.Textbox(label="SQL Gold")
        sql_gen = gr.Textbox(label="SQL Gen")
    
    dropdown = gr.Dropdown(choices=ALL_DB, label="Select database")
    button = gr.Button("Evaluate")
    
    with gr.Row():
        tss = gr.Textbox(label="Table Similarity Score")
        # tss2 = gr.Textbox(label="Table Similarity Score decompose")
        ves = gr.Textbox(label="VES")
        common_keywords = gr.Textbox(label="SQL similarity")
        final_score = gr.Textbox(label="Final score (no ves cosidered)")
        
    gr.Markdown("###")  # add a spqce
    
    with gr.Row():
        gold_table = gr.DataFrame(label="Gold Table")
        gen_table = gr.DataFrame(label="Gen Table")
        
    
    button.click(process_inputs, inputs=[sql_gold, sql_gen, dropdown], outputs=[gold_table, gen_table, tss, ves, common_keywords, final_score])

# Esegui l'app
demo.launch(share = True, debug = True)
