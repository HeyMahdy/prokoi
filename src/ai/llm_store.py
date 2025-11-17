from typing import Optional, Any

_llm: Optional[Any] = None


def set_llm(llm) -> None:
    global _llm
    _llm = llm


def get_llm():
    if _llm is None:
        raise RuntimeError("LLM not initialized yet; ensure FastAPI lifespan ran")
    return _llm

