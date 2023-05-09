
from .semantic_sim import calculate_score
def semantic_compute(query, documents, glove):
    try:
        scores = calculate_score(query, documents, glove)
        return scores
    except Exception:
        print("ERROR")
        return []