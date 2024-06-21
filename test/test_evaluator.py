import sys
sys.path.append('../src')

from evaluation.Evaluator import tableEvaluator
from databasesFacilitator.databaseInterpreter import DatabaseInterpreterPandas


if "__main__" == __name__:
    print("Test Table Evaluator")
    tab_eval = tableEvaluator()
    print(tab_eval.name)
    interpreter = DatabaseInterpreterPandas("california_schools", '/mnt/data/gpinna/lisbona_sql_metric/sql_metric/data/raw_data/dev')
    interpreter.load_database()
    print("="*30)
    print("Evaluating table")
    tab_eval.evaluate("SELECT City, Street FROM schools Order BY City DESC LIMIT 6",
                      # "SELECT City, Street FROM (SELECT City, Street FROM schools LIMIT 6) ORDER BY City DESC;",
                      "SELECT Street as T, City FROM schools Order BY City DESC LIMIT 6",
                      interpreter)
    print("="*30)
    
    print("End Test Table Evaluator")
    