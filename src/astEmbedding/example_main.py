from ast_algo import SQLASTComparer
from sql_embedder import SQLEmbeddingComparer

if __name__ == "__main__":
    sql1 = """SELECT employees.name, departments.department_name
                FROM employees
                INNER JOIN departments ON employees.department_id = departments.department_id
                WHERE departments.department_name = 'Sales';"""
    sql2 = """SELECT name
                  FROM departments 
                  WHERE departments.department_id = employees.department_id 
                    AND department_name = 'Sales') AS department_name
              FROM employees
              WHERE department_id = (SELECT department_id 
                                     FROM departments 
                                     WHERE department_name = 'Sales');"""

    ast_comparer = SQLASTComparer(sql1, sql2)
    asts = ast_comparer.get_ast()
    print("ASTs:", asts)

    embedding_comparer = SQLEmbeddingComparer()
    similarity_score = embedding_comparer.compare_embeddings(sql1, sql2)
    print("Similarity Score:", similarity_score)
