from sql_embedder import SQLEmbeddingComparer

if __name__ == "__main__":
    sql1 = """SELECT employees.name, employees.department_name
                FROM employees
                """
    sql2 = """SELECT name, 
                  FROM cofee 
                """

    embedding_comparer = SQLEmbeddingComparer(trust_remote_code=True)
    
    similarity_score = embedding_comparer.compare_embeddings(sql1, sql2, compare_ast=False)
    print("Similarity Score :", similarity_score)
    
    # # If you want to compare raw SQL queries instead, you can specify compare_ast=False
    # similarity_score_sql = embedding_comparer.compare_embeddings(sql1, sql2, compare_ast=False)
    # print("Similarity Score (SQL):", similarity_score_sql)

