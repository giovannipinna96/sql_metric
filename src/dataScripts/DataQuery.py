from dataclasses import dataclass, field
from typing import List, Tuple, Union, Dict, Optional
import pandas as pd
import re
from dataScripts import SQL_KEYWORDS, ALL_DB
import os
import json


@dataclass(frozen=True, kw_only=True)
class DataQuery:
    path: Optional[str] = None
    question_id: Optional[int] = None
    db_id: str
    question: str
    evidence: Optional[str]
    SQL: str
    difficulty: Optional[str]
    bird_split: str = "dev"
    is_gold: bool = True
    _key_words: List[str] = field(init=False)
    
    def __post_init__(self):
        object.__setattr__(self, '_key_words', self._extract_sql_keywords(self.SQL)) # Use the same thing the generated __init__ method does: object.__setattr__.
        
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
    path: str
    table_names_original: List[str]
    table_names: List[str]
    column_names_original: List[Tuple[int, str]]
    column_names: List[Tuple[int, str]]
    column_types: List[str]
    primary_keys: List[int] | List[Union[int, List[int]]]
    foreign_keys: List[int] | List[Union[int, List[int]]]
    
    
    
@dataclass
class DataManager:
    db_name: str
    path: str
    data_query: List[DataQuery] = field(init=False)
    data_table: List[DataTable] = field(init=False)
    tables_info: List[Dict[str, pd.DataFrame]] = field(init=False)
    
    @staticmethod
    def read_csv_files_to_dict(folder_path):
    # Create an empty dictionary to store file name and dataframe pairs
        csv_dict = {}
        
        # List all files in the folder
        for file_name in os.listdir(folder_path):
            # Check if the file is a CSV file
            if file_name.endswith('.csv'):
                # Construct the full file path
                file_path = os.path.join(folder_path, file_name)
                # Read the CSV file into a dataframe
                df = pd.read_csv(file_path)
                # Store the dataframe in the dictionary with the file name as the key (without the .csv extension)
                csv_dict[file_name.replace('.csv', '')] = df
                
        return csv_dict
    
    def __post_init__(self):
        if self.db_name.lower() not in [n_db.lower() for n_db in ALL_DB.keys()] + [n_db.lower() for n_db in ALL_DB.values()]:
            raise AttributeError(
                f'Cannot recognize llm {self.db_name}. It is not in the dictionary of known DBs, which are: {str(ALL_DB.keys())}.')
        else:
            try:
                self.db_name = ALL_DB[self.db_name.lower()]
            except:
                pass # because the name is already correct and consistent with the name of the database
        self.data_query_path = os.path.join(self.path, "dev.json")
        self.data_table_path = os.path.join(self.path, "dev_tables.json")
        
        with open(self.data_query_path, 'r') as f:
            self.data_query = [DataQuery(**q, path=self.data_query_path) for q in json.load(f) if q['db_id'] == self.db_name]
        
        with open(self.data_table_path, 'r') as f:
            self.data_table = [DataTable(**q, path=self.data_table_path) for q in json.load(f) if q['db_id'] == self.db_name]
            
        self.tables_info = DataManager.read_csv_files_to_dict(os.path.join(self.path, "dev_databases", self.db_name, "database_description"))
    
