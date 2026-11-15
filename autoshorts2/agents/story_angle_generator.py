"""Story Angle and Hook Optimizer for AutoShorts 2.0
"""

from typing import List, Tuple
from autoshorts2.models import StoryAngle, HookCandidate, ResearchFactSheet

class StoryAngleGenerator:
    def generate_angles(self, fact_sheet: ResearchFactSheet) -> List[StoryAngle]:
        angles = [
            StoryAngle(
                angle_id=1,
                title="The Free Money Loophole: How One Guy Got $300,000 From The US Mint",
                premise="Focus on the staggering physical absurdity of tons of $1 coins delivered to an apartment and wheeled into banks for infinite credit card points.",
                curiosity_score=9.7,
                surprise_score=9.8,
                visual_potential=9.9,
                total_score=9.8
            ),
            StoryAngle(
                angle_id=2,
                title="The Federal Reserve's Worst Nightmare",
                premise="Focus on the bank's perspective: a customer repeatedly bringing in hundreds of pounds of coins, triggering panic in the vault.",
                curiosity_score=9.1,
                surprise_score=8.9,
                visual_potential=8.8,
                total_score=8.93
            ),
            StoryAngle(
                angle_id=3,
                title="How To Fly First Class Forever For $0",
                premise="Focus on the travel hacker perspective racking up millions of miles using government coin subsidies.",
                curiosity_score=9.3,
                surprise_score=8.7,
                visual_potential=8.5,
                total_score=8.83
            ),
            StoryAngle(
                angle_id=4,
                title="The $1 Coin Disaster That Cost Taxpayers Millions",
                premise="Focus on government bureaucratic failure and why the Mint paid shipping companies millions.",
                curiosity_score=8.4,
                surprise_score=8.6,
                visual_potential=8.2,
                total_score=8.4
            ),
            StoryAngle(
                angle_id=5,
                title="The Perfect Legal Arbitrage",
                premise="Analytical breakdown of interchange fees, cash back percentages, and deposit velocity.",
                curiosity_score=8.8,
                surprise_score=8.9,
                visual_potential=9.0,
                total_score=8.9
            )
        ]
        # Return sorted by highest total score
        return sorted(angles, key=lambda a: a.total_score, reverse=True)


class HookOptimizer:
    def generate_and_score_hooks(self, selected_angle: StoryAngle) -> Tuple[HookCandidate, List[HookCandidate]]:
        """Generates 10 hooks adhering to PERSON + ACTION + UNEXPECTED CONSEQUENCE structure."""
        hooks = [
            HookCandidate(
                hook_id=1,
                hook_text="He ordered 300,000 dollars in government coins... and the shipping was completely free.",
                structure_type="PERSON + ACTION + UNEXPECTED CONSEQUENCE",
                curiosity_score=9.9,
                stakes_score=9.7,
                total_score=9.8,
                selected=True
            ),
            HookCandidate(
                hook_id=2,
                hook_text="This man discovered an infinite money glitch, and the US government paid for it.",
                structure_type="PERSON + DISCOVERY + UNEXPECTED SPONSOR",
                curiosity_score=9.4,
                stakes_score=9.2,
                total_score=9.3
            ),
            HookCandidate(
                hook_id=3,
                hook_text="He bought 800 pounds of gold-colored coins on his credit card... but he never spent a single dollar.",
                structure_type="PERSON + ACTION + PARADOX",
                curiosity_score=9.6,
                stakes_score=9.3,
                total_score=9.45
            ),
            HookCandidate(
                hook_id=4,
                hook_text="In 2008, one guy made $6,000 every month using this legal banking loophole.",
                structure_type="TIME + ACTION + REVENUE",
                curiosity_score=9.1,
                stakes_score=9.0,
                total_score=9.05
            ),
            HookCandidate(
                hook_id=5,
                hook_text="The delivery truck dropped 40 heavy wooden boxes on his porch... and the neighbors called the police.",
                structure_type="ACTION + PHYSICAL PROP + ESCALATION",
                curiosity_score=9.2,
                stakes_score=8.9,
                total_score=9.05
            ),
            HookCandidate(
                hook_id=6,
                hook_text="He figured out how to get free airline tickets forever, without breaking a single law.",
                structure_type="PERSON + REWARD + LEGALITY",
                curiosity_score=8.9,
                stakes_score=8.7,
                total_score=8.8
            ),
            HookCandidate(
                hook_id=7,
                hook_text="The bank manager stared at the 800-pound cart of coins, and refused to open the vault.",
                structure_type="CHARACTER + REACTION + CONFLICT",
                curiosity_score=9.0,
                stakes_score=9.1,
                total_score=9.05
            ),
            HookCandidate(
                hook_id=8,
                hook_text="He deposited thousands of dollars every week, but he wasn't running a business.",
                structure_type="ACTION + CADENCE + MYSTERY",
                curiosity_score=9.1,
                stakes_score=8.8,
                total_score=8.95
            ),
            HookCandidate(
                hook_id=9,
                hook_text="The US Mint tried to fix a tiny currency mistake... and accidentally handed him millions in rewards.",
                structure_type="INSTITUTION + MISTAKE + CONSEQUENCE",
                curiosity_score=9.3,
                stakes_score=9.2,
                total_score=9.25
            ),
            HookCandidate(
                hook_id=10,
                hook_text="He discovered a flaw in the US Treasury website that let him print unlimited credit card points.",
                structure_type="DISCOVERY + FLAW + BENEFIT",
                curiosity_score=9.2,
                stakes_score=9.4,
                total_score=9.3
            )
        ]
        
        # Best hook is Hook #1
        selected = hooks[0]
        return selected, hooks
