"""Script Writer and Scene Planner for AutoShorts 2.0
Implements the 6-beat storytelling structure:
0-2s: HOOK
2-10s: SETUP
10-35s: ESCALATION
35-50s: INFOGRAPHIC PAYOFF
50-65s: RETURN & CONSEQUENCE
65-75s: FINAL REVEAL
"""

from typing import List, Dict, Any
from autoshorts2.models import (
    ScriptResult, ScenePlan, HudState, InfographicSpec, HookCandidate, ResearchFactSheet
)

SCRIPT_RAW_SCENES = [
    {
        "scene_id": 1,
        "beat": "HOOK",
        "narration": "He ordered 300,000 dollars in government coins... and the shipping was completely free.",
        "visual_description": "Protagonist in dark hoodie stands in a dim apartment hallway surrounded by towering wooden crates glowing with golden coin edges.",
        "character_action": "Protagonist holding a single shiny gold $1 coin up to the neon pink lamp light with a sly smirk.",
        "environment": "dim_apartment_hallway",
        "camera": "slow_push_in",
        "lighting": "dim_magenta_neon",
        "character_expression": "scheming_smirk",
        "character_pose": "holding_coin",
        "hud": {
            "label_1": "COINS", "val_1": "$300,000",
            "label_2": "SHIPPING", "val_2": "$0.00",
            "label_3": "RISK", "val_3": "10%",
            "progress_percent": 10.0
        },
        "sound_effect": "coins",
        "music_state": "mystery",
        "transition": "hard_cut",
        "emphasized_words": ["$300,000", "coins", "completely", "free"]
    },
    {
        "scene_id": 2,
        "beat": "SETUP",
        "narration": "In 2008, the US Mint wanted everyone using new $1 coins. But nobody wanted them.",
        "visual_description": "The US Treasury building silhouette under a dark stormy sky with official seal stamped in pink accent.",
        "character_action": "Protagonist looking at government website on a glowing laptop screen at his wooden desk.",
        "environment": "dim_apartment_desk",
        "camera": "pan_left",
        "lighting": "warm_desk_lamp",
        "character_expression": "focused_typing",
        "character_pose": "typing",
        "hud": {
            "label_1": "CIRCULATION", "val_1": "FAILING",
            "label_2": "COST", "val_2": "$1.00",
            "label_3": "INTEREST", "val_3": "0%",
            "progress_percent": 15.0
        },
        "sound_effect": "click",
        "music_state": "mystery",
        "transition": "hard_cut",
        "emphasized_words": ["2008", "$1", "nobody", "wanted"]
    },
    {
        "scene_id": 3,
        "beat": "SETUP",
        "narration": "So the government offered a bizarre deal: buy as many coins as you want online with a credit card, at face value, with free armored delivery.",
        "visual_description": "An armored Brink's delivery truck parked at the curb, headlights piercing the dark street as a giant box is unloaded.",
        "character_action": "Protagonist watching from his window, eyes wide as the credit card clicks on screen.",
        "environment": "street_curbside",
        "camera": "pull_out",
        "lighting": "dim_magenta_neon",
        "character_expression": "scheming_smirk",
        "character_pose": "window_peek",
        "hud": {
            "label_1": "DIRECT SHIP", "val_1": "ACTIVE",
            "label_2": "SHIPPING", "val_2": "$0 FREE",
            "label_3": "LIMIT", "val_3": "NONE",
            "progress_percent": 25.0
        },
        "sound_effect": "whoosh",
        "music_state": "tension_build",
        "transition": "hard_cut",
        "emphasized_words": ["bizarre", "deal", "credit", "card", "free", "armored"]
    },
    {
        "scene_id": 4,
        "beat": "ESCALATION",
        "narration": "Felix realized what this meant. He pulled out a rewards card paying 2% cash back, and ordered $5,000.",
        "visual_description": "Close up of an obsidian black rewards credit card tapping against the laptop, neon pink sparks popping.",
        "character_action": "Protagonist entering credit card digits with intense focus.",
        "environment": "dim_apartment_desk",
        "camera": "snap_zoom",
        "lighting": "warm_desk_lamp",
        "character_expression": "focused_typing",
        "character_pose": "typing",
        "hud": {
            "label_1": "ORDER", "val_1": "$5,000",
            "label_2": "CASHBACK", "val_2": "+$100",
            "label_3": "SUSPICION", "val_3": "5%",
            "progress_percent": 35.0
        },
        "sound_effect": "digital_scan",
        "music_state": "tension_build",
        "transition": "hard_cut",
        "emphasized_words": ["realized", "2%", "cash", "back", "$5,000"]
    },
    {
        "scene_id": 5,
        "beat": "ESCALATION",
        "narration": "When the heavy boxes arrived, he wheeled them straight into his local bank, deposited the cash, and paid off the card.",
        "visual_description": "Bank interior lobby with sleek glass windows. Protagonist wheels a heavy hand-truck stacked with coin boxes to the teller counter.",
        "character_action": "Protagonist casually pushing the heavy metal hand-truck toward the counter.",
        "environment": "bank_counter",
        "camera": "tracking_shot",
        "lighting": "bright_corporate",
        "character_expression": "straining_effort",
        "character_pose": "wheeling_cart",
        "hud": {
            "label_1": "DEPOSITED", "val_1": "$5,000",
            "label_2": "PROFIT", "val_2": "$100",
            "label_3": "SUSPICION", "val_3": "20%",
            "progress_percent": 45.0
        },
        "sound_effect": "cash_count",
        "music_state": "tension_build",
        "transition": "hard_cut",
        "emphasized_words": ["heavy", "bank", "deposited", "paid", "off"]
    },
    {
        "scene_id": 6,
        "beat": "ESCALATION",
        "narration": "Then he ordered $10,000. Then $50,000. His apartment was sinking under literal tons of gold-colored metal.",
        "visual_description": "Protagonist's small living room packed to the ceiling with heavy cardboard boxes stamped 'US MINT', floorboards flexing.",
        "character_action": "Protagonist sitting on a mountain of coin boxes, checking his exploding frequent flyer balance on his phone.",
        "environment": "apartment_boxes",
        "camera": "micro_shake",
        "lighting": "dim_magenta_neon",
        "character_expression": "wide_shock",
        "character_pose": "sitting_on_boxes",
        "hud": {
            "label_1": "COINS ORDERED", "val_1": "$150,000",
            "label_2": "MILES", "val_2": "300,000",
            "label_3": "WEIGHT", "val_3": "1.8 TONS",
            "progress_percent": 65.0
        },
        "sound_effect": "tension_pulse",
        "music_state": "tension_build",
        "transition": "zoom_transition",
        "emphasized_words": ["$10,000", "$50,000", "literal", "tons", "metal"]
    },
    {
        "scene_id": 7,
        "beat": "INFOGRAPHIC",
        "narration": "Here was the math: The US Mint charged exactly one dollar for a one-dollar coin, and paid 100% of shipping fees. The credit card paid 2% cash back. That meant free money with zero risk.",
        "visual_description": "Clean, ultra-high contrast beige documentary infographic screen. Bold black typography, large animated equation, and hot pink threshold highlight bar.",
        "character_action": "Clean graphical motion showing coin input, credit card 2% spread, and zero shipping barrier.",
        "environment": "infographic_beige",
        "camera": "slow_push_in",
        "lighting": "clean_documentary",
        "character_expression": "scheming_smirk",
        "character_pose": "standing",
        "hud": {
            "label_1": "US MINT COST", "val_1": "$1.00",
            "label_2": "SHIPPING", "val_2": "$0.00",
            "label_3": "CASHBACK", "val_3": "+2.0%",
            "progress_percent": 75.0
        },
        "is_infographic": True,
        "infographic_spec": {
            "title": "THE FREE MONEY SPREAD",
            "subtitle": "PRESIDENTIAL $1 COIN ARBITRAGE (2008)",
            "threshold_label": "INTERCHANGE PROFIT MARGIN",
            "threshold_value": "+2.00% NET SPREAD",
            "breakdown_items": [
                {"label": "Coin Purchase Price", "val": "$1.00 / Coin"},
                {"label": "Gov Armored Shipping", "val": "$0.00 (Subsidized)"},
                {"label": "Credit Card Reward", "val": "+$0.02 Cash Back"},
                {"label": "Local Bank Deposit", "val": "$1.00 Full Value"}
            ],
            "pink_highlight_stat": "ZERO DOWNSIDE RISK",
            "chart_type": "threshold_line"
        },
        "sound_effect": "ding",
        "music_state": "analytical_arp",
        "transition": "graphic_wipe",
        "emphasized_words": ["math", "one", "dollar", "100%", "shipping", "2%", "free", "money", "zero"]
    },
    {
        "scene_id": 8,
        "beat": "RETURN",
        "narration": "Back at the bank, tellers started panicking. Vault floors were literally running out of space to store 800-pound deliveries.",
        "visual_description": "Bank manager in suit staring in disbelief through glass window as an avalanche of coin rolls fills the vault shelf.",
        "character_action": "Bank manager holding his head in distress as protagonist stands at the counter with another pallet.",
        "environment": "bank_vault_meeting",
        "camera": "snap_zoom",
        "lighting": "bright_corporate",
        "character_expression": "nervous_sweat",
        "character_pose": "counter_talking",
        "hud": {
            "label_1": "VAULT FULL", "val_1": "CRITICAL",
            "label_2": "BANK PROFIT", "val_2": "$0",
            "label_3": "SUSPICION", "val_3": "85%",
            "progress_percent": 85.0
        },
        "sound_effect": "boom",
        "music_state": "climax_tension",
        "transition": "hard_cut",
        "emphasized_words": ["bank", "tellers", "panicking", "vault", "800-pound"]
    },
    {
        "scene_id": 9,
        "beat": "RETURN",
        "narration": "And then... the Department of the Treasury flagged his name.",
        "visual_description": "Red surveillance spotlight cuts across the scene. An official federal notice envelope lands heavily on the desk.",
        "character_action": "Protagonist freezing as the red warning alert flashes on his phone.",
        "environment": "dim_apartment_desk",
        "camera": "slow_push_in",
        "lighting": "red_alert",
        "character_expression": "panicked_stare",
        "character_pose": "shocked_freeze",
        "hud": {
            "label_1": "TOTAL ORDERED", "val_1": "$300,000",
            "label_2": "FLAGGED", "val_2": "YES",
            "label_3": "ALERT LEVEL", "val_3": "99%",
            "progress_percent": 95.0
        },
        "sound_effect": "stamp_impact",
        "music_state": "drop_silence",
        "transition": "hard_cut",
        "emphasized_words": ["Department", "Treasury", "flagged", "name"]
    },
    {
        "scene_id": 10,
        "beat": "REVEAL",
        "narration": "Federal investigators launched an audit. But they discovered something wild: he hadn't broken a single law. The Treasury had to shut down credit card purchases permanently—while he kept every single flight and dollar.",
        "visual_description": "Protagonist walking out into a rain-slicked city avenue under glowing neon signs, grinning with hands in pockets, looking back at the skyline.",
        "character_action": "Protagonist walking forward confidently as golden coin particles and airline boarding passes drift in the air.",
        "environment": "street_night",
        "camera": "tracking_shot",
        "lighting": "dim_magenta_neon",
        "character_expression": "triumphant",
        "character_pose": "proud_walk",
        "hud": {
            "label_1": "FREE FLIGHTS", "val_1": "LIFETIME",
            "label_2": "PROFIT", "val_2": "$6,000+",
            "label_3": "VERDICT", "val_3": "100% LEGAL",
            "progress_percent": 100.0
        },
        "sound_effect": "coins",
        "music_state": "sting",
        "transition": "hard_cut",
        "emphasized_words": ["investigators", "wild", "never", "broken", "law", "permanently", "kept", "every", "dollar"]
    }
]

class ScriptWriter:
    def create_script(self, hook: HookCandidate, fact_sheet: ResearchFactSheet) -> ScriptResult:
        full_text = " ".join(s["narration"] for s in SCRIPT_RAW_SCENES)
        words = full_text.split()
        
        scenes = []
        curr_time = 0.0
        for item in SCRIPT_RAW_SCENES:
            # Estimate scene duration based on word count (approx 2.5 words per sec + buffer)
            word_count = len(item["narration"].split())
            est_duration = max(3.0, round(word_count / 2.3, 2))
            
            hud_obj = None
            if "hud" in item:
                hud_obj = HudState(
                    label_1=item["hud"]["label_1"],
                    val_1=item["hud"]["val_1"],
                    label_2=item["hud"]["label_2"],
                    val_2=item["hud"]["val_2"],
                    label_3=item["hud"]["label_3"],
                    val_3=item["hud"]["val_3"],
                    progress_percent=item["hud"]["progress_percent"]
                )
                
            info_spec = None
            if item.get("is_infographic") and "infographic_spec" in item:
                spec_d = item["infographic_spec"]
                info_spec = InfographicSpec(
                    title=spec_d["title"],
                    subtitle=spec_d["subtitle"],
                    threshold_label=spec_d.get("threshold_label"),
                    threshold_value=spec_d.get("threshold_value"),
                    breakdown_items=spec_d.get("breakdown_items", []),
                    pink_highlight_stat=spec_d.get("pink_highlight_stat", ""),
                    chart_type=spec_d.get("chart_type", "threshold_line")
                )
                
            scene = ScenePlan(
                scene_id=item["scene_id"],
                beat=item["beat"],
                duration=est_duration,
                start_time=round(curr_time, 2),
                end_time=round(curr_time + est_duration, 2),
                narration=item["narration"],
                visual_description=item["visual_description"],
                character_action=item["character_action"],
                environment=item["environment"],
                camera=item["camera"],
                lighting=item["lighting"],
                character_expression=item["character_expression"],
                character_pose=item["character_pose"],
                hud_state=hud_obj,
                is_infographic=item.get("is_infographic", False),
                infographic_spec=info_spec,
                sound_effect=item.get("sound_effect"),
                music_state=item["music_state"],
                transition=item.get("transition", "hard_cut"),
                emphasized_words=item.get("emphasized_words", [])
            )
            scenes.append(scene)
            curr_time += est_duration
            
        return ScriptResult(
            title="The $300,000 Government Coin Glitch",
            selected_hook=hook,
            full_script_text=full_text,
            word_count=len(words),
            scenes=scenes
        )
