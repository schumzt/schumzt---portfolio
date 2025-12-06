"""
memory_stack_simulation.py

Toy implementation of the Layered Memory Stack /
Dynamic Memory Framework.

This example is NOT a full cognitive model. Its purpose is to:
- represent sensory, episodic, and semantic layers,
- show how an input event is encoded across layers with different
  stability / abstraction,
- demonstrate reconstruction of a "remembered" event from layered traces.
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class MemoryTrace:
    """Simple memory trace with content and stability weight."""
    content: str
    strength: float  # 0.0 ~ 1.0


class LayeredMemoryStack:
    def __init__(self):
        # Very small toy buffers
        self.sensory: List[MemoryTrace] = []
        self.episodic: List[MemoryTrace] = []
        self.semantic: Dict[str, MemoryTrace] = {}

    def encode_event(self, raw_event: str) -> None:
        """
        Encode a raw event into all three layers.

        In a full model, "parsing" & "abstraction" would be learned.
        Here we just use simple string operations as a proxy.
        """
        # Sensory: almost raw, high detail, low stability
        self.sensory.append(MemoryTrace(content=raw_event, strength=0.3))

        # Episodic: add a minimal timestamp-like tag
        episodic_repr = f"EPISODE: {raw_event}"
        self.episodic.append(MemoryTrace(content=episodic_repr, strength=0.6))

        # Semantic: extract a very crude "topic" as a stable key
        topic = raw_event.split()[0].lower()  # toy: first token as topic
        if topic not in self.semantic:
            self.semantic[topic] = MemoryTrace(content=f"TOPIC: {topic}",
                                               strength=0.9)

    def decay(self, sensory_decay: float = 0.2, episodic_decay: float = 0.05) -> None:
        """Apply a very simple decay rule to show differential stability."""
        for trace in self.sensory:
            trace.strength = max(0.0, trace.strength - sensory_decay)
        for trace in self.episodic:
            trace.strength = max(0.0, trace.strength - episodic_decay)
        # semantic layer is assumed relatively stable in this toy, so no decay

    def reconstruct(self, event_index: int) -> str:
        """
        Reconstruct a remembered event by combining
        (sensory, episodic, semantic) traces.

        In the full theory this corresponds to reconstructive memory;
        here we just concatenate weighted pieces.
        """
        if event_index >= len(self.episodic):
            raise IndexError("No such episodic trace")

        epi = self.episodic[event_index]
        # try to find a matching semantic topic
        topic = epi.content.split()[1].lower()  # second token after 'EPISODE:'
        sem = self.semantic.get(topic, None)

        parts = []
        parts.append(f"[episodic@{epi.strength:.2f}] {epi.content}")
        if sem:
            parts.append(f"[semantic@{sem.strength:.2f}] {sem.content}")

        return " | ".join(parts)


def demo():
    stack = LayeredMemoryStack()

    events = [
        "Lecture on memory architecture with GPT",
        "Lecture on identity superposition",
        "Walk by the river at sunset",
    ]

    for e in events:
        stack.encode_event(e)

    print("=== Initial encoding ===")
    for i, epi in enumerate(stack.episodic):
        print(i, epi)

    # Apply some decay
    stack.decay()

    print("\n=== After decay ===")
    for i, epi in enumerate(stack.episodic):
        print(i, epi)

    print("\n=== Reconstructed memories ===")
    for i in range(len(stack.episodic)):
        print(f"{i}: {stack.reconstruct(i)}")


if __name__ == "__main__":
    demo()
