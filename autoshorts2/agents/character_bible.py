"""Character Bible Generator and Consistency Manager for AutoShorts 2.0
"""

from autoshorts2.models import CharacterBible

def create_default_protagonist() -> CharacterBible:
    return CharacterBible(
        character_id="hero_arbitrageur",
        name="Felix 'The Point Hunter'",
        silhouette="Sharp, sleek profile with dark flat-brim baseball cap, oversized charcoal hoodie, and thin expressive limbs",
        face_shape="Rounded geometric white/light face (#F8F6F2) with confident expressive eyes and hand-drawn dark contour",
        face_color="#F8F6F2",
        headwear="Matte charcoal baseball cap (#111116) worn forward with slight upward tilt",
        clothing="Oversized matte charcoal-black hoodie (#16171E) with electric neon pink drawstrings (#FF2A85)",
        legs_and_feet="Slim black joggers (#101014) and crisp white sneakers with pink soles (#FFFFFF / #FF2A85)",
        expression_library=[
            "scheming_smirk",       # calculating the loophole
            "focused_typing",       # ordering online late at night
            "straining_effort",     # hauling heavy crates of coins
            "wide_shock",           # delivery trucks filling the street
            "nervous_sweat",        # teller staring with suspicion
            "panicked_stare",       # letter from the Treasury arrives
            "triumphant_grin"       # walking away with free miles & cash
        ],
        body_animations=[
            "laptop_typing",
            "box_lifting",
            "cart_wheeling",
            "counter_talking",
            "suspicious_glance",
            "shocked_freeze"
        ]
    )
