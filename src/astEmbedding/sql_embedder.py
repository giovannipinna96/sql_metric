from sentence_transformers import SentenceTransformer, util

class SQLEmbeddingComparer:
    def __init__(self, model_name: str = "sentence-transformers/msmarco-bert-base-dot-v5"):  #<----CAN define a different model here
        """
        initialize the embedding model
        """
        self.model = SentenceTransformer(model_name)

    def compare_embeddings(self, sql_stmt1: str, sql_stmt2: str):
        """
        cosine similarity of embeddings for two SQL queries.
        """
        query_emb = self.model.encode(sql_stmt1)
        doc_emb = self.model.encode(sql_stmt2)
        return util.cos_sim(query_emb, doc_emb)[0].cpu().tolist()
