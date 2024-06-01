from typing import Any
from models.AbstractLanguageModel import AbstractLanguageModel
from sentence_transformers import SentenceTransformer
import os
import torch

class ColumnsSimilarityModel(AbstractLanguageModel):
    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)

    def _load_model(self) -> Any:
        super()._load_model()
        model_id = self.llm_id()
        
        self.__model = SentenceTransformer(model_id, device_map = 'auto')

    def ask(self, prompts: list[str]) -> str: # ! we don't want this type
        torch.cuda.empty_cache()
        embeddings = self.__model.encode(prompts)
        
        return embeddings
