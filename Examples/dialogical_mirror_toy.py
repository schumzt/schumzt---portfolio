"""
dialogical_mirror_toy.py

Toy simulation of Dialogical Mirror dynamics.

We model:
- a Self state with a belief value between -1 and 1
- a Mirror state that reflects and slightly stabilizes / challenges it

The update rule is intentionally simple. The purpose is just to show
how iterated dialogue can:
- reduce extremes,
- increase coherence,
- or amplify certain tendencies, depending on parameters.
"""

from dataclasses import dataclass


@dataclass
class AgentState:
    name: str
    belief: float  # -1 ~ 1


def update_dialogue(self: AgentState,
                    mirror: AgentState,
                    reflection_strength: float = 0.6,
                    challenge_strength: float = 0.2) -> None:
    """
    One dialogue step:

    - mirror moves slightly toward self (reflection)
    - self moves toward a weighted combination of:
        * mirror (recognition)
        * a moderated value (challenge against extremes)
    """
    # Mirror reflects the self
    mirror.belief += reflection_strength * (self.belief - mirror.belief)

    # "Moderated" value is a contraction toward 0
    moderated = self.belief * (1.0 - challenge_strength)

    # Self moves toward (mirror + moderated) / 2
    target = 0.5 * (mirror.belief + moderated)
    self.belief += 0.5 * (target - self.belief)  # soft update


def demo():
    self = AgentState("Self", belief=0.9)   # initially extreme
    mirror = AgentState("Mirror", belief=0.0)

    print("=== Dialogical Mirror Demo ===")
    print(f"Initial: Self={self.belief:.3f}, Mirror={mirror.belief:.3f}")

    for step in range(1, 11):
        update_dialogue(self, mirror)
        print(
            f"Step {step:2d}: "
            f"Self={self.belief:.3f}, Mirror={mirror.belief:.3f}"
        )


if __name__ == "__main__":
    demo()
