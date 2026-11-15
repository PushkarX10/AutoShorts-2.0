"""WHAT IF? Space & Planet Exploration CLI Interface
Run from terminal to generate new scientific 2D animated space Shorts.
Usage:
    python -m autoshorts2.space.cli generate "What if you lived on Mars for 30 days?" --planet mars
    python -m autoshorts2.space.cli list-planets
"""

import argparse
import sys
from autoshorts2.space.planet_data import PLANET_DATABASE
from autoshorts2.space.pipeline import SpaceShortsPipeline

def main():
    parser = argparse.ArgumentParser(
        description="WHAT IF? — Space & Planet Exploration Shorts Automation Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a complete animated space Short")
    gen_parser.add_argument("topic", type=str, help="Topic/Question (e.g. 'What if you lived on Mars for 30 days?')")
    gen_parser.add_argument("--planet", "-p", default="mars", choices=list(PLANET_DATABASE.keys()), help="Target planet")
    gen_parser.add_argument("--voice", "-v", default="en-US-ChristopherNeural", help="Edge-TTS voice")

    # List planets command
    subparsers.add_parser("list-planets", help="List supported planets and physical scientific constants")

    args = parser.parse_args()

    if args.command == "list-planets":
        print("\n=== SUPPORTED PLANETARY DATABASES ===")
        for key, p in PLANET_DATABASE.items():
            print(f"\n[{key.upper()}] - {p.name}")
            print(f"  Gravity: {p.gravity_g}g | Avg Temp: {p.surface_temp_avg} | Pressure: {p.surface_pressure_atm} ATM")
            print(f"  Atmosphere: {p.atmosphere_composition}")
            print(f"  Hazards: {', '.join(p.key_hazards)}")
            print(f"  Survival: {p.unprotected_survival_time}")
        print()
        sys.exit(0)

    elif args.command == "generate":
        pipeline = SpaceShortsPipeline(voice=args.voice)
        result = pipeline.generate_short(topic=args.topic, planet_key=args.planet)
        print(f"\n[SUCCESS] Generated Short at: {result['video_path']}")
        sys.exit(0)

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
