"""Data models and validation schemas for AutoShorts 2.0
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class FactualClaim(BaseModel):
    statement: str
    verified: bool = True
    source: str
    numeric_value: Optional[str] = None

class ResearchFactSheet(BaseModel):
    topic: str
    core_paradox: str
    historical_event_or_law: str
    key_numbers: List[str]
    claims: List[FactualClaim]
    unusual_details: List[str]

class StoryAngle(BaseModel):
    angle_id: int
    title: str
    premise: str
    curiosity_score: float
    surprise_score: float
    visual_potential: float
    total_score: float

class HookCandidate(BaseModel):
    hook_id: int
    hook_text: str
    structure_type: str  # e.g., "PERSON + ACTION + UNEXPECTED CONSEQUENCE"
    curiosity_score: float
    stakes_score: float
    total_score: float
    selected: bool = False

class CharacterBible(BaseModel):
    character_id: str = "protagonist_main"
    name: str = "The Arbitrageur"
    silhouette: str = "Sleek, distinctive profile with tilted cap and oversized hoodie"
    face_shape: str = "Stylized rounded rectangular light face with hand-drawn charcoal contour"
    face_color: str = "#F8F6F2"
    headwear: str = "Dark charcoal curved baseball cap (#111116)"
    clothing: str = "Oversized matte black hoodie (#16171E) with subtle hot-pink drawstrings (#FF2A85)"
    legs_and_feet: str = "Thin black tapered joggers and chunky white sneakers"
    expression_library: List[str] = Field(default_factory=lambda: [
        "scheming_smirk", "focused_typing", "straining_effort", "wide_shock", "nervous_sweat", "triumphant"
    ])
    body_animations: List[str] = Field(default_factory=lambda: [
        "typing", "hauling_crate", "wheeling_cart", "whispering", "frozen_spotlight"
    ])

class HudState(BaseModel):
    label_1: str = "ORDERED"
    val_1: str = "$0"
    label_2: str = "PROFIT"
    val_2: str = "$0"
    label_3: str = "SUSPICION"
    val_3: str = "0%"
    progress_percent: float = 0.0

class InfographicSpec(BaseModel):
    title: str
    subtitle: str
    threshold_label: Optional[str] = None
    threshold_value: Optional[str] = None
    breakdown_items: List[Dict[str, str]] = Field(default_factory=list)
    pink_highlight_stat: str
    chart_type: str = "threshold_line"  # "threshold_line", "comparison_bars", "flow_loop"

class SubtitleWord(BaseModel):
    word: str
    start: float
    end: float
    is_emphasized: bool = False

class ScenePlan(BaseModel):
    scene_id: int
    beat: str  # HOOK, SETUP, ESCALATION, INFOGRAPHIC, RETURN, REVEAL
    duration: float
    start_time: float
    end_time: float
    narration: str
    visual_description: str
    character_action: str
    environment: str  # dim_room, apartment_boxes, bank_counter, vault_meeting, infographic_beige, street_night
    camera: str  # push_in, pull_out, pan_left, snap_zoom, static_wide, micro_shake
    lighting: str  # warm_desk_lamp, dim_magenta_neon, bright_corporate, clean_documentary, red_alert
    character_expression: str
    character_pose: str
    hud_state: Optional[HudState] = None
    is_infographic: bool = False
    infographic_spec: Optional[InfographicSpec] = None
    sound_effect: Optional[str] = None
    music_state: str  # mystery, tension_build, analytical_arp, climax_tension, drop_silence, sting
    transition: str = "hard_cut"
    emphasized_words: List[str] = Field(default_factory=list)

class ScriptResult(BaseModel):
    title: str
    selected_hook: HookCandidate
    full_script_text: str
    word_count: int
    scenes: List[ScenePlan]

class Storyboard(BaseModel):
    project_id: str
    topic: str
    voice_profile: str
    total_duration: float
    scenes: List[ScenePlan]
    words: List[SubtitleWord]

class FinalOutputPackage(BaseModel):
    title: str
    hook: str
    full_script: str
    character_bible: CharacterBible
    scene_plan: List[Dict[str, Any]]
    visual_prompts: List[Dict[str, str]]
    infographic_specs: List[Dict[str, Any]]
    voiceover_script: str
    subtitle_file_srt: str
    subtitle_file_ass: str
    music_direction: Dict[str, str]
    sfx_timeline: List[Dict[str, Any]]
    editing_timeline: List[Dict[str, Any]]
    final_mp4_path: str
    thumbnail_path: str
    youtube_description: str
    hashtags: List[str]

class ShortProject(BaseModel):
    project_id: str
    topic: str
    category: str = "money_loophole"
    research: ResearchFactSheet
    selected_angle: StoryAngle
    character_bible: CharacterBible
    script: ScriptResult
    storyboard: Storyboard
    audio_path: Optional[str] = None
    final_video_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    output_package: Optional[FinalOutputPackage] = None
    created_at: str
