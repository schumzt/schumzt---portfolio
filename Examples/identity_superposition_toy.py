"""
identity_superposition_toy.py

Toy implementation of Identity Superposition / Identity Vector Integration.

We represent "identity states" as low-dimensional vectors and
construct a superposed identity vector as a weighted sum of
contextual selves.
"""

from dataclasses import dataclass
from typing import Dict, List
import math


@dataclass
class IdentityState:
    name: str
    vector: List[float]  # low-dimensional trait / role representation
    weight: float        # contextual activation


def l2_norm(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def normalize(v: List[float]) -> List[float]:
    n = l2_norm(v)
    if n == 0:
        return v
    return [x / n for x in v]


def superpose(states: List[IdentityState]) -> List[float]:
    dim = len(states[0].vector)
    agg = [0.0] * dim
    for s in states:
        for i in range(dim):
            agg[i] += s.weight * s.vector[i]
    return normalize(agg)


def cosine_similarity(a: List[float], b: List[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    den = l2_norm(a) * l2_norm(b)
    return 0.0 if den == 0 else num / den


def demo():
    # Very small 3D "trait" space: [analytical, empathic, playful]
    base_states = [
        IdentityState("Researcher", [0.9, 0.3, 0.2], weight=0.0),
        IdentityState("Teacher",    [0.7, 0.8, 0.4], weight=0.0),
        IdentityState("Artist",     [0.4, 0.6, 0.9], weight=0.0),
    ]

    # Scenario 1: in a research meeting
    for s in base_states:
        s.weight = {"Researcher": 0.9, "Teacher": 0.3, "Artist": 0.1}[s.name]
    research_identity = superpose(base_states)

    # Scenario 2: in a mentoring session
    for s in base_states:
        s.weight = {"Researcher": 0.4, "Teacher": 0.9, "Artist": 0.3}[s.name]
    mentoring_identity = superpose(base_states)

    print("=== Identity Superposition Demo ===")
    print("Base states (normalized vectors):")
    for s in base_states:
        print(f"  {s.name}: {normalize(s.vector)}")

    print("\nSuperposed identity (research meeting):", research_identity)
    print("Superposed identity (mentoring session):", mentoring_identity)

    print("\nCosine similarity to each base state:")
    for s in base_states:
        sim_r = cosine_similarity(research_identity, normalize(s.vector))
        sim_m = cosine_similarity(mentoring_identity, normalize(s.vector))
        print(
            f"  {s.name}: "
            f"sim(research)={sim_r:.3f}, sim(mentoring)={sim_m:.3f}"
        )


if __name__ == "__main__":
    demo()
