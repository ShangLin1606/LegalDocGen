from pathlib import Path
from typing import List
import glob
def simple_keyword_retrieval(query: str, corpus_dir: str, top_k: int = 3) -> List[str]:
    files = glob.glob(str(Path(corpus_dir) / "*.txt"))
    scored = []
    q = set(query.split())
    for f in files:
        text = Path(f).read_text(encoding="utf-8", errors="ignore")
        score = sum(1 for w in q if w in text)
        scored.append((score, f, text))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [t for _, _, t in scored[:top_k]]
