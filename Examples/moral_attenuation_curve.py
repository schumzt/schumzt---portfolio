"""
moral_attenuation_curve.py

Toy implementation of Moral Attenuation Theory (MAT).

This script defines a very simple attenuation function:

    responsibility_weight = rarity_factor
                             * exp(-time / tau_time)
                             * exp(-distance / tau_distance)

This is NOT claiming to be the "true" functional form.
The purpose is just to show how moral responsibility can be modeled
as a decaying weight over time and distance, modulated by rarity.
"""

import math
from dataclasses import dataclass
from typing import List


@dataclass
class EventContext:
    time_days: float        # time since event (days)
    distance_km: float      # social/physical distance proxy
    rarity: float           # 0~1 (1 = extremely rare, 0 = trivial)


def moral_attenuation(ctx: EventContext,
                      tau_time: float = 365.0,
                      tau_distance: float = 5000.0) -> float:
    """
    Compute a toy responsibility weight between 0 and 1.

    - tau_time: time scale of moral fading
    - tau_distance: distance scale of moral fading
    """
    time_factor = math.exp(-ctx.time_days / tau_time)
    distance_factor = math.exp(-ctx.distance_km / tau_distance)
    weight = ctx.rarity * time_factor * distance_factor
    return weight


def demo():
    examples: List[EventContext] = [
        EventContext(time_days=1, distance_km=1, rarity=1.0),
        EventContext(time_days=365, distance_km=10, rarity=0.8),
        EventContext(time_days=365 * 5, distance_km=1000, rarity=0.9),
        EventContext(time_days=365 * 20, distance_km=10000, rarity=1.0),
    ]

    print("=== Moral Attenuation Demo ===")
    for i, ctx in enumerate(examples):
        w = moral_attenuation(ctx)
        print(
            f"Case {i}: time={ctx.time_days} days, "
            f"distance={ctx.distance_km} km, rarity={ctx.rarity} → "
            f"weight={w:.4f}"
        )

    # Optional: simple ASCII curve for time decay
    print("\n=== Time decay with fixed distance & rarity ===")
    for days in [0, 30, 180, 365, 365 * 5, 365 * 20]:
        ctx = EventContext(time_days=days, distance_km=0, rarity=1.0)
        w = moral_attenuation(ctx)
        bar = "#" * int(w * 40)
        print(f"{days:5d} days: {w:.4f} {bar}")


if __name__ == "__main__":
    demo()
