from abc import ABC, abstractmethod
from typing import List

class Evaluator(ABC):
    
    def __init__(self) -> None:
        print("Init Evaluator")
        ...
    @abstractmethod
    def evaluate(self, sqls: List[str] | str) -> List[float] | float:
        ...
        
class vesEvaluator(Evaluator):
    def __init__(self) -> None:
        super().__init__()
        self.__name = "ves evaluator"
        
    @property
    def name(self) -> str:
        return self.__name
    
    def evaluate(self, sqls: List[str] | str) -> List[float] | float:
        pass
    
class sqlQueryEvaluator(Evaluator):
    def __init__(self) -> None:
        super().__init__()
        self.__name = "sql query evaluator"
        
    @property
    def name(self) -> str:
        return self.__name
    
    def evaluate(self, sqls: List[str] | str) -> List[float] | float:
        pass
    
class tableEvaluator(Evaluator):
    def __init__(self) -> None:
        super().__init__()
        self.__name = "table evaluator"
        
    @property
    def name(self) -> str:
        return self.__name
    
    def evaluate(self, sqls: List[str] | str) -> List[float] | float:
        pass
    