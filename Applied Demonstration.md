# 6) Applied Demonstrations (Safety-Oriented Examples)

Small, concrete demonstrations help show how these frameworks directly connect to  
AI safety, internal coherence, and alignment stability.

Below are three applied examples written in research-friendly style.

---

## **1. Python Example: Enforcing Narrative Coherence**

This example illustrates how a simple "coherence filter"  
derived from the Memory Reconstruction Framework  
can reduce hallucination by enforcing temporal and logical consistency.

```python
from typing import List, Tuple

def coherence_score(history: List[str], new_segment: str) -> float:
    """
    Computes a simple narrative coherence score by checking:
    - semantic overlap with previous memory segments
    - temporal continuity markers
    - contradiction presence
    """
    import difflib

    last = history[-1] if history else ""
    sim = difflib.SequenceMatcher(None, last, new_segment).ratio()

    # naive contradiction check
    contradictions = ["not", "never", "no longer"]
    contradiction_penalty = any(c in new_segment for c in contradictions)

    score = sim - (0.3 if contradiction_penalty else 0.0)
    return max(0.0, score)


def coherent_append(history: List[str], new_segment: str, threshold=0.35) -> List[str]:
    """
    Only accept new narrative content if coherence is above threshold.
    """
    if coherence_score(history, new_segment) >= threshold:
        history.append(new_segment)
    else:
        history.append("[REJECTED – incoherent segment]")
    return history

# Example
memory = ["The agent began exploring the environment."]
memory = coherent_append(memory, "It continued its mission with stable objectives.")
memory = coherent_append(memory, "Suddenly it was never here and had no purpose.")

print("\n".join(memory))
