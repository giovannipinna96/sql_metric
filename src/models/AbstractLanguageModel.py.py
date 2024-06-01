from abc import ABC, abstractmethod
from typing import Any
from models import ALL_LLMs


class AbstractLanguageModel(ABC):
    def __init__(self, model_name: str) -> None:
        super().__init__()
        self.__NAME = model_name.strip()

        allowed_models: list[str] = [key for key in ALL_LLMs if ALL_LLMs[key][0] == self.__class__.__name__]

        if self.name.lower() not in [n_model.lower() for n_model in allowed_models]:
            raise AttributeError(
                f'Cannot recognize llm {self.name} for category {self.__class__.__name__}. It is not in the dictionary of known llms, which are: {str(allowed_models)}.')

        self.__llm_class: str = ALL_LLMs[self.name][0]
        self.__llm_id: str = ALL_LLMs[self.name][1]
        self.__llm_role: str = ALL_LLMs[self.name][2]
        self._load_model()

    def llm_class(self) -> str:
        return self.__llm_class

    def llm_id(self) -> str:
        return self.__llm_id
    
    def llm_role(self) -> str:
        return self.__llm_role

    @abstractmethod
    def ask(self, prompts: list[str]) -> str:
        pass

    @property
    def name(self) -> str:
        return self.__NAME

    @abstractmethod
    def _load_model(self) -> Any:
        print("Loading model...")
        pass