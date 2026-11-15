"""Planetary Scientific Data & Physical Constants for WHAT IF? Universe
Accurate scientific facts for planetary exploration Shorts.
"""

from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class PlanetFacts:
    name: str
    gravity_g: float
    surface_temp_avg: str
    surface_pressure_atm: float
    atmosphere_composition: str
    day_length: str
    distance_from_sun: str
    unprotected_survival_time: str
    key_hazards: List[str]
    color_palette: Dict[str, str]

PLANET_DATABASE: Dict[str, PlanetFacts] = {
    "mars": PlanetFacts(
        name="Mars",
        gravity_g=0.38,
        surface_temp_avg="-63°C (-81°F)",
        surface_pressure_atm=0.006,  # 0.6% of Earth
        atmosphere_composition="95% Carbon Dioxide, 2.6% Nitrogen, 1.9% Argon, 0.16% Oxygen",
        day_length="24 hours, 37 minutes (1 Sol)",
        distance_from_sun="228 million km (1.52 AU)",
        unprotected_survival_time="Under 15 seconds (blood boils at body temp due to Armstrong Limit)",
        key_hazards=[
            "Extremely low pressure (Armstrong Limit)",
            "Planet-wide blinding dust storms",
            "Severe solar and cosmic radiation",
            "Sub-zero extreme nighttime temperatures (-125°C)"
        ],
        color_palette={
            "primary": "#C65B45",
            "secondary": "#F18B45",
            "accent": "#55D7E8",
            "sky": "#341B26"
        }
    ),
    "moon": PlanetFacts(
        name="The Moon",
        gravity_g=0.166,
        surface_temp_avg="-130°C to +120°C",
        surface_pressure_atm=0.0,
        atmosphere_composition="Vacuum (Trace Helium, Neon, Hydrogen)",
        day_length="29.5 Earth days",
        distance_from_sun="150 million km (1.0 AU)",
        unprotected_survival_time="Under 10 seconds (vacuum ebullism)",
        key_hazards=[
            "Total vacuum",
            "Razor-sharp abrasive regolith dust",
            "Extreme thermal swings",
            "Micrometeorite impacts"
        ],
        color_palette={
            "primary": "#536780",
            "secondary": "#A4AFC0",
            "accent": "#55D7E8",
            "sky": "#080B14"
        }
    ),
    "jupiter": PlanetFacts(
        name="Jupiter",
        gravity_g=2.53,  # cloud top
        surface_temp_avg="-110°C (upper cloud deck)",
        surface_pressure_atm=2.0,  # increases to millions of atm deeper down
        atmosphere_composition="90% Hydrogen, 10% Helium, traces of Methane & Ammonia",
        day_length="9 hours, 55 minutes",
        distance_from_sun="778 million km (5.2 AU)",
        unprotected_survival_time="Instant crushing & radiation death",
        key_hazards=[
            "No solid surface to stand on",
            "Super-lethal radiation belts",
            "600 km/h jet streams & storms",
            "Crushing atmospheric pressure deeper in core"
        ],
        color_palette={
            "primary": "#D48B47",
            "secondary": "#E5A96A",
            "accent": "#8064C8",
            "sky": "#10182A"
        }
    ),
    "titan": PlanetFacts(
        name="Titan",
        gravity_g=0.14,
        surface_temp_avg="-179°C (-290°F)",
        surface_pressure_atm=1.45,  # 50% higher than Earth!
        atmosphere_composition="95% Nitrogen, 5% Methane",
        day_length="15 Earth days, 22 hours",
        distance_from_sun="1.4 billion km (9.5 AU)",
        unprotected_survival_time="Hypothermia in minutes; pressure is safe but no oxygen",
        key_hazards=[
            "Cryogenic liquid methane lakes",
            "Deep sub-zero temperatures (-179°C)",
            "Thick orange photochemical smog",
            "Suffocation (zero oxygen)"
        ],
        color_palette={
            "primary": "#D9933B",
            "secondary": "#7A5623",
            "accent": "#55D7E8",
            "sky": "#21160B"
        }
    )
}
