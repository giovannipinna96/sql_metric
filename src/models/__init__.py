ALL_LLMs: dict[str, tuple[str, str]] = {
    'MiniLM': ('HuggingFaceLLM', 'sentence-transformers/paraphrase-MiniLM-L6-v2', 'embeddings'),
    'ALLMiniLM': ('HuggingFaceLLM', 'sentence-transformers/all-MiniLM-L6-v2', 'embeddings')
}

models_list = sorted([key for key in ALL_LLMs])
all_llms_macro_categories = sorted(list(set([ALL_LLMs[key][0] for key in ALL_LLMs])))