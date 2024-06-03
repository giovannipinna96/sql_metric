from abc import ABC, abstractmethod
from typing import List
from databaseFacilitator import DatabaseManager
from math import sqrt

class Evaluator(ABC):    
    def __init__(self) -> None:
        print("Init Evaluator")
        ...
    @abstractmethod
    def evaluate(self, sql_gold: str, sql_predicted: str, db_manager: DatabaseManager) -> List[float] | float:
        ...

    
class sqlQueryEvaluator(Evaluator):
    def __init__(self) -> None:
        super().__init__()
        self.__name = "sql query evaluator"
        
    @property
    def name(self) -> str:
        return self.__name
    
    def evaluate(self, sql_gold: str, sql_predicted: str, db_manager: DatabaseManager) -> List[float] | float:
        pass
    
class tableEvaluator(Evaluator):
    def __init__(self) -> None:
        super().__init__()
        self.__name = "table evaluator"
        
    @property
    def name(self) -> str:
        return self.__name
    
    def evaluate(self, sql_gold: str, sql_predicted: str, db_manager: DatabaseManager) -> List[float] | float:
        result_query_execution_gold, execution_time_gold = db_manager.query_executor(sql_gold)
        result_query_execution_gen, execution_time_gen = db_manager.query_executor(sql_predicted)
        pass
    
    def table_evaluation(self, result_query_execution_gold, result_query_execution_gen) -> float:
        # ! mettere parte di De Lorenzo
        pass
    
    def is_equal(self, result_query_execution_gold, result_query_execution_gen) -> bool:
        # ! qui inserire come le tabelle sono uguali o no
        pass
    
    def ves_evaluation(self, result_query_execution_gold, result_query_execution_gen, execution_time_gold, execution_time_gen) -> float | int:
        if self.is_equal(result_query_execution_gold, result_query_execution_gen):
            return sqrt(execution_time_gold / execution_time_gen)
        else: 
            return 0
        
    def mean_ves_evaluation(self, result_query_execution_gold, result_query_execution_gen, execution_time_gold, execution_time_gen) -> float | int:
        print("VES evaluation...")
        if len(result_query_execution_gold) == len(result_query_execution_gen) == len(execution_time_gold) == len(execution_time_gen):
            sum = 0
            for i in range(len(execution_time_gold)):
                sum += self.ves_evaluation(result_query_execution_gold[i], result_query_execution_gen[i], execution_time_gold[i], execution_time_gen[i])
            return sum / len(execution_time_gold)
        else:
            raise ValueError("The lengths of the lists are not equal.")
        
    