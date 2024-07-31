import sys
sys.path.append("../src")

from sentence_transformers import SentenceTransformer, util
from astEmbedding.ast_algo import SQLASTComparer

########## EMBEDDING MODELS FOR CODE : 
# 1. "WhereIsAI/UAE-Code-Large-V1"
# 2 "jinaai/jina-embeddings-v2-base-code"
# 3. "flax-sentence-embeddings/st-codesearch-distilroberta-base"
# 4. "SQAI/streetlight_sql_embedding2"
# 5. "SQAI/streetlight_sql_embedding3"


######### EMBEDDING MODELS FOR TEXT : 
# 1. "nomic-ai/nomic-embed-text-v1"


class SQLEmbeddingComparer:
    def __init__(self, model_name: str = "sergeyvi4ev/all-MiniLM-RAGSQL-code", trust_remote_code:bool= True):  #<----CAN define a different model here
        """
        initialize the embedding model
        """
        

        self.model = SentenceTransformer(model_name, trust_remote_code=trust_remote_code)

    def compare_embeddings(self, sql_stmt1: str, sql_stmt2: str, compare_ast: bool = True):
        """
        Cosine similarity of embeddings for two SQL queries or their ASTs.
        
        Parameters:
        - sql_stmt1: First SQL statement
        - sql_stmt2: Second SQL statement
        - compare_ast: Boolean to determine whether to compare ASTs instead of raw SQL queries
        """
        if compare_ast:
            # Parse SQL statements to ASTs
            try:
                # Parse SQL statements to ASTs
                ast_comparer = SQLASTComparer(sql_stmt1, sql_stmt2)
                asts = ast_comparer.get_ast()
                input1 = asts['AST1']
                input2 = asts['AST2']
            except ValueError as e:
                print("Query similairty is 0 because of the error")
                return 0  
        else:
            # Use raw SQL statements
            input1 = sql_stmt1
            input2 = sql_stmt2

        # Encode and compare embeddings
        query_emb = self.model.encode(input1)
        doc_emb = self.model.encode(input2)
        return util.cos_sim(query_emb, doc_emb)[0].cpu().tolist()
