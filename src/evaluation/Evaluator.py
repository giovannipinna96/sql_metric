import sys
sys.path.append("../src")

import re
import numpy as np
from itertools import permutations
import random
import Levenshtein
from abc import ABC, abstractmethod
from typing import List
from databasesFacilitator.databaseInterpreter import DatabaseManager
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
        self.__name = "table_evaluator"
        
    @property
    def name(self) -> str:
        return self.__name
    

    @staticmethod
    def replace_limit_with_10(main_string, new_limit: str = 'LIMIT 10'):
        """
        Check if a substring is exactly present within any string in a list of strings.
        Ensures that the substring is a whole word match.

        Parameters:
        substring (str): The substring to find.
        main_list (list of str): The list of strings to search within.

        Returns:
        bool: True if the substring is found as a whole word in any string in the list, False otherwise.
        """
        # Regular expression to match "limit" followed by a single digit
        pattern = re.compile(r'\blimit\s[0-9]\b')
        
        # Perform replacement in the main string
        replaced_string = pattern.sub(new_limit, main_string.lower())
        # print(replaced_string)
        return replaced_string
   
    @staticmethod
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
    
    @staticmethod
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
    

    def evaluate(self, sql_gold: str, sql_predicted: str, db_manager: DatabaseManager, max_extra_information_percentage=0.25) -> List[float] | float:
        if not sql_gold == sql_predicted:
            # print("Augmenting limit to 10")
            # sql_gold = self.replace_limit_with_10(sql_gold)
            # sql_predicted = self.replace_limit_with_10(sql_predicted)
            result_query_execution_gold, execution_time_gold = db_manager.query_executor(sql_gold)
            result_query_execution_gen, execution_time_gen = db_manager.query_executor(sql_predicted)
            print(result_query_execution_gen.shape)
            if result_query_execution_gen.shape[0] < 150000:
                if self.is_exact_substring('ORDER BY', self.delete_inside_parentheses(sql_gold.upper())):# or self.is_exact_substring('ORDER BY', sql_predicted.upper()):
                    print("order")
                    res_order_table = self.order_table_evaluation(result_query_execution_gold=result_query_execution_gold, result_query_execution_gen=result_query_execution_gen, max_extra_information_percentage=max_extra_information_percentage)
                else:
                    res_table = self.table_evaluation(result_query_execution_gold=result_query_execution_gold, result_query_execution_gen=result_query_execution_gen)
                res_ves = self.ves_evaluation(result_query_execution_gold=result_query_execution_gold, result_query_execution_gen=result_query_execution_gen, execution_time_gold=execution_time_gold, execution_time_gen=execution_time_gen)
                # res_levenshtein_distance = self.levenshtein_distance_between_two_sql_stings(sql_gold_string=db_manager.data_query.keywords, sql_predicted_string=sql_predicted)
            else:
                print("Too rows"*3)
                return None, None, 0, 0
        else:
            print("The gold and predicted sql are equal.")
            return None, None, 1, 1
           
        if self.is_exact_substring('ORDER BY', self.delete_inside_parentheses(sql_gold.upper())):# or self.is_exact_substring('ORDER BY', sql_predicted.upper()):
            return result_query_execution_gold, result_query_execution_gen, res_order_table, res_ves
        else:
            # print("no order by"*30)
            return result_query_execution_gold, result_query_execution_gen, res_table, res_ves
    
    @staticmethod
    def _edit_distance(list1, list2):
        len_list1 = len(list1)
        len_list2 = len(list2)
        dp = [[0 for _ in range(len_list2 + 1)] for _ in range(len_list1 + 1)]

        for i in range(len_list1 + 1):
            for j in range(len_list2 + 1):
                if i == 0:
                    dp[i][j] = j

                elif j == 0:
                    dp[i][j] = i

                elif list1[i - 1] == list2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]

                else:
                    dp[i][j] = 1 + min(dp[i - 1][j],  # Remove
                                    dp[i][j - 1],  # Insert
                                    dp[i - 1][j - 1])  # Replace
        return dp[len_list1][len_list2]
    

    def calculate_order_score(list1, list2):
        # Calculate the length of both lists
        len1, len2 = len(list1), len(list2)
        
        # If both lists are empty, they are trivially the same
        if len1 == 0 and len2 == 0:
            return 1.0
        
        # If one of the lists is empty, treat it as a shift by the length of the other list
        if len1 == 0 or len2 == 0:
            return 0.0

        # Determine the maximum possible shift
        max_shift = max(len1, len2)
        
        # If the lists are exactly the same
        if list1 == list2:
            return 1.0
        
        # Calculate shift score
        def shift_score(shift):
            return 1 - (shift / max_shift)
        
        # Calculate the minimum shift required to align the lists
        min_shift = max_shift  # Initialize to max possible shift
        
         # Compare every possible shift for both lists
        for shift in range(max_shift):
            # Shift list1 to the right by 'shift' positions
            shifted_list1 = list1[-shift:] + list1[:-shift] if shift < len1 else [''] * (shift - len1) + list1
            # Shift list2 to the right by 'shift' positions
            shifted_list2 = list2[-shift:] + list2[:-shift] if shift < len2 else [''] * (shift - len2) + list2
            
            # Check if the shifted versions match the original lists
            if shifted_list1[:len2] == list2 or shifted_list2[:len1] == list1:
                min_shift = shift
                break
        
        # Calculate the score based on the minimum shift
        score = shift_score(min_shift)
        return score
    
    def _build_cross_edit_distance_matrix(self, lists1, lists2):
        rows = len(lists1)
        cols = len(lists2)
        m = max(len(lists1[0]), len(lists2[0]))
        d = max(rows, cols)
        matrix = [[m for _ in range(d)] for _ in range(d)]

        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = self._edit_distance(lists1[i], lists2[j])

        return matrix

            
    def table_evaluation(self, result_query_execution_gold, result_query_execution_gen) -> float | None:
        # print(result_query_execution_gold)
        # print(result_query_execution_gen)
        # print("Table Evaluation...")
        list_result_query_execution_gold = list(result_query_execution_gold.to_dict(orient='list').values())
        list_result_query_execution_gen = list(result_query_execution_gen.to_dict(orient='list').values())
        edit_distance_matirx = self._build_cross_edit_distance_matrix(list_result_query_execution_gold,
                                                      list_result_query_execution_gen)
        
        # ! non so quante righe e colonne sono presenti nella gold query dalla generated query
        
        e = 0
        # for i in range(len(edit_distance_matirx)):
            # print(edit_distance_matirx[i])
        for i in range(len(edit_distance_matirx)):
            e += min(edit_distance_matirx[i])/max(len(list_result_query_execution_gold[0]), len(list_result_query_execution_gen[0]))
        # print(1 - (e/len(edit_distance_matirx)))
        return 1 - (e/len(edit_distance_matirx))
    
    @staticmethod
    def levenshtein_distance_between_two_sql_stings(sql_gold_string, sql_predicted_string):
        """
        Calculate the Levenshtein distance between two strings using the python-Levenshtein library.

        Parameters:
        str1 (str): The first string.
        str2 (str): The second string.

        Returns:
        int: The Levenshtein distance between the two strings.
        """
        # print("Levenshtein distance...")
        # print(Levenshtein.distance(sql_gold_string, sql_predicted_string))
        return Levenshtein.distance(sql_gold_string, sql_predicted_string)
    
        
    def ves_evaluation(self, result_query_execution_gold, result_query_execution_gen, execution_time_gold, execution_time_gen) -> float | int:
        # if self.is_equal(result_query_execution_gold, result_query_execution_gen):
        # print("VES evaluation...")
        # print(sqrt(execution_time_gold / execution_time_gen)) # TODO sometime is over 1. Proportional to the data retrived?
        return sqrt(execution_time_gold / execution_time_gen) # TODO check if is correct
        # else: 
            # return 0
        
    def mean_ves_evaluation(self, result_query_execution_gold, result_query_execution_gen, execution_time_gold, execution_time_gen) -> float | int:
        # print("VES evaluation...")
        if len(result_query_execution_gold) == len(result_query_execution_gen) == len(execution_time_gold) == len(execution_time_gen):
            sum = 0
            for i in range(len(execution_time_gold)):
                sum += self.ves_evaluation(result_query_execution_gold[i], result_query_execution_gen[i], execution_time_gold[i], execution_time_gen[i]) # TODO check if is correct
            return sum / len(execution_time_gold)
        else:
            raise ValueError("The lengths of the lists are not equal.")
        
    @staticmethod
    def find_most_similar_indices(matrix1, matrix2):
        num_rows1 = len(matrix1)
        num_rows2 = len(matrix2)
        
        if num_rows1 == 0 or num_rows2 == 0:
            return []
        
        results = []
        
        for row1 in matrix1:
            max_similarity = -1
            most_similar_index = -1
            
            for i in range(num_rows2):
                row2 = matrix2[i]
                
                # Calculate similarity
                similarity = sum(1 for x, y in zip(row1, row2) if x == y)
                
                # Update most similar index if found a better match
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_index = i
            
            results.append(most_similar_index)
        
        return results
    
    @staticmethod
    def riordina_per_indici(lista, indici):
        if len(lista) != len(indici):
            raise ValueError("Le liste devono avere la stessa lunghezza")
        # Creiamo una lista temporanea di tuple (indice, elemento)
        temp = [(indici[i], lista[i]) for i in range(len(lista))]
        # Ordiniamo la lista temporanea secondo gli indici
        temp.sort(key=lambda x: x[0])
        # Estraiamo gli elementi ordinati dalla lista temporanea
        lista_ordinata = [elemento for indice, elemento in temp]
        return lista_ordinata
    
    @staticmethod
    def lcs(X, Y):
        # Find the length of the strings
        m = len(X)
        n = len(Y)
        
        # Create a table to store lengths of longest common suffixes of substrings.
        # Note that LCSuff[i][j] contains length of longest common suffix of
        # X[0...i-1] and Y[0...j-1]. The first row and first column entries have no
        # logical meaning, they are used only for simplicity of program
        LCSuff = [[0 for k in range(n+1)] for l in range(m+1)]
        
        # To store length of the longest common substring
        result = 0
        
        # Building the LCSuff table in bottom-up fashion
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    LCSuff[i][j] = 0
                elif X[i-1] == Y[j-1]:
                    LCSuff[i][j] = LCSuff[i-1][j-1] + 1
                    result = max(result, LCSuff[i][j])
                else:
                    LCSuff[i][j] = 0
        return result
    
    # def longest_common_subpattern(self, list1, list2):
    #     max_length = 0
    #     for sublist1, sublist2 in zip(list1, list2):
    #         length = self.lcs(sublist1, sublist2)
    #         if length > max_length:
    #             max_length = length
    #     print("maxlen")
    #     print(type(max_length))
    #     return max_length
    # @staticmethod
    # def count_non_empty_sublists(lst):
    #     return sum(1 for sublist in lst if sublist)
    
    # def longest_common_subpattern(self, list1, list2):
    #     results = []
        
    #     # Iterate over the longer list
    #     for i in range(max(len(list1), len(list2))):
    #         if i < len(list1) and i < len(list2):
    #             sublist1 = list1[i]
    #             sublist2 = list2[i]
    #         elif i < len(list1):
    #             sublist1 = list1[i]
    #             sublist2 = []
    #         else:
    #             sublist1 = []
    #             sublist2 = list2[i]
            
    #         biggest_subpattern = []
    #         n, m = len(sublist1), len(sublist2)
            
    #         for x in range(n):
    #             for y in range(m):
    #                 current_subpattern = []
    #                 k = 0
    #                 while x + k < n and y + k < m and sublist1[x + k] == sublist2[y + k]:
    #                     current_subpattern.append(sublist1[x + k])
    #                     k += 1
                    
    #                 if len(current_subpattern) > len(biggest_subpattern):
    #                     biggest_subpattern = current_subpattern

    #         results.append(biggest_subpattern)
            
    #         #print("7"*30)
    #         #print(results)
    #         #print("7"*30)

    #     return self.count_non_empty_sublists(results)
    
    def longest_common_subpattern(self, list1, list2):
        def compare_sublists(sublist1, sublist2):
            return all(item1 == item2 for item1, item2 in zip(sublist1, sublist2))

        max_subpattern = 0
        for i in range(len(list1)):
            for j in range(len(list2)):
                current_subpattern = 0
                k, l = i, j
                while k < len(list1) and l < len(list2):
                    if compare_sublists(list1[k], list2[l]):
                        current_subpattern += 1
                        k += 1
                        l += 1
                    else:
                        break
                max_subpattern = max(max_subpattern, current_subpattern)

        return max_subpattern
    
    
    def longest_common_subpattern_strict(self, list1, list2):
        def compare_sublists(sublist1, sublist2):
            return all(item1 == item2 for item1, item2 in zip(sublist1, sublist2))

        max_subpattern = 0
        for shift in range(min(len(list1), len(list2))):
            current_subpattern = 0
            i = j = shift
            while i < len(list1) and j < len(list2):
                if compare_sublists(list1[i], list2[j]):
                    current_subpattern += 1
                    i += 1
                    j += 1
                else:
                    break
            max_subpattern = max(max_subpattern, current_subpattern)

        return max_subpattern
    
    @staticmethod
    def transpose_matrix(matrix):
        # Use zip(*matrix) to transpose the matrix
        transposed = list(map(list, zip(*matrix)))
        return transposed
    
    @staticmethod
    def calculate_score(gold_rows, generated_rows, max_matching_gold_rows):
        # print("a")
        # print(gold_rows)
        # print("b")
        # print(generated_rows)
        # print("c")
        # print(max_matching_gold_rows)
        # print("="*30)
        # if generated_rows == gold_rows == max_matching_gold_rows:
        #     print("si entra qua")
        #     return 1.0
        # missing_rows_penalty = (gold_rows - max_matching_gold_rows) / gold_rows # da correggere
        if max_matching_gold_rows == 0:
            score = 0
        elif generated_rows < gold_rows:
            missing_rows_penalty = (gold_rows - max_matching_gold_rows) / gold_rows
            score = 1.0 - missing_rows_penalty
        else:
            missing_rows_penalty = (generated_rows - max_matching_gold_rows) / gold_rows # ! ma è giusto diviso per gold_rows?
            score = 1.0 - (missing_rows_penalty / 1.5)
        
        print(f'max_match {max_matching_gold_rows}')
        print(f"the raw socre {score}")
        return score

# # Example usage:
# gold_rows = 100
# generated_rows = 90
# max_matching_gold_rows = 85

# score = calculate_score(gold_rows, generated_rows, max_matching_gold_rows)
# print(f"Score: {score}")

   
    def order_table_evaluation(self, result_query_execution_gold, result_query_execution_gen, ranges = None, random: bool = True, number_of_pairs: int = 10, max_extra_information_percentage=0.25) -> float | None:
        # ! i due risultati non sono invertibili se inverto sql_gold & generated viene diverso come è possibile?
        list_result_query_execution_gold = list(result_query_execution_gold.to_dict(orient='list').values())
        list_result_query_execution_gen = list(result_query_execution_gen.to_dict(orient='list').values())
        
        # print(list_result_query_execution_gold)
        # print("="*30)
        # print(list_result_query_execution_gen)
        # print("="*30)
        
        best_permutation = self.find_most_similar_indices(list_result_query_execution_gold, list_result_query_execution_gen)
        reorderedlist_result_query_execution_gold = self.riordina_per_indici(list_result_query_execution_gold, best_permutation)
        transpost_list_result_query_execution_gold = self.transpose_matrix(reorderedlist_result_query_execution_gold)
        transpost_list_result_query_execution_gen = self.transpose_matrix(list_result_query_execution_gen)
        # print(transpost_list_result_query_execution_gold)
        # print("="*30)
        # print(transpost_list_result_query_execution_gen)
        # print("="*30)
        # print("<"*30)
        # print(transpost_list_result_query_execution_gold)
        # print("<"*30)
        # print(transpost_list_result_query_execution_gen)
        
        # print(type(transpost_list_result_query_execution_gold))
        # print(type(transpost_list_result_query_execution_gold[0]))
        # print(len(transpost_list_result_query_execution_gold))
        # print(len(transpost_list_result_query_execution_gold[0]))
        
        # print("<a"*30)
        # print(self.longest_common_subpattern(transpost_list_result_query_execution_gold, transpost_list_result_query_execution_gen))
        # print("<a"*30)
        if round(len(transpost_list_result_query_execution_gold[0]) * (1 + max_extra_information_percentage)) > len(transpost_list_result_query_execution_gen[0]) or round(len(transpost_list_result_query_execution_gold) * (1 + max_extra_information_percentage)) > len(transpost_list_result_query_execution_gen): 
            # score = self.longest_common_subpattern(transpost_list_result_query_execution_gold, transpost_list_result_query_execution_gen) / len(transpost_list_result_query_execution_gold[0])
            row_score = self.calculate_score(len(transpost_list_result_query_execution_gold), len(transpost_list_result_query_execution_gen), self.longest_common_subpattern(transpost_list_result_query_execution_gold, transpost_list_result_query_execution_gen)) # !  self.longest_common_subpattern(transpost_list_result_query_execution_gold[0], transpost_list_result_query_execution_gen[0]) non solo per uno ma per tutti
            column_score = self.calculate_score(len(transpost_list_result_query_execution_gold[0]), len(transpost_list_result_query_execution_gen[0]), len(best_permutation))
            if row_score == 0 or column_score == 0:
                score = 0
            else:
                if len(transpost_list_result_query_execution_gold[0]) > len(transpost_list_result_query_execution_gen[0]) or len(transpost_list_result_query_execution_gold) > len(transpost_list_result_query_execution_gen):
                    score = (row_score * 0.4 + column_score * 0.6) * 0.8
                else:
                    score = (row_score * 0.4 + column_score * 0.6)
        else:
            score = 0
        try:
            print(f"socre for ordered table: {score}, row_score {row_score}, column_score {column_score}")
        except:
            print(f"score {score}")
        return score
        