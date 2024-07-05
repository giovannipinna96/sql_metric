from pglast import parse_sql
from sentence_transformers import SentenceTransformer, util
import pprint

class SQLASTComparer:
    def __init__(self, sql_query1: str, sql_query2: str):
        """
        Initialize with two SQL queries to compare.
        """
        self.sql_query1 = sql_query1
        self.sql_query2 = sql_query2
        self.ast1 = self._parse_sql_to_ast(self.sql_query1)
        self.ast2 = self._parse_sql_to_ast(self.sql_query2)

    def _parse_sql_to_ast(self, sql_query: str):
        """
        Parses an SQL query into an AST.
        """
        try:
            return parse_sql(sql_query)[0].stmt
        except Exception as e:
            raise ValueError(f"The query {sql_query} is WRONG, please review the query. Error: {e}")

    def get_ast(self):
        """
        get ASTs as strings
        """
        
        pp = pprint.PrettyPrinter()
        ast = {
            'AST1': pp.pformat(self.ast1(skip_none=True)),
            'AST2': pp.pformat(self.ast2(skip_none=True))
        }
        return ast
