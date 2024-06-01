from dataclasses import dataclass
from typing import List, Tuple, Union

import re
from dataScripts import SQL_KEYWORDS


@dataclass(frozen=True, kw_only=True)
class DataQuery:
    question_id: int
    db_id: str
    question: str
    evidence: str
    SQL: str
    difficulty: str
    bird_split: str
    is_gold: bool
    _key_words: List[str]
    
    def __post_init__(self):
        self._key_words = self._extract_sql_keywords(self.SQL)
        
    @staticmethod
    def _extract_sql_keywords(SQL: str): # ! here yuriy AST code
        # Convert the query to uppercase to match keywords case-insensitively
        sql_query_upper = SQL.upper()
    
        # Use a set to store found keywords to avoid duplicates
        found_keywords = set()
    
        # Loop through the list of SQL keywords and check if they are present in the query
        for keyword in SQL_KEYWORDS:
            # Use regular expression to find whole words only
            if re.search(r'\b' + keyword + r'\b', sql_query_upper):
                found_keywords.add(keyword)
    
        return list(found_keywords)
    
    @property
    def key_words(self) -> List[str]:
        return self._key_words
        
    
@dataclass(frozen=True, kw_only=True)
class DataTable:
    db_id: str
    table_names_original: List[str]
    table_names: List[str]
    column_names_original: List[Tuple[int, str]]
    column_names: List[Tuple[int, str]]
    column_types: List[str]
    primary_keys: List[int] | List[Union[int, List[int]]]
    foreign_keys: List[int] | List[Union[int, List[int]]]
    