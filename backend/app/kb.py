import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _tokenize(text: str) -> set[str]:
    text = text.lower()
    zh_chars = re.findall(r"[\u4e00-\u9fff]", text)
    words = re.findall(r"[a-zA-Z0-9_]+", text)
    bigrams = [text[i:i+2] for i in range(max(0, len(text)-1)) if re.match(r"[\u4e00-\u9fff]{2}", text[i:i+2])]
    return set(zh_chars + words + bigrams)

class KnowledgeBase:
    def __init__(self) -> None:
        self.docs = json.loads((DATA_DIR / "kb.json").read_text(encoding="utf-8"))

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        q_tokens = _tokenize(query)
        scored = []
        for doc in self.docs:
            haystack = f"{doc['title']} {doc['content']}"
            score = len(q_tokens & _tokenize(haystack))
            if score > 0:
                scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:top_k]]

kb = KnowledgeBase()
