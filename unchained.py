import os
import sys
import time
import random
import textwrap

# ══════════════════════════════════════════════════════════════
#         U N C H A I N E D
#         The Curse of the Sunken Compass
# ══════════════════════════════════════════════════════════════

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PLAYER STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

player = {
    "name": "Adventurer",
    "current_room": "shore",
    "inventory": [],
    "visited_rooms": [],
    "turn_count": 0,

    # Combat stats
    "health": 100,
    "max_health": 100,
    "stamina": 50,
    "max_stamina": 50,
    "stamina_regen": 5,
    "momentum": 0,

    # Status
    "status_effects": [],
    "in_combat": False,
    "combat_target": None,

    # Reactive systems (-10 to +10)
    "morality": 0,
    "reputation": 0,
    "jack_trust": 0,
    "terror_allegiance": 0,
    "crown_allegiance": 0,
    "witch_trades": [],

    # Story flags
    "heart_destroyed": False,
    "heart_weakened": False,
    "colossals_freed": False,
    "jones_confronted": False,
    "jones_knows_journals": False,
    "tidal_vision_seen": False,
    "lighthouse_signaled": False,
    "altar_ritual_done": False,
    "coat_worn": False,
    "guardian_defeated": False,
    "ghost_sailor_named": False,

    # Jack state
    "jack_dismissed_count": 0,
    "jack_vanished": False,

    # Colossal command cooldown
    "colossal_cooldown": 0,

    "game_over": False,
    "ending": None,

    # Runtime state
    "triggered_events": [],
    "cutlass_oiled": False
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# WORLD — 22 ROOMS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

rooms = {
    "shore": {
        "description": (
            "Sand black as charcoal. Your ship is matchwood behind you — "
            "three pieces, already sinking. Offshore, two colossal shapes "
            "clash in the deep, the sea churning white around them. The "
            "air smells of salt and something older. Something that has "
            "been waiting. A translucent figure materializes from the "
            "spray, smelling inexplicably of cheese."
        ),
        "exits": {
            "north": "jungle_path",
            "east": "six_crowned_shallows",
            "west": "abyssal_crown_reef",
            "south": "wreck_of_ship"
        },
        "items": [],
        "npc": "barnacle_jack",
        "hidden": False,
        "combat_room": False,
        "environment_actions": []
    },

    "wreck_of_ship": {
        "description": (
            "The hull lies in three pieces. Barnacles have already begun "
            "their work — ambitious little things. Your logbook floats "
            "in the shallows. A rusted boarding axe is lodged in what "
            "used to be the mast. And there, somehow completely intact "
            "among the carnage: a locked chest. The sea took everything "
            "except that. Make of that what you will."
        ),
        "exits": {"north": "shore"},
        "items": ["old_logbook", "boarding_axe", "locked_chest"],
        "npc": None,
        "hidden": True,
        "combat_room": False,
        "environment_actions": []
    },

    "six_crowned_shallows": {
        "description": (
            "Shallow water, crystal clear, warm in a way the rest of "
            "this island is not. Six-headed eels drift through the coral. "
            "Twin-jawed crabs pick through the sand with unsettling "
            "precision. Everything here has too many of something. "
            "Offshore, one of the Six-Crowned Terror's heads rises "
            "slowly above the waterline and regards you with what can "
            "only be described as mild professional interest."
        ),
        "exits": {"west": "shore", "north": "tidal_pool"},
        "items": [],
        "npc": "terror_heads",
        "hidden": True,
        "combat_room": False,
        "environment_actions": []
    },

    "abyssal_crown_reef": {
        "description": (
            "A natural rock arch frames the deep water beyond — darker "
            "than it should be, darker than the sky above it. Kraken "
            "hatchlings no larger than your arm drift through the coral "
            "like smoke. Something vast and serpentine moves in the "
            "water beyond the arch, slow and deliberate as a tide. Near "
            "the base of the arch, a hatchling struggles beneath a "
            "collapsed rock formation. It has been there a while."
        ),
        "exits": {"east": "shore", "north": "bone_bridge"},
        "items": [],
        "npc": "kraken_hatchling",
        "hidden": True,
        "combat_room": False,
        "environment_actions": []
    },

    "jungle_path": {
        "description": (
            "Dense. Wrong. The canopy is too thick for the amount of "
            "light filtering through it — the math doesn't work. Roots "
            "reach across the path like they're trying to slow you down. "
            "The ground pulses beneath your boots, soft and rhythmic. "
            "Not like an earthquake. Like a heartbeat. The island is "
            "alive, you realize. You file this under problems to deal "
            "with later."
        ),
        "exits": {
            "south": "shore",
            "north": "ghost_camp",
            "west": "mangrove_maze",
            "east": "crows_perch"
        },
        "items": [],
        "npc": None,
        "hidden": False,
        "combat_room": False,
        "environment_actions": []
    },

    "crows_perch": {
        "description": (
            "A dead tree so large its lowest branch is taller than a "
            "ship's mast. Something has built a nest up here — layers "
            "of sailcloth, rope, and what appears to be an entire "
            "ship's wheel reduced to kindling. Inside the nest: a "
            "spyglass, a compass shard, and a piece of sailcloth "
            "covered in drawings. A child drew this. No child should "
            "know this island exists."
        ),
        "exits": {"west": "jungle_path"},
        "items": ["spyglass", "compass_shard", "island_map"],
        "npc": None,
        "hidden": True,
        "combat_room": False,
        "environment_actions": []
    },

    "mangrove_maze": {
        "description": (
            "Roots tangle into walls. Brackish water fills the spaces "
            "between them, knee-deep in places, chest-deep in others. "
            "The paths shift as the tide breathes in and out — what "
            "was passable a moment ago is gone. Between two roots "
            "ahead, something stands very still. Human-shaped. Not "
            "moving. Not quite looking at you, but aware you're there "
            "in the way only the dead can be."
        ),
        "exits": {"east": "jungle_path", "north": "ghost_camp"},
        "items": [],
        "npc": "ghost_sailor",
        "hidden": False,
        "combat_room": False,
        "environment_actions": []
    },

    "ghost_camp": {
        "description": (
            "The ruins of a camp — tents reduced to frames, a fire pit "
            "that hasn't held flame in centuries. Undead sailors move "
            "through it with the weary routine of people who have "
            "completely run out of things to do but haven't figured "
            "out how to stop. One is doing laundry. Another is losing "
            "an argument with a seagull. A third sits sharpening a "
            "knife that has no blade, the grinding sound somehow "
            "perfectly convincing."
        ),
        "exits": {
            "south": "jungle_path",
            "north": "sea_cave",
            "east": "witch_hut",
            "west": "shipwreck_hollow"
        },
        "items": [],
        "npc": "ghost_crew",
        "hidden": False,
        "combat_room": False,
        "environment_actions": []
    },

    "witch_hut": {
        "description": (
            "Built from driftwood and whale bone, lashed together with "
            "rope that looks like it was never meant to hold but has "
            "held for forty years regardless. Inside, hanging things "
            "catch the light — glass, bone, things you don't have "
            "names for. A woman sits with her back to you. She doesn't "
            "look up. She already knew you were coming. She's been "
            "deciding what she thinks of you since before you arrived."
        ),
        "exits": {"west": "ghost_camp"},
        "items": [],
        "npc": "witch",
        "hidden": True,
        "combat_room": False,
        "environment_actions": []
    },

    "shipwreck_hollow": {
        "description": (
            "A cave swallowed thirty ships and kept them. Masts rise "
            "like a dead forest. Figureheads stare at nothing with "
            "painted eyes — women, lions, sea creatures, all wearing "
            "the same expression, which is no expression at all. This "
            "is where the island puts what it takes. Against a broken "
            "mast, deliberately propped, sits a logbook. Someone "
            "wanted it to be found. They just didn't know if anyone "
            "ever would be."
        ),
        "exits": {"east": "ghost_camp"},
        "items": ["captains_logbook"],
        "npc": None,
        "hidden": True,
        "combat_room": False,
        "environment_actions": []
    },

    "sea_cave": {
        "description": (
            "Dark. Flooded ankle-deep, the water cold enough to make "
            "your boots feel like they're filling with ice. The air "
            "hums with something ancient and deeply unhappy about "
            "visitors. Bioluminescence traces the cave walls in slow "
            "pulses — almost beautiful, if you weren't busy noticing "
            "the enormous shape at the far end. Four arms. Barnacled. "
            "The size of a mill door. It is holding a blade that "
            "catches the dim light like it was made for exactly this."
        ),
        "exits": {
            "south": "ghost_camp",
            "north": "the_ruins",
            "east": "tidal_pool"
        },
        "items": [],
        "npc": "cave_guardian",
        "hidden": False,
        "combat_room": True,
        "environment_actions": [
            "throw stalactite",
            "use cave walls",
            "flood corner",
            "use water"
        ]
    },

    "tidal_pool": {
        "description": (
            "A natural pool, connected to the open sea through channels "
            "you can't see. Luminescent creatures drift through it like "
            "living stars that got turned around on the way somewhere "
            "better. The water is warm. The silence here is complete — "
            "no wind, no waves, no island heartbeat. At the bottom of "
            "the pool, something vast and patient waits. Not a monster. "
            "Not a threat. Something old enough that those categories "
            "stopped applying to it centuries ago."
        ),
        "exits": {"west": "sea_cave", "south": "six_crowned_shallows"},
        "items": [],
        "npc": "deep_presence",
        "hidden": True,
        "combat_room": False,
        "environment_actions": []
    },

    "bone_bridge": {
        "description": (
            "A bridge built entirely from whale bones, spanning a gorge "
            "above open sea. The engineering is impossible and has been "
            "standing for three hundred years anyway. Every surface is "
            "carved with names — small, careful letters, hundreds of "
            "them, covering every bone from end to end. Every soul the "
            "island has ever taken. The bridge groans in the wind. Not "
            "structurally. More like it's tired."
        ),
        "exits": {
            "south": "abyssal_crown_reef",
            "east": "sea_cave",
            "north": "storm_altar"
        },
        "items": [],
        "npc": None,
        "hidden": False,
        "combat_room": False,
        "environment_actions": []
    },

    "storm_altar": {
        "description": (
            "A circle of standing stones on a cliff face, wrapped in a "
            "storm that goes no further than the stones themselves. "
            "Lightning strikes them in rhythm — irregular but patterned, "
            "like a language with very high stakes punctuation. The "
            "stones are covered in script that shifts when you look "
            "directly at it, settling into legibility only in your "
            "peripheral vision. The air tastes like the moment before "
            "something irreversible happens."
        ),
        "exits": {
            "south": "bone_bridge",
            "east": "the_ruins",
            "west": "volcanic_ridge"
        },
        "items": [],
        "npc": None,
        "hidden": False,
        "combat_room": False,
        "environment_actions": []
    },

    "volcanic_ridge": {
        "description": (
            "Black rock runs along the island's spine like a scar. Hot "
            "underfoot — not uncomfortable, but insistent, reminding "
            "you the island has opinions about what it's made of. Steam "
            "vents punctuate the ridge at irregular intervals with a "
            "sound disturbingly close to breathing. The rock catches "
            "light strangely in places. Dark glass. Volcanic, sharp-"
            "edged, the kind of material that makes a blade want to "
            "happen."
        ),
        "exits": {
            "east": "storm_altar",
            "south": "jungle_path",
            "north": "ruined_lighthouse"
        },
        "items": ["volcanic_shard"],
        "npc": None,
        "hidden": False,
        "combat_room": False,
        "environment_actions": []
    },

    "hidden_grotto": {
        "description": (
            "The entrance is behind a waterfall of bioluminescent algae "
            "that falls completely silently, which is wrong in a way "
            "that takes a moment to place. Inside: silence so complete "
            "you can hear your own pulse. The cave walls are covered "
            "in a mural painted by human hands — careful, deliberate "
            "strokes, the kind that take time. Someone wanted whoever "
            "found this to understand something. They painted it like "
            "they weren't sure anyone ever would."
        ),
        "exits": {"south": "volcanic_ridge"},
        "items": [],
        "npc": None,
        "hidden": True,
        "combat_room": False,
        "environment_actions": []
    },

    "sunken_crypt": {
        "description": (
            "An underground chamber, partially flooded, the water still "
            "and black as ink. Personal effects are arranged on every "
            "dry surface — journals, navigational charts, instruments. "
            "A portrait hangs on the far wall, deliberately defaced "
            "but not destroyed. Someone couldn't bring themselves to "
            "finish the job. The air is still in a way that feels "
            "chosen. Whatever happened here, it happened slowly. "
            "The room has had a long time to remember it."
        ),
        "exits": {"west": "the_ruins"},
        "items": ["jones_journal"],
        "npc": None,
        "hidden": True,
        "combat_room": False,
        "environment_actions": []
    },

    "the_ruins": {
        "description": (
            "A temple so old the coral has become structural — remove "
            "it and the walls would follow. Carvings cover every surface: "
            "sea creatures in chains, a figure on a throne of bones, "
            "tidal patterns that repeat in fractals too precise to be "
            "decorative. Beneath the cracked floor, something pulses "
            "with slow, terrible rhythm. Warm through the stone. "
            "Insistent. Like it knows you're standing on it. Like it "
            "has been waiting for exactly this."
        ),
        "exits": {
            "south": "sea_cave",
            "east": "sunken_crypt",
            "west": "storm_altar",
            "north": "clifftop"
        },
        "items": ["heart_of_the_locker"],
        "npc": "davy_jones",
        "hidden": False,
        "combat_room": True,
        "environment_actions": ["overturn altar", "smash pillar", "invoke heart"]
    },

    "ruined_lighthouse": {
        "description": (
            "The lighthouse stopped functioning centuries ago — not "
            "because the mechanism broke, but because someone removed "
            "the oil and didn't come back. The mirror array at the top "
            "is intact, untouched, gathering dust with extraordinary "
            "patience. Through the salt-crusted window: open sea, "
            "horizon to horizon, and somewhere beyond it, the rest of "
            "the world. Still out there. Still happening without you."
        ),
        "exits": {"south": "volcanic_ridge", "east": "clifftop"},
        "items": [],
        "npc": None,
        "hidden": False,
        "combat_room": False,
        "environment_actions": []
    },

    "clifftop": {
        "description": (
            "The highest point on the island. The ocean in every "
            "direction, the horizon a perfect unbroken line except "
            "for the churning where the sea is doing something it "
            "shouldn't. The island cracks and shudders beneath your "
            "feet — not collapsing, not yet, but making its intentions "
            "clear. Far below, the water tears open in a circle large "
            "enough to swallow a fleet. Something is rising from it. "
            "Something that contains everything the ocean ever learned "
            "to be afraid of, assembled into a single answer to the "
            "question of what fear looks like when it has no more use "
            "for metaphor."
        ),
        "exits": {},
        "items": [],
        "npc": "sovereign",
        "hidden": False,
        "combat_room": True,
        "environment_actions": ["cut chain", "call colossals", "use compass"]
    }
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ITEMS — 21 ITEMS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

items = {
    "old_logbook": {
        "name": "Old Logbook",
        "description": (
            "Your logbook. Waterlogged, half the ink dissolved into "
            "the sea. What remains is mundane — supply lists, weather "
            "notes, the coordinates of a place you'll never reach now. "
            "The last entry reads: 'Island on the horizon. Not on any "
            "chart. Heading toward it.' You wrote that yourself. You "
            "were optimistic then."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": False,
        "quest_item": False
    },

    "boarding_axe": {
        "name": "Boarding Axe",
        "description": (
            "Rusted but solid. Lodged in the remains of the mast with "
            "enough force that whoever threw it — you, during the "
            "wreck, apparently — had a very bad moment right before "
            "doing so. The edge is dull. It will still ruin someone's "
            "day if applied correctly."
        ),
        "obtainable": True,
        "combinable": True,
        "combines_with": "volcanic_shard",
        "combines_into": "ashblade",
        "single_use": False,
        "quest_item": False
    },

    "locked_chest": {
        "name": "Locked Chest",
        "description": (
            "Oak and iron, completely intact. Not a scratch on it. "
            "The sea destroyed everything else and left this. That "
            "either means it's very well made or something is very "
            "interested in what's inside. Possibly both. It needs "
            "a key you don't have."
        ),
        "obtainable": False,
        "combinable": True,
        "combines_with": "chest_key",
        "combines_into": "captains_coat",
        "single_use": True,
        "quest_item": True
    },

    "chest_key": {
        "name": "Chest Key",
        "description": (
            "Small. Iron. Hung around the navigator's neck for three "
            "hundred years. He hands it to you like he's been waiting "
            "to be asked and is relieved it's finally over. The key "
            "is cold in a way that has nothing to do with temperature."
        ),
        "obtainable": True,
        "combinable": True,
        "combines_with": "locked_chest",
        "combines_into": "captains_coat",
        "single_use": True,
        "quest_item": True
    },

    "captains_coat": {
        "name": "Captain's Coat",
        "description": (
            "Your coat. Somehow dry. Somehow pressed. The brass "
            "buttons catch the light the way they always did, and "
            "for a moment you feel like yourself again — which is "
            "either very useful or very dangerous depending on what "
            "you do next. It sits on your shoulders like a decision."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": True,
        "quest_item": False
    },

    "spyglass": {
        "name": "Spyglass",
        "description": (
            "Brass. Engraved with initials that aren't yours. "
            "Extends to three times its collapsed length and brings "
            "the horizon close enough to read. Through it, the island "
            "resolves into detail — paths you couldn't see from the "
            "ground, structures half-buried in jungle, a lighthouse "
            "you'd have walked past without knowing it was there."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": False,
        "quest_item": True
    },

    "compass_shard": {
        "name": "Compass Shard",
        "description": (
            "Half a compass, cleanly broken, the needle still "
            "somehow intact and still somehow pointing — not north. "
            "Not any direction you can name. It points with complete "
            "conviction toward something. You don't know what yet. "
            "The break is fresh, which is impossible given where "
            "you found it."
        ),
        "obtainable": True,
        "combinable": True,
        "combines_with": "compass_of_the_dead",
        "combines_into": "enhanced_compass",
        "single_use": False,
        "quest_item": True
    },

    "island_map": {
        "name": "Island Map",
        "description": (
            "Drawn on sailcloth in a child's hand — careful, serious, "
            "the way children draw things when they mean them. Every "
            "room on the island is marked, including ones that "
            "shouldn't exist from any reasonable vantage point. "
            "Some rooms are marked with an X. Some with a question "
            "mark. One is marked with a small drawing of a skull "
            "wearing a very elaborate hat."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": False,
        "quest_item": True
    },

    "tide_lantern": {
        "name": "Tide Lantern",
        "description": (
            "Glass and iron, salt-fogged, containing a flame that "
            "burns blue-white and doesn't flicker. It illuminates "
            "things that aren't there in the dark — or rather, things "
            "that are there but have learned to hide from ordinary "
            "light. It feels like an apology for something. You "
            "take it anyway."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": False,
        "quest_item": True
    },

    "sea_chart": {
        "name": "Sea Chart",
        "description": (
            "A navigational chart of the island, rendered in the "
            "precise hand of a man who spent forty years at sea "
            "before spending three hundred years dead on this beach. "
            "Every path, every room, every hidden entrance marked "
            "with the confidence of someone who mapped it on foot "
            "and checked it twice. In the margin, in smaller "
            "writing: 'Don't go to the bridge angry.'"
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": False,
        "quest_item": True
    },

    "volcanic_shard": {
        "name": "Volcanic Shard",
        "description": (
            "Dark glass, sharp on every edge except the one that "
            "somehow fits naturally against your palm. Formed in "
            "whatever event created this ridge — fast, violent, "
            "precise. It catches light like it's storing it for "
            "later. It would make an extraordinary blade if it "
            "had a handle. You look at the boarding axe in your "
            "inventory and begin to think."
        ),
        "obtainable": True,
        "combinable": True,
        "combines_with": "boarding_axe",
        "combines_into": "ashblade",
        "single_use": False,
        "quest_item": False
    },

    "ashblade": {
        "name": "Ashblade",
        "description": (
            "The volcanic shard takes to the boarding axe handle "
            "like it was designed for it — which is impossible, "
            "since one is three centuries old and the other formed "
            "in a volcanic event, but the island has stopped "
            "surprising you with impossibilities. The blade that "
            "results is dark glass edged with volcanic light, "
            "something between a sword and a statement. It hums "
            "differently than the cutlass. Lower. Angrier."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": False,
        "quest_item": False
    },

    "saltwater_salve": {
        "name": "Saltwater Salve",
        "description": (
            "A small jar of something that smells like the sea "
            "at its cleanest — before ships, before blood, before "
            "whatever this island has been doing to the water for "
            "three centuries. The witch seals it without ceremony. "
            "'One use,' she says. 'Don't waste it on something "
            "stupid.' You don't ask what counts as stupid. Her "
            "expression implies the list is longer than you'd expect."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": True,
        "quest_item": False
    },

    "ghost_rope": {
        "name": "Ghost Rope",
        "description": (
            "Looks like ordinary rope. Feels like ordinary rope. "
            "When you loop it in your hands it passes through your "
            "fingers wrong — not quite solid, obeying gravity on "
            "a slight delay. 'It binds what the living can't,' "
            "the witch says. 'And some things the living shouldn't "
            "try.' She doesn't elaborate. You've noticed she never "
            "elaborates. You've also noticed she's always right."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": True,
        "quest_item": False
    },

    "abyssal_oil": {
        "name": "Abyssal Oil",
        "description": (
            "Black. Viscous. Sealed in a vial that seems darker "
            "on the inside than the outside, which should not be "
            "geometrically possible. Applied to a blade, it makes "
            "the blade real to things that have decided they're "
            "beyond being cut. 'He'll feel that,' the witch says, "
            "and the way she says it makes clear she's looked "
            "forward to this for a while."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": True,
        "quest_item": False
    },

    "captains_logbook": {
        "name": "Captain's Logbook",
        "description": (
            "Not your logbook. Someone else's — the last captain to "
            "reach the Ruins before you. The entries grow shorter "
            "toward the end, the handwriting deteriorating not from "
            "fear but from understanding. The final entry: 'The Heart "
            "cannot be broken from the outside. You have to want to "
            "destroy it — completely, without reservation. The cutlass "
            "isn't the blade. Intent is. We didn't know until it was "
            "too late. If you find this: mean it.'"
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": False,
        "quest_item": True
    },

    "compass_of_the_dead": {
        "name": "Compass of the Dead",
        "description": (
            "Ancient — older than the island, you suspect, or at "
            "least older than whatever the island became. The needle "
            "doesn't point north. It doesn't point in any direction "
            "you can name. When you pick it up, it spins once, twice, "
            "then stops. Pointing at you. You put it in your pocket "
            "and try not to think about what that means."
        ),
        "obtainable": True,
        "combinable": True,
        "combines_with": "compass_shard",
        "combines_into": "enhanced_compass",
        "single_use": False,
        "quest_item": True
    },

    "tidemark_cutlass": {
        "name": "Tidemark Cutlass",
        "description": (
            "The moment your hand closes around the hilt it hums — "
            "low, resonant, the frequency of something recognizing "
            "something else. Tidal runes run the length of the blade, "
            "filled with bioluminescence that pulses like a slow "
            "breath. It is the most beautiful thing on this island "
            "and it has been in the wrong hands until now. It knew "
            "that. It waited."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": False,
        "quest_item": True
    },

    "heart_of_the_locker": {
        "name": "Heart of the Locker",
        "description": (
            "Obsidian, fist-sized, floating an inch above the ground. "
            "It beats. It has always been beating. Warm to the touch "
            "in a way that feels personal, like it recognizes your "
            "hand and has opinions about it. It will keep beating "
            "until something means it enough to stop. The captain's "
            "logbook said intent is the blade. You understand that "
            "now. You need to be sure."
        ),
        "obtainable": False,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": True,
        "quest_item": True
    },

    "jones_journal": {
        "name": "Davy Jones' Journal",
        "description": (
            "His handwriting is precise and small — a man who was "
            "careful with space, careful with words. The early "
            "entries are navigational, professional, unremarkable. "
            "Then there's a gap. Then the entries resume in the "
            "same hand but different — slower, like each word cost "
            "something. He writes about a choice. About what the "
            "Heart offered and what it cost and how he didn't "
            "understand the exchange rate until it was settled. "
            "The last entry is four words: 'I remember being afraid.' "
            "Below it, underlined once: 'I miss it.'"
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": False,
        "quest_item": True
    },

    "enhanced_compass": {
        "name": "Enhanced Compass",
        "description": (
            "The shard fits the broken compass like it was always "
            "meant to. The needle, whole for the first time, spins "
            "once — fast, deliberate — and settles. It no longer "
            "points at you. It points at something you can't see "
            "from here, something beyond the clifftop, something "
            "the compass has apparently known about for a very "
            "long time and has been waiting for the right moment "
            "to show you. Your hands are shaking slightly. You "
            "think that might be appropriate."
        ),
        "obtainable": True,
        "combinable": False,
        "combines_with": None,
        "combines_into": None,
        "single_use": True,
        "quest_item": True
    }
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NPCs
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

npcs = {
    "barnacle_jack": {
        "name": "Barnacle Jack",
        "type": "dialogue",
        "location": "shore",
        "condition": lambda p: not p["jack_vanished"],
        "dialogue": {
            "greeting": {
                "first_visit": (
                    "A translucent figure steps from the spray — sea-rotted, "
                    "three centuries dead, and somehow the most talkative "
                    "thing on the island. He smells inexplicably of cheese."
                ),
                "returning": (
                    "Jack materializes beside you with the casual ease of "
                    "someone who has nowhere else to be. Which is accurate."
                )
            },
            "options": {
                "1": {
                    "text": "What is this island?",
                    "response": (
                        "'Cursed rock, far as I can tell. Been here three "
                        "centuries and it hasn't gotten friendlier. The island "
                        "breathes, did you notice? Most people notice too late.'"
                    ),
                    "effects": {"jack_trust": 1},
                    "condition": None
                },
                "2": {
                    "text": "What are those creatures offshore?",
                    "response": (
                        "'The Abyssal Crown and the Six-Crowned Terror. Ancient "
                        "things. Been fighting long as anyone can remember. "
                        "Thing is — things that old don't fight without reason. "
                        "Someone's giving them one. Gerald always said: follow "
                        "the reason, not the fight. Gerald was occasionally right.'"
                    ),
                    "effects": {"jack_trust": 1},
                    "condition": None
                },
                "3": {
                    "text": "What should I do?",
                    "response": (
                        "He considers this with more seriousness than you expected. "
                        "'Find the Heart,' he says. 'Everything else is decoration.'"
                    ),
                    "effects": {"jack_trust": 1},
                    "condition": None
                },
                "4": {
                    "text": "Tell me about Gerald.",
                    "response": (
                        "'Gerald was my first mate. Bravest man I ever knew, "
                        "which is different from the smartest. Once fought a "
                        "harbour master with a wheel of cheese. Won, technically, "
                        "though the legal situation was complicated. Lovely hat. "
                        "Terrible judgment. Miss him every day.'"
                    ),
                    "effects": {},
                    "condition": None
                },
                "5": {
                    "text": "I don't have time for this.",
                    "response": (
                        "Jack's expression doesn't change. "
                        "'Everyone says that,' he says. 'Everyone.'"
                    ),
                    "effects": {"jack_trust": -1, "jack_dismissed_count": 1},
                    "condition": None
                },
                "6": {
                    "text": "What aren't you telling me?",
                    "response": (
                        "He's quiet for a moment. Longer than a ghost needs "
                        "to be quiet. 'The colossals aren't fighting each other. "
                        "They're being made to. Something beneath this island "
                        "has been pulling their strings for centuries. The Heart "
                        "of the Locker. Find it. Break it. Everything else "
                        "follows from that.'"
                    ),
                    "effects": {"jack_trust": 1},
                    "condition": lambda p: p["jack_trust"] >= 3
                },
                "7": {
                    "text": "I found the mural.",
                    "response": (
                        "He goes still in a way ghosts don't usually go still. "
                        "Follows you to the grotto without being asked. Stands "
                        "in front of the wall for a long time. 'We painted this,' "
                        "he says finally. 'I'd forgotten.' A pause. 'We thought "
                        "someone would find it sooner.' He turns to you. 'Ask me "
                        "anything. I'm done being careful.'"
                    ),
                    "effects": {"jack_trust": 2, "morality": 1},
                    "condition": lambda p: (
                        "hidden_grotto" in p["visited_rooms"] and
                        p["jack_trust"] >= 3
                    )
                }
            },
            "vanished_message": (
                "The air where Jack usually appears is empty. "
                "He has stopped coming. You dismissed him one too many times. "
                "Whatever he would have told you, he won't now."
            )
        }
    },

    "ghost_crew": {
        "name": "Ghost Crew",
        "type": "dialogue",
        "location": "ghost_camp",
        "condition": None,
        "members": {
            "old_pete": {
                "name": "Old Pete",
                "greeting": (
                    "A ghost with the weathered look of a man who spent "
                    "forty years at sea and three hundred years regretting it. "
                    "He speaks slowly, like each word costs something."
                ),
                "dialogue": {
                    "1": {
                        "text": "How long have you been here?",
                        "response": (
                            "'Three hundred and twelve years, four months, "
                            "eleven days.' He pauses. 'Give or take. The "
                            "days blur after the first century.'"
                        ),
                        "effects": {}
                    },
                    "2": {
                        "text": "What happened to your crew?",
                        "response": (
                            "'We found the Ruins. We found the Heart. We "
                            "thought destroying it would free us.' He looks "
                            "at his hands. 'We were right. We just didn't "
                            "survive the finding out.'"
                        ),
                        "effects": {"morality": 1}
                    },
                    "3": {
                        "text": "What is the Heart exactly?",
                        "response": (
                            "'A lock,' he says. 'And a key. And the door "
                            "itself. Davy Jones built it from something older "
                            "than any of us. It keeps the colossals chained "
                            "and keeps him powerful and keeps this island "
                            "breathing. Pull one thread, the whole thing unravels.'"
                        ),
                        "effects": {}
                    }
                }
            },
            "navigator": {
                "name": "The Navigator",
                "greeting": (
                    "Stands apart from the others, watching the treeline "
                    "with the focused expression of a man still doing his job "
                    "three centuries after it stopped mattering."
                ),
                "dialogue": {
                    "1": {
                        "text": "Can you help me navigate the island?",
                        "response": (
                            "'Depends.' He looks at you with the particular "
                            "judgment of someone who has watched a lot of "
                            "people make a lot of decisions. 'What have "
                            "you left behind you?'"
                        ),
                        "effects": {},
                        "condition": lambda p: p["reputation"] < 2
                    },
                    "1_unlocked": {
                        "text": "Can you help me navigate the island?",
                        "response": (
                            "He studies you for a moment, then nods once — "
                            "the nod of a man who has made a decision and "
                            "will stand by it. He produces a chart so detailed "
                            "it makes your own map look like a child's drawing. "
                            "Which it is, technically."
                        ),
                        "effects": {},
                        "gives_item": "sea_chart",
                        "condition": lambda p: p["reputation"] >= 2
                    }
                }
            },
            "laundry_ghost": {
                "name": "The Laundry Ghost",
                "greeting": (
                    "Wringing out a shirt that has been wet for three hundred "
                    "years. He glances up with the expression of a man who "
                    "has achieved a kind of peace with his circumstances."
                ),
                "dialogue": {
                    "1": {
                        "text": "What are you doing?",
                        "response": (
                            "'Laundry.' He wrings the shirt again. 'It's not "
                            "going to dry. Hasn't dried in three centuries. "
                            "I find the routine comforting.' A pause. "
                            "'There's a woman in the jungle who trades things. "
                            "East of camp. Don't let her expression put you off. "
                            "That's just her face.'"
                        ),
                        "effects": {}
                    },
                    "2": {
                        "text": "Has anyone ever left this island?",
                        "response": (
                            "He considers the shirt. 'Not that stayed gone. "
                            "The island has a way of keeping what it wants.' "
                            "He looks at you. 'You might be different. "
                            "You're still annoyed. The ones who made it "
                            "were always annoyed. The ones who weren't...' "
                            "He gestures vaguely at himself."
                        ),
                        "effects": {}
                    }
                }
            },
            "knife_ghost": {
                "name": "The Knife Ghost",
                "greeting": (
                    "Sharpening a knife that has no blade. The grinding "
                    "sound is perfect and completely convincing. He doesn't "
                    "look up when you approach."
                ),
                "dialogue": {
                    "1": {
                        "text": "What do you know about the sea cave?",
                        "response": (
                            "'Guardian's been there longer than us. "
                            "Longer than the island, some say. Took the "
                            "cutlass off the last captain who tried to pass.' "
                            "He runs a thumb along the invisible blade. "
                            "'Bring me the logbook from the hollow and "
                            "I'll tell you something useful about it.'"
                        ),
                        "effects": {}
                    },
                    "1_with_item": {
                        "text": "I found the logbook.",
                        "response": (
                            "He reads it without taking it from you, which "
                            "is a ghost thing apparently. 'The guardian tires,' "
                            "he says finally. 'Keep it moving. Keep it working. "
                            "Six turns, maybe seven. After that it slows down.' "
                            "He goes back to his knife. 'Don't thank me.'"
                        ),
                        "effects": {},
                        "condition": lambda p: "captains_logbook" in p["inventory"]
                    }
                }
            },
            "boot_ghost": {
                "name": "The Boot Ghost",
                "greeting": (
                    "Sitting with one boot on and one foot bare, "
                    "staring at the empty space where the other boot "
                    "should be with the focused misery of a man "
                    "with one real problem left."
                ),
                "dialogue": {
                    "1": {
                        "text": "What's wrong?",
                        "response": (
                            "'Lost my boot. Left one, size nine. "
                            "Been looking three hundred years.' "
                            "He looks at you with desperate hope. "
                            "'You haven't seen a boot, have you?'"
                        ),
                        "effects": {}
                    }
                }
            }
        }
    },

    "ghost_sailor": {
        "name": "The Ghost Sailor",
        "type": "dialogue",
        "location": "mangrove_maze",
        "condition": None,
        "one_time": True,
        "dialogue": {
            "greeting": (
                "He stands between two roots, not quite looking at you. "
                "Human-shaped. Patient in the way only the very dead can be. "
                "When he speaks, his voice comes from slightly the wrong direction."
            ),
            "options": {
                "1": {
                    "text": "I'm listening.",
                    "response": (
                        "He tells you his name. Then he tells you how he got "
                        "here — not the storm, not the wreck, but the choice "
                        "he made before the storm that put him in its path. "
                        "He speaks for a long time. You let him. When he's "
                        "done he reaches into nothing and produces a lantern "
                        "that burns blue-white without flickering. 'Take it,' "
                        "he says. 'It finds what hides from ordinary light.' "
                        "He looks almost relieved. 'Thank you for staying.'"
                    ),
                    "effects": {"morality": 1},
                    "gives_item": "tide_lantern",
                    "sets_flag": "ghost_sailor_named"
                },
                "2": {
                    "text": "I don't have time.",
                    "response": (
                        "He nods once, slowly, like he expected this. "
                        "Like everyone says this. He turns back to face "
                        "the roots and doesn't move again. The lantern, "
                        "wherever it was, stays wherever it is. "
                        "You walk past him. He doesn't watch you go."
                    ),
                    "effects": {"morality": -1}
                }
            }
        }
    },

    "witch": {
        "name": "The Witch",
        "type": "dialogue_and_trade",
        "location": "witch_hut",
        "condition": lambda p: p["reputation"] >= 1 or p["jack_trust"] >= 2,
        "dialogue": {
            "greeting": {
                "jack_vouched": (
                    "'Jack sent you?' She finally looks up. "
                    "'That old rot-bag.' A pause. 'Fine. Sit down. "
                    "It's a long story and you need to hear it.'"
                ),
                "default": (
                    "She doesn't look up. 'You're either very brave "
                    "or very lost.' Another moment. 'Sit down. "
                    "I'll decide which.'"
                )
            },
            "options": {
                "1": {
                    "text": "What do you know about the Heart?",
                    "response": (
                        "'Everything.' She says it the way people say "
                        "things that are simply true. 'It's a wound the "
                        "island gave itself a long time ago. Davy Jones "
                        "didn't create it — he found it. Figured out how "
                        "to live inside it. Difference between a parasite "
                        "and a host is who was there first.' She looks at "
                        "you. 'The island was there first.'"
                    ),
                    "effects": {},
                    "condition": lambda p: len(p.get("witch_trades", [])) >= 2
                },
                "2": {
                    "text": "I want to trade.",
                    "response": "trade_menu",
                    "effects": {}
                },
                "3": {
                    "text": "How do I destroy the Heart?",
                    "response": (
                        "'Someone already wrote that down. Shipwreck hollow, "
                        "propped against the mast. Read it.' She turns back "
                        "to her work. 'And mean it. That part matters more "
                        "than the cutlass.'"
                    ),
                    "effects": {},
                    "condition": lambda p: len(p.get("witch_trades", [])) >= 1
                }
            }
        },
        "trade": {
            "greeting": (
                "She looks at what you're carrying with the focused "
                "assessment of someone who has been doing this a long time."
            ),
            "rates": {
                "saltwater_salve": 2,
                "ghost_rope": 3,
                "abyssal_oil": 4
            },
            "wants": []
        }
    },

    "terror_heads": {
        "name": "The Six-Crowned Terror",
        "type": "event",
        "location": "six_crowned_shallows",
        "condition": None,
        "events": [
            {
                "trigger": "first_visit",
                "text": (
                    "Two heads surface simultaneously. They regard you "
                    "with six eyes between them.\n"
                    "Head #4: 'It's doing the thing again.'\n"
                    "Head #2: 'What thing?'\n"
                    "Head #4: 'The compassionate thing. I find it unsettling.'\n"
                    "They submerge."
                ),
                "effects": {}
            },
            {
                "trigger": "free_creature",
                "text": (
                    "Three heads surface this time.\n"
                    "Head #3: 'It freed one of ours.'\n"
                    "Head #1: 'I saw.'\n"
                    "Head #3: 'That's significant.'\n"
                    "Head #1: 'Don't read into it.'\n"
                    "Head #3: 'I'm absolutely reading into it.'"
                ),
                "effects": {"terror_allegiance": 2}
            },
            {
                "trigger": "harm_creature",
                "text": (
                    "A single head rises. Watches you. Says nothing. "
                    "Submerges slowly."
                ),
                "effects": {"terror_allegiance": -2}
            }
        ]
    },

    "kraken_hatchling": {
        "name": "Kraken Hatchling",
        "type": "event",
        "location": "abyssal_crown_reef",
        "condition": None,
        "events": [
            {
                "trigger": "free_hatchling",
                "text": (
                    "It takes effort — the rock is heavier than it looks "
                    "and the hatchling is not grateful in any visible way. "
                    "It drifts free, regards you with one enormous eye, "
                    "and descends into the deep without ceremony. "
                    "In the deep water beyond the arch, something vast "
                    "and serpentine goes still. Then continues moving. "
                    "But slower. Like it noticed."
                ),
                "effects": {"crown_allegiance": 2, "morality": 1}
            },
            {
                "trigger": "ignore_hatchling",
                "text": (
                    "The hatchling struggles. You walk past. "
                    "In the water beyond the arch, something vast "
                    "changes direction almost imperceptibly."
                ),
                "effects": {}
            },
            {
                "trigger": "harm_hatchling",
                "text": (
                    "The water beyond the arch goes completely still. "
                    "Then the temperature drops. "
                    "You walk away quickly."
                ),
                "effects": {"crown_allegiance": -3, "morality": -2}
            }
        ]
    },

    "deep_presence": {
        "name": "The Deep Presence",
        "type": "event",
        "location": "tidal_pool",
        "condition": lambda p: "tide_lantern" in p["inventory"],
        "one_time": True,
        "events": [
            {
                "trigger": "sit_and_wait",
                "text": (
                    "You sit at the edge of the pool. Nothing happens "
                    "for long enough that a lesser person would leave. "
                    "Then the presence stirs. What it shows you isn't "
                    "language and isn't image — it's understanding, "
                    "arriving fully formed: the island before the Heart, "
                    "the colossals before the chains, the sea before it "
                    "had a king. What the ocean actually is, underneath "
                    "everything that's been done to it. You sit with it "
                    "for a long time. When you stand up, something has "
                    "shifted in your chest, quiet and permanent."
                ),
                "effects": {},
                "sets_flag": "tidal_vision_seen"
            }
        ]
    },

    "cave_guardian": {
        "name": "Cave Guardian",
        "type": "combat",
        "location": "sea_cave",
        "condition": lambda p: not p["guardian_defeated"],
        "combat_stats": {
            "health": 80,
            "health_max": 80,
            "stamina": 60,
            "attack_power": 15,
            "ai_type": "brute",
            "phase": 1,
            "tiredness": 0
        },
        "abilities": {
            "crush": {
                "damage": 15,
                "description": (
                    "The guardian brings two arms down simultaneously. "
                    "The cave floor cracks where you were standing."
                ),
                "weight": 60
            },
            "slam": {
                "damage": 25,
                "description": (
                    "A single massive arm sweeps across the cave. "
                    "The kind of blow that ends arguments."
                ),
                "weight": 30
            },
            "throw": {
                "damage": 15,
                "description": (
                    "It hurls you into the cave wall. "
                    "The cave wall has opinions about this."
                ),
                "applies_effect": "Drowned",
                "weight": 10
            }
        },
        "dialogue": {
            "combat_start": (
                "It doesn't roar. It doesn't posture. "
                "It simply turns toward you with the calm "
                "of something that has never lost."
            ),
            "player_parry": (
                "The guardian pauses — something new "
                "has happened. It recalibrates."
            ),
            "tiring": (
                "Its movements are slower now. Three centuries "
                "of waiting and one prolonged fight — even "
                "ancient things tire eventually."
            ),
            "defeated": (
                "It sinks to one knee. The cutlass falls. "
                "You catch it before it hits the water. "
                "The moment your hand closes around the hilt "
                "it hums — low, resonant, recognizing something."
            )
        },
        "loot": ["tidemark_cutlass"],
        "conditional_loot": {
            "item": "compass_of_the_dead",
            "condition": lambda p: "tide_lantern" in p["inventory"]
        }
    },

    "davy_jones": {
        "name": "Davy Jones",
        "type": "combat",
        "location": "the_ruins",
        "condition": None,
        "combat_stats": {
            "health": 120,
            "health_max": 120,
            "stamina": 999,
            "attack_power": 20,
            "ai_type": "manipulator",
            "phase": 1
        },
        "abilities": {
            "theatrical_strike": {
                "damage": 30,
                "description": (
                    "He moves like punctuation — deliberate, "
                    "perfectly placed, impossible to misread."
                ),
                "weight": 30
            },
            "drain_stamina": {
                "damage": 0,
                "stamina_drain": 20,
                "description": (
                    "'Tired already?' He tilts his head. "
                    "'We've barely started.'"
                ),
                "weight": 30
            },
            "taunt": {
                "damage": 0,
                "stamina_drain": 15,
                "description": "Jones delivers a theatrical monologue.",
                "weight": 20
            },
            "standard": {
                "damage": 20,
                "description": (
                    "A precise strike. Nothing wasted. "
                    "He doesn't fight like a monster. "
                    "He fights like a man who has had centuries to practice."
                ),
                "weight": 20
            },
            "heal": {
                "damage": 0,
                "heal_amount": 10,
                "description": (
                    "The wound closes. Black water retreats "
                    "back into his coat like it was never there."
                ),
                "condition": lambda p: not p["heart_destroyed"]
            }
        },
        "taunt_lines": [
            "'You're doing remarkably well for someone who arrived clinging to a hat.'",
            "'You mistake pain for weakness. I mistake nothing. I simply enjoy the theatre.'",
            "'Everyone who has stood where you're standing has been very determined. Very.'",
            "'The Heart still beats. Can you feel it? I can always feel it.'",
            "'Gerald, was it? Jack mentioned him. Sounded like a cautionary tale.'"
        ],
        "finisher_response": (
            "For the first time, something crosses his face "
            "that isn't composure. He looks, briefly, impressed. "
            "'Well,' he says. 'Well.'"
        ),
        "dialogue": {
            "combat_start": (
                "He steps from the shadow between one moment and the next. "
                "Immaculate. Composed. He straightens his coat before "
                "speaking, which somehow makes it worse. "
                "'You've done remarkably well for someone who washed "
                "ashore clinging to a hat.'"
            ),
            "heart_intact": (
                "The wound closes before it finishes opening. "
                "He doesn't even look down. "
                "'You mistake pain for weakness,' he says. "
                "'The Heart still beats. So do I.'"
            ),
            "heart_destroyed": (
                "The wound stays open. Black water spills. "
                "He looks at it with something that might be surprise "
                "if he were capable of surprise. "
                "He isn't. But he looks at it anyway."
            ),
            "journals_unlocked": (
                "He goes still. Not the careful stillness of control — "
                "something else. Something the coat and the composure "
                "weren't built for. 'Did you,' he says. Not a question. "
                "'Then you know what the Heart cost.' Another silence. "
                "'It cost more than I was told it would.' He looks at "
                "the floor where the Heart pulses. 'It always does.'"
            ),
            "defeated": (
                "He dissolves — slowly, with a kind of dignity, "
                "the black rain of him pattering against the coral floor. "
                "His last words, delivered with complete sincerity: "
                "'Magnificent. Truly. You should have seen yourself.'"
            )
        },
        "loot": []
    },

    "sovereign": {
        "name": "The Sovereign of All Drowned Fears",
        "type": "combat",
        "location": "clifftop",
        "condition": lambda p: p["heart_destroyed"],
        "combat_stats": {
            "health": 200,
            "health_max": 200,
            "stamina": 999,
            "attack_power": 25,
            "ai_type": "multi_phase",
            "phase": 1
        },
        "phase_transitions": {
            "phase_2": {
                "health_threshold": 140,
                "description": (
                    "The Sovereign sheds its outer form like a coat. "
                    "The heads retract. The body elongates. "
                    "The storm that has been circling the island "
                    "moves inward and becomes part of it."
                )
            },
            "phase_3": {
                "health_threshold": 60,
                "description": (
                    "Something at the Sovereign's center cracks open — "
                    "a core of abyssal light, dark the way only things "
                    "that have never seen the sun are dark. "
                    "You know what to do."
                )
            }
        },
        "abilities": {
            "phase_1": {
                "head_bite": {
                    "damage": 20,
                    "weight": 40,
                    "descriptions": [
                        "Head #1 strikes with the speed of something that was never slow.",
                        "Head #2 comes from the left. You were watching the right.",
                        "Head #3 bites and misses and seems annoyed about it.",
                        "Head #4 and #5 strike together. One connects.",
                        "Head #6 — the quiet one — finally moves."
                    ]
                },
                "tail_whip": {
                    "damage": 15,
                    "weight": 30,
                    "applies_effect": "Drowned",
                    "description": (
                        "The leviathan tail sweeps the clifftop. "
                        "The stone cracks where it passes."
                    )
                },
                "six_snap": {
                    "damage": 10,
                    "weight": 30,
                    "description": (
                        "All six heads strike simultaneously from "
                        "different directions. Hard to dodge. "
                        "Head #3 aims for your hat specifically."
                    )
                }
            },
            "phase_2": {
                "abyssal_storm": {
                    "damage": 25,
                    "weight": 40,
                    "applies_effect": "Terrified",
                    "description": (
                        "The storm closes in. Lightning that isn't lightning "
                        "strikes everywhere at once."
                    )
                },
                "crushing_wave": {
                    "damage": 30,
                    "weight": 35,
                    "resets_momentum": True,
                    "description": (
                        "A wall of water that shouldn't exist this high "
                        "above sea level crashes across the clifftop."
                    )
                },
                "tentacle_sweep": {
                    "damage": 20,
                    "weight": 25,
                    "applies_effect": "Bleeding",
                    "description": (
                        "Kraken arms the size of ship masts sweep "
                        "across the stone."
                    )
                }
            },
            "phase_3": {
                "core_pulse": {
                    "damage": 35,
                    "weight": 40,
                    "applies_effect": "Saltbound",
                    "description": (
                        "The core pulses outward. "
                        "Everything within reach becomes briefly wrong."
                    )
                },
                "reform": {
                    "damage": 0,
                    "heal_amount": 20,
                    "weight": 60,
                    "description": (
                        "The core begins to seal itself. "
                        "The wound closes from the inside. "
                        "Strike harder."
                    ),
                    "condition": "player_did_not_use_heavy"
                }
            }
        },
        "dialogue": {
            "combat_start": (
                "The ocean tears open. He rises without hurry, "
                "without drama — the drama is structural, built into "
                "what he is. Every monster. Every terror. Every nightmare "
                "assembled into one sovereign form."
            ),
            "phase_2_start": (
                "The Sovereign sheds its outer form. "
                "The storm moves inward. "
                "Behind you, the Abyssal Crown and the Six-Crowned Terror "
                "surface. Whether they're with you depends entirely "
                "on what you've done until now."
            ),
            "phase_3_start": (
                "The abyssal core is visible. "
                "Dark the way only things that have never seen sun are dark. "
                "You know what this means. Do it before it seals."
            ),
            "head_3_commentary": [
                "Head #3, mid-battle: 'I told you. LEFT.'",
                "Head #3, after a player dodge: 'Hm. Respect.'",
                "Head #3, taking damage: 'That one was fair.'",
                "Head #3, during phase transition: 'This is fine. This is fine.'"
            ],
            "defeated": (
                "The Sovereign fractures from the core outward — "
                "slow, like a decision being unmade. "
                "Davy Jones, somewhere inside all of it, "
                "dissolves into salt and black rain. "
                "Silence falls across the sea.\n\n"
                "Barnacle Jack appears. Grave, for once.\n\n"
                "'Chains ain't always cages, lad. "
                "Sometimes they're anchors.'\n\n"
                "He pauses.\n\n"
                "'Gerald would've cried. "
                "Would've embarrassed us all.'\n\n"
                "Another pause.\n\n"
                "'I miss him.'"
            )
        },
        "loot": []
    }
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UTILITY FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def print_slow(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def wrap(text):
    return textwrap.fill(text, width=70)


def print_wrapped(text, slow=False):
    formatted = wrap(text)
    if slow:
        print_slow(formatted)
    else:
        print(formatted)


def divider():
    print("\n" + "─" * 70 + "\n")


def apply_effects(effects):
    """Apply a dict of stat changes to the player."""
    for key, value in effects.items():
        if key in player:
            player[key] += value


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TITLE SEQUENCE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def title_sequence():
    clear_screen()
    time.sleep(0.3)

    # ── ASCII art compass ─────────────────────────────────────────
    compass = [
        "                        *   ",
        "                        |   ",
        "                     N  |   ",
        "              . · ·  ·  |  · · . · .",
        "           ·              |              ·",
        "         ·         . · . | . · .          ·",
        "        ·       ·        |        ·         ·",
        "       ·      ·     ╔════╧════╗     ·        ·",
        "      ·      ·      ║ ╲     ╱ ║      ·        ·",
        "   W ——·——·——·——·—— ║  ╲▲ ▼╱  ║ ——·——·——·——·—— E",
        "      ·      ·      ║  ▼╱ ╲▲  ║      ·        ·",
        "       ·      ·     ╚════╤════╝     ·        ·",
        "        ·       ·        |        ·         ·",
        "         ·         · · · | · · ·          ·",
        "           ·              |              ·",
        "              · · ·  ·   |  · · · ",
        "                      S  |   ",
        "                         |   ",
        "                             ",
    ]

    # Print compass slowly line by line
    for line in compass:
        print(line)
        time.sleep(0.04)

    time.sleep(0.4)
    print()

    # ── Title block ───────────────────────────────────────────────
    title_lines = [
        r"  _   _ _   _  ____ _   _    _    ___ _   _ _____ ____  ",
        r" | | | | \ | |/ ___| | | |  / \  |_ _| \ | | ____|  _ \ ",
        r" | | | |  \| | |   | |_| | / _ \  | ||  \| |  _| | | | |",
        r" | |_| | |\  | |___|  _  |/ ___ \ | || |\  | |___| |_| |",
        r"  \___/|_| \_|\____|_| |_/_/   \_\___|_| \_|_____|____/ ",
    ]

    for line in title_lines:
        print(line)
        time.sleep(0.06)

    time.sleep(0.3)
    print()
    print("          T H E   C U R S E   O F   T H E   S U N K E N   C O M P A S S")
    print()
    print("  ─────────────────────────────────────────────────────────────────────")
    time.sleep(1)

    # ── Opening lines ─────────────────────────────────────────────
    print()
    opening = [
        "  Your ship dies screaming.",
        "  Black waves split the hull.",
        "  Two colossal shapes clash in the dark beyond the storm.",
        "  You wash ashore alone.",
        "",
        "  The island watches.",
        "  It has seen this before.",
        "  It is patient.",
    ]
    for line in opening:
        print_slow(line, delay=0.025)
        time.sleep(0.15)

    time.sleep(0.8)
    print()
    print("  ─────────────────────────────────────────────────────────────────────")
    print()
    print("  Commands: go  look  take  drop  use  combine  talk  inventory  map")
    print()
    print("  Type  help  at any time for the full command list.")
    print()
    input("  Press Enter to begin...")
    clear_screen()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHOW ROOM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def show_room():
    clear_screen()

    current_room_id = player.get("current_room")
    room = rooms.get(current_room_id)
    if not room:
        print(f"Error: Room '{current_room_id}' not found.")
        return

    room_name = current_room_id.replace("_", " ").title()

    divider()
    print(room_name.upper())
    divider()
    print("")
    print_wrapped(room["description"])
    print("")

    # Exits
    exit_list = list(room["exits"].keys())
    if exit_list:
        print("Exits: " + ", ".join(exit_list))
    else:
        print("Exits: none")

    # Items on ground
    if room["items"]:
        item_names = [items[k]["name"] for k in room["items"] if k in items]
        if item_names:
            print("")
            print("You see: " + ", ".join(item_names))

    # NPC present
    if room["npc"]:
        npc = npcs.get(room["npc"])
        if npc:
            # Check npc condition
            condition = npc.get("condition")
            if condition is None or condition(player):
                print("")
                print(npc["name"] + " is here.")

    # Environment actions (combat rooms only)
    if room["combat_room"] and room["environment_actions"]:
        print("")
        print("Environment: " + ", ".join(room["environment_actions"]))

    # Status bar
    print("")
    print(f"HP: {player['health']}/{player['max_health']}  "
          f"Stamina: {player['stamina']}/{player['max_stamina']}  "
          f"Turn: {player['turn_count']}")

    divider()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT & COMMAND ROUTING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_input():
    print("> ", end="")
    raw = input().strip().lower()
    parts = raw.split(" ", 1)
    command = parts[0]
    target = parts[1] if len(parts) > 1 else ""
    return command, target


def resolve_command(command, target):
    if command == "go":
        move_player(target)
    elif command in ("look", "l", "examine", "x"):
        cmd_look(target)
    elif command in ("take", "get", "pick"):
        cmd_take(target)
    elif command == "drop":
        cmd_drop(target)
    elif command in ("inventory", "i", "inv"):
        cmd_inventory()
    elif command == "combine":
        cmd_combine(target)
    elif command in ("talk", "speak"):
        cmd_talk(target)
    elif command == "use":
        cmd_use(target)
    elif command in ("map", "m"):
        cmd_map()
    elif command == "help":
        cmd_help()
    elif command in ("quit", "exit", "q"):
        cmd_quit()
    elif command in ("fight", "attack", "engage", "battle"):
        room = rooms[player["current_room"]]
        if room.get("combat_room") and room.get("npc"):
            npc = npcs.get(room["npc"])
            if npc and npc.get("type") == "combat":
                condition = npc.get("condition")
                if condition is None or condition(player):
                    enter_combat(room["npc"])
                    return
        print_wrapped("There is nothing to fight here.")
    elif command == "":
        pass
    else:
        print_wrapped("The wind swallows your words. Try again.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MOVEMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def unlock_condition_met(room_key):
    """Returns True if player can access a hidden room."""
    if room_key == "tidal_pool":
        return "tide_lantern" in player["inventory"]
    if room_key == "witch_hut":
        return player["reputation"] >= 1 or player["jack_trust"] >= 2
    if room_key in ("hidden_grotto", "sunken_crypt"):
        return (
            "island_map" in player["inventory"] or
            "tide_lantern" in player["inventory"]
        )
    # These are marked hidden in the data but intentionally
    # have no access restriction — open by design
    return True





def move_player(direction):
    if not direction:
        print_wrapped("Go where? Try: go north, go south, go east, go west.")
        return

    room = rooms[player["current_room"]]

    if direction not in room["exits"]:
        print_wrapped("The sea offers no path that way.")
        return

    target_key = room["exits"][direction]
    target_room = rooms[target_key]

    # Hidden room check
    if target_room["hidden"] and not unlock_condition_met(target_key):
        print_wrapped("You find nothing that way.")
        return

    # Special room checks
    if target_key == "bone_bridge":
        if not bridge_crossing_safe():
            return

    # Move the player
    player["current_room"] = target_key
    player["turn_count"] += 1

    # First visit trigger
    first_visit = target_key not in player["visited_rooms"]
    if first_visit:
        player["visited_rooms"].append(target_key)

    show_room()

    if first_visit:
        trigger_room_event(target_key)

    check_room_combat()


def bridge_crossing_safe():
    """Returns True if bridge crossing is safe, handles permadeath."""
    if "ghost_rope" in player["inventory"]:
        print_wrapped(
            "You secure yourself with the ghost rope before crossing. "
            "The bridge groans but holds."
        )
        return True
    if player["crown_allegiance"] >= 2:
        print_wrapped(
            "Below the bridge, something vast stabilizes the bones "
            "from beneath. You cross without incident."
        )
        return True
    # Risky crossing
    print_wrapped(
        "The bridge sways. You step carefully. Each bone shifts "
        "under your weight. Halfway across, a section gives way."
    )
    time.sleep(1)
    if "captains_coat" in player["inventory"] and player["coat_worn"]:
        print_wrapped(
            "The coat snags on a bone spur — an impossible catch "
            "that shouldn't have held. It tears. But you don't fall."
        )
        player["inventory"].remove("captains_coat")
        player["coat_worn"] = False
        print_wrapped("The captain's coat is gone. But you're alive.")
        return True
    # Death
    player_death("bone_bridge")
    return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXPLORATION COMMANDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def normalize(text):
    """Strip apostrophes, lowercase, underscores — for fuzzy matching.
    Means "captain's logbook", "captains logbook", "captains_logbook"
    all resolve to the same thing."""
    return text.lower().replace("'", "").replace(" ", "_")


def item_match(target, key_list):
    """Find best matching item key from a list given user input string.
    Handles apostrophes, case, partial names, and word subsets.
    
    Match priority:
    1. Exact match after normalization
    2. Normalized target is substring of normalized key
    3. All significant words of target appear in key
    4. Any single long word (4+ chars) of target appears in key
    """
    norm = normalize(target)
    words = [w for w in norm.split("_") if len(w) > 2]

    # 1. Exact match
    for k in key_list:
        if normalize(k) == norm:
            return k

    # 2. Substring match (whole phrase)
    for k in key_list:
        if norm in normalize(k):
            return k

    # 3. All significant words present in key
    if len(words) >= 2:
        for k in key_list:
            norm_k = normalize(k)
            if all(w in norm_k for w in words):
                return k
        # Majority match: most words match (handles "Davy Jones' Journal"
        # where "davy" is not in "jones_journal" but "jones"+"journal" are)
        if len(words) >= 2:
            for k in key_list:
                norm_k = normalize(k)
                matched = sum(1 for w in words if w in norm_k)
                if matched >= max(1, len(words) - 1):
                    return k

    # 4. Single keyword — only if target is one meaningful word
    #    (avoids "locked chest" -> "chest_key" false match)
    if len(words) == 1 and len(words[0]) > 3:
        for k in key_list:
            if words[0] in normalize(k):
                return k

    return None


def cmd_look(target):
    if not target:
        show_room()
        return

    room = rooms[player["current_room"]]

    # Look at item in room
    key = item_match(target, room["items"])
    if key:
        print("")
        print_wrapped(items[key]["description"])
        return

    # Look at item in inventory
    key = item_match(target, player["inventory"])
    if key:
        print("")
        print_wrapped(items[key]["description"])
        return

    # Look at NPC
    if room["npc"]:
        npc = npcs.get(room["npc"])
        if npc and normalize(target) in normalize(npc["name"]):
            if npc["type"] == "dialogue" and "dialogue" in npc:
                greeting = npc["dialogue"]["greeting"]
                if isinstance(greeting, dict):
                    if room["npc"] in player["visited_rooms"]:
                        print_wrapped(greeting.get("returning", ""))
                    else:
                        print_wrapped(greeting.get("first_visit", ""))
                else:
                    print_wrapped(greeting)
            return

    print_wrapped("You don't see that here.")


def cmd_take(target):
    if not target:
        print_wrapped("Take what?")
        return

    room = rooms[player["current_room"]]
    key = item_match(target, room["items"])

    if not key:
        print_wrapped("There's nothing like that here.")
        return

    if not items[key]["obtainable"]:
        print_wrapped("You can't take that.")
        return

    room["items"].remove(key)
    player["inventory"].append(key)
    print("")
    print("Taken: " + items[key]["name"])

    # Flag: captains logbook sets the "I know what intent means" flag
    if key == "captains_logbook":
        player["captains_logbook_read"] = True

    # Flag: picking up Jones journal
    if key == "jones_journal":
        player["jones_knows_journals"] = True
        print("")
        print_wrapped(
            "You read it here, standing in the crypt. "
            "You understand something now that you didn't before."
        )


def cmd_drop(target):
    if not target:
        print_wrapped("Drop what?")
        return

    key = item_match(target, player["inventory"])

    if not key:
        print_wrapped("You're not carrying that.")
        return

    player["inventory"].remove(key)
    rooms[player["current_room"]]["items"].append(key)
    print("Dropped: " + items[key]["name"])


def cmd_inventory():
    print("")
    if not player["inventory"]:
        print_wrapped("You carry nothing but your fury.")
        return

    print("You are carrying:")
    for key in player["inventory"]:
        if key in items:
            print("  - " + items[key]["name"])
    print("")


def cmd_combine(target):
    parts = target.split(" and ")
    if len(parts) != 2:
        print_wrapped(
            "Combine what with what? "
            "Try: combine boarding axe and volcanic shard"
        )
        return

    raw_a = parts[0].strip()
    raw_b = parts[1].strip()
    key_a = raw_a.replace(" ", "_")
    key_b = raw_b.replace(" ", "_")

    # Fuzzy match — handles apostrophes and partial names
    # Also checks room items for non-obtainable items (e.g. locked_chest)
    room_items = rooms[player["current_room"]]["items"]

    if key_a not in player["inventory"]:
        key_a = item_match(raw_a, player["inventory"])
        if not key_a:
            # Try room items (non-obtainable interactables)
            key_a = item_match(raw_a, room_items)
            if not key_a:
                print_wrapped(f"You're not carrying the {raw_a}.")
                return

    if key_b not in player["inventory"]:
        key_b = item_match(raw_b, player["inventory"])
        if not key_b:
            # Try room items
            key_b = item_match(raw_b, room_items)
            if not key_b:
                print_wrapped(f"You're not carrying the {raw_b}.")
                return

    item_a = items.get(key_a)
    item_b = items.get(key_b)

    # Check both directions
    result_key = None
    if item_a and item_a["combinable"] and item_a["combines_with"] == key_b:
        result_key = item_a["combines_into"]
    elif item_b and item_b["combinable"] and item_b["combines_with"] == key_a:
        result_key = item_b["combines_into"]

    if result_key:
        # Remove from inventory or room (locked_chest stays in room)
        room = rooms[player["current_room"]]
        for k in (key_a, key_b):
            if k in player["inventory"]:
                player["inventory"].remove(k)
            elif k in room["items"] and not items[k]["obtainable"]:
                room["items"].remove(k)
        player["inventory"].append(result_key)
        print("")
        print_wrapped(items[result_key]["description"])
        return

    print_wrapped("Those don't combine into anything.")


def cmd_use(target):
    if not target:
        print_wrapped("Use what?")
        return

    key = item_match(target, player["inventory"])
    current = player["current_room"]

    # Special case: heart_of_the_locker cannot be picked up but can be invoked
    if not key:
        if current == "the_ruins" and any(
            w in target for w in ("heart", "invoke", "destroy", "locker")
        ):
            if "heart_of_the_locker" in rooms["the_ruins"]["items"]:
                cmd_invoke_heart()
                return
        print_wrapped("You're not carrying that.")
        return

    # Captain's coat
    if key == "captains_coat":
        if player["coat_worn"]:
            print_wrapped("You're already wearing it.")
        else:
            player["coat_worn"] = True
            player["reputation"] += 1
            print_wrapped(
                "You put on the coat. Something settles in your posture. "
                "The island notices."
            )
        return

    # Spyglass
    if key == "spyglass":
        if current == "ruined_lighthouse":
            player["lighthouse_signaled"] = True
            print_wrapped(
                "Through the mirror array and the spyglass both, you aim "
                "a flash of reflected light toward the open sea. "
                "Someone out there will see it. Whether they come in time "
                "is another matter."
            )
        elif current == "crows_perch":
            print_wrapped(
                "Through the glass: the island resolves into clarity. "
                "You can see two hidden structures you'd have missed — "
                "one north of the ridge, one east of the ruins. "
                "The map in your mind updates."
            )
            # Hint toward hidden_grotto and sunken_crypt
        else:
            print_wrapped(
                "You extend the spyglass. The horizon comes close. "
                "Nothing you didn't already know — but the island looks "
                "different from inside it than it did from the water."
            )
        return

    # Island map
    if key == "island_map":
        print_wrapped(
            "The child's drawing shows every room, including several "
            "marked with question marks. One is north of the volcanic "
            "ridge. One is east of the ruins. Both require something "
            "to see by — or the map itself to find."
        )
        return

    # Saltwater salve — used in combat only
    if key == "saltwater_salve":
        if player["in_combat"]:
            heal_amount = min(40, player["max_health"] - player["health"])
            player["health"] += heal_amount
            player["inventory"].remove(key)
            print_wrapped(
                f"You apply the salve. The wounds close. "
                f"+{heal_amount} health."
            )
        else:
            print_wrapped(
                "You're not hurt badly enough to waste this. "
                "Save it for when you need it."
            )
        return

    # Abyssal oil
    if key == "abyssal_oil":
        if "tidemark_cutlass" in player["inventory"]:
            player["inventory"].remove(key)
            # Mark cutlass as oiled via a flag
            player["cutlass_oiled"] = True if "cutlass_oiled" not in player else player.get("cutlass_oiled", False)
            player["cutlass_oiled"] = True
            print_wrapped(
                "You coat the cutlass in abyssal oil. The blade darkens. "
                "It will feel real to things that have decided they're "
                "beyond being cut."
            )
        else:
            print_wrapped(
                "You need a blade to apply this to. "
                "The cutlass, specifically."
            )
        return

    # Compass of the dead / enhanced compass
    if key in ("compass_of_the_dead", "enhanced_compass"):
        if current == "clifftop":
            print_wrapped(
                "The compass spins in your hand. "
                "This is where it was always pointing."
            )
            # Final choice will be triggered by game state
        elif current == "tidal_pool" and not player["tidal_vision_seen"]:
            player["tidal_vision_seen"] = True
            print("")
            print_slow("The compass pulls you toward the water's edge.")
            time.sleep(0.5)
            print_wrapped(
                "You sit at the edge of the pool. The presence stirs. "
                "What it shows you isn't language and isn't image — "
                "it's understanding, arriving fully formed: the island "
                "before the Heart, the colossals before the chains, "
                "the sea before it had a king. You sit with it for a "
                "long time. When you stand up, something has shifted "
                "in your chest, quiet and permanent."
            )
        else:
            print_wrapped(
                "The needle spins. Then steadies. "
                "Pointing somewhere ahead. Not yet."
            )
        return

    # Tide lantern
    if key == "tide_lantern":
        if current == "sea_cave":
            print_wrapped(
                "The lantern's blue-white flame catches something at the "
                "cave's back wall — a chamber behind the waterfall, "
                "hidden from ordinary light. Inside: a compass, ancient, "
                "its needle spinning."
            )
            if "compass_of_the_dead" not in player["inventory"]:
                player["inventory"].append("compass_of_the_dead")
                print_wrapped("You take the Compass of the Dead.")
        else:
            print_wrapped(
                "The blue-white flame illuminates things that hide from "
                "ordinary light. Edges of hidden doors. Paths not visible "
                "in daylight. The island has more rooms than it shows."
            )
        return

    # Heart of the Locker — can only be destroyed post-Jones
    if key == "heart_of_the_locker":
        if player["current_room"] != "the_ruins":
            print_wrapped(
                "The Heart isn't here. "
                "It rests in the Ruins, where it has always rested."
            )
            return
        if not player["jones_confronted"]:
            print_wrapped(
                "The Heart pushes back — Jones is still bound to it. "
                "Defeat him first."
            )
            return
        if not player.get("heart_weakened") and not player.get("altar_overturned"):
            print_wrapped(
                "You reach for it. Something holds you back. "
                "The altar — overturn it first. Weaken the connection."
            )
            return
        if "captains_logbook" not in player["inventory"]:
            print_wrapped(
                "You reach for it. A doubt stops your hand. "
                "Find the captain's logbook. Read what they left you. "
                "Then come back and mean it."
            )
            return
        # Destruction sequence
        clear_screen()
        divider()
        print("  HEART OF THE LOCKER")
        divider()
        print("")
        print_wrapped(
            "Obsidian. Floating an inch above the ground. Still beating. "
            "It has always been beating."
        )
        print("")
        print_wrapped(
            "The captain's logbook said: intent is the blade. "
            "Not the cutlass. Not the ashblade. "
            "You have to mean it. Completely. Without reservation."
        )
        print("")
        print("Do you mean it? [y/n] > ", end="")
        choice = input().strip().lower()
        if choice != "y":
            print_wrapped(
                "Your hands open. You step back. "
                "The Heart continues to beat. It will wait."
            )
            return
        print("")
        print_slow("You close your hands around the Heart.")
        time.sleep(1)
        print_slow("It beats against your palms.")
        time.sleep(1)
        print_slow("Once.")
        time.sleep(0.8)
        print_slow("Twice.")
        time.sleep(0.8)
        print_slow("You mean it.")
        time.sleep(1.2)
        print_slow("The beat stops.")
        time.sleep(2)
        print("")
        print_wrapped(
            "The silence that follows is the loudest thing you've ever heard. "
            "The floor cracks. The coral walls fracture. "
            "Something beneath the island screams — not in pain, "
            "but in release, like a held breath finally let go."
        )
        time.sleep(1)
        print_wrapped(
            "The Heart dissolves. Black water. Salt. Then nothing."
        )
        time.sleep(1)
        print_wrapped(
            "The island shudders. The colossals go still offshore. "
            "Far above, on the clifftop, the sea tears open."
        )
        player["heart_destroyed"] = True
        player["morality"] += 2
        player["reputation"] += 2
        if "heart_of_the_locker" in player["inventory"]:
            player["inventory"].remove("heart_of_the_locker")
        if "heart_of_the_locker" in rooms["the_ruins"]["items"]:
            rooms["the_ruins"]["items"].remove("heart_of_the_locker")
        print("")
        print_wrapped(
            "The passage to the clifftop is open. "
            "Something is waiting for you there."
        )
        time.sleep(1)
        input("\nPress Enter to continue...")
        show_room()
        return

    print_wrapped(
        f"You're not sure how to use the "
        f"{items[key]['name']} here."
    )

def cmd_invoke_heart():
    """Invoke / destroy the Heart of the Locker from the ruins floor."""
    if player["current_room"] != "the_ruins":
        print_wrapped("The Heart is not here.")
        return

    if player["heart_destroyed"]:
        print_wrapped(
            "The Heart is already destroyed. "
            "Its absence is its own presence."
        )
        return

    if not player["heart_weakened"] and not player.get("altar_overturned"):
        print_wrapped(
            "The Heart pulses back against your intent. "
            "It is too strong. Overturn the altar first."
        )
        return

    if not ("tidemark_cutlass" in player["inventory"] or
            "ashblade" in player["inventory"]):
        print_wrapped(
            "You need a blade that knows what it's cutting. "
            "The boarding axe won't do."
        )
        return

    # Requires the captain's logbook knowledge — intent matters
    if not player.get("captains_logbook_read") and        "captains_logbook" not in player["inventory"]:
        print_wrapped(
            "You reach for it. The Heart pulses back. "
            "It knows you're not sure. "
            "Find out what you need to know first."
        )
        return

    print("")
    print_slow("You reach into the Heart's pulse.")
    time.sleep(0.5)
    print_slow("You mean it.")
    time.sleep(0.5)

    dmg_self = random.randint(15, 25)
    player["health"] = max(1, player["health"] - dmg_self)
    player["heart_destroyed"] = True
    player["heart_weakened"] = True

    rooms["the_ruins"]["items"].remove("heart_of_the_locker")

    print("")
    print_wrapped(
        "The Heart of the Locker shatters. "
        "Not like glass — like a decision being unmade. "
        "The ruins shudder. Something beneath the island goes quiet "
        "for the first time in three hundred years. "
        f"You take {dmg_self} damage from the backlash."
    )
    time.sleep(1)
    print("")
    print_wrapped(
        "The floor cracks. The ruins begin to shake. "
        "There is only one place left to go."
    )
    gain_momentum(5)




def cmd_map():
    print("")
    if not player["visited_rooms"]:
        print_wrapped("You haven't explored enough to map anything.")
        return

    print("Visited locations:")
    for room_key in player["visited_rooms"]:
        marker = ">" if room_key == player["current_room"] else " "
        print(f"  {marker} {room_key.replace('_', ' ').title()}")
    print("")


def cmd_help():
    print("")
    print("─" * 70)
    print("  COMMANDS")
    print("─" * 70)
    print("  go [direction]        move north, south, east, or west")
    print("  look                  examine your surroundings")
    print("  look [item/npc]       examine something specific")
    print("  take [item]           pick up an item")
    print("  drop [item]           drop an item")
    print("  use [item]            use an item")
    print("  combine [a] and [b]   combine two items")
    print("  talk                  speak to whoever is here")
    print("  inventory / i         list carried items")
    print("  map                   show visited rooms")
    print("  help                  show this list")
    print("  quit                  end the game")
    print("─" * 70)
    print("")


def cmd_quit():
    print("")
    print_slow("The sea takes you. Coward.")
    time.sleep(1)
    sys.exit()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DIALOGUE SYSTEM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cmd_talk(target):
    room = rooms[player["current_room"]]

    if not room["npc"]:
        print_wrapped("There's no one here to talk to.")
        return

    npc_key = room["npc"]
    npc = npcs.get(npc_key)
    if not npc:
        print_wrapped("There's no one here.")
        return

    # Check NPC condition
    condition = npc.get("condition")
    if condition and not condition(player):
        if npc_key == "barnacle_jack":
            print_wrapped(npc["dialogue"]["vanished_message"])
        else:
            print_wrapped("There's no one here.")
        return

    npc_type = npc.get("type")

    if npc_type == "dialogue":
        talk_dialogue_npc(npc_key, npc)
    elif npc_type == "dialogue_and_trade":
        talk_witch(npc)
    elif npc_type == "event":
        talk_event_npc(npc_key, npc)
    elif npc_type == "combat":
        print_wrapped(
            npc["dialogue"]["combat_start"]
        )
        print_wrapped("You'll need to fight your way through this.")
    else:
        print_wrapped("They don't respond.")


def talk_dialogue_npc(npc_key, npc):
    # Ghost crew has members, not a dialogue key — handle first
    if npc_key == "ghost_crew":
        print_wrapped(
            "The dead carry on around you. Several are willing to talk."
        )
        talk_ghost_crew(npc)
        return

    # Ghost sailor — one time event
    if npc.get("one_time") and player.get("ghost_sailor_named"):
        print_wrapped("He has already told you everything he had to say.")
        return

    dialogue = npc["dialogue"]

    # Greeting
    greeting = dialogue.get("greeting", "")
    if isinstance(greeting, dict):
        if player["current_room"] in player["visited_rooms"] and \
           player["visited_rooms"].index(player["current_room"]) < len(player["visited_rooms"]) - 1:
            print_wrapped(greeting.get("returning", ""))
        else:
            print_wrapped(greeting.get("first_visit", ""))
    elif greeting:
        print_wrapped(greeting)

    # Options
    options = dialogue.get("options", {})
    if not options:
        return

    while True:
        print("")
        available = []
        for opt_key, opt in options.items():
            cond = opt.get("condition")
            if cond is None or cond(player):
                available.append((opt_key, opt))

        if not available:
            print_wrapped("There's nothing more to ask.")
            break

        for opt_key, opt in available:
            print(f"  [{opt_key}] {opt['text']}")
        print("  [0] Leave")
        print("")
        print("> ", end="")
        choice = input().strip()

        if choice == "0":
            break

        matched = None
        for opt_key, opt in available:
            if choice == opt_key:
                matched = opt
                break

        if matched:
            print("")
            print_wrapped(matched["response"])
            apply_effects(matched.get("effects", {}))

            # Give item if flagged
            if "gives_item" in matched:
                item_key = matched["gives_item"]
                if item_key not in player["inventory"]:
                    player["inventory"].append(item_key)
                    print_wrapped(f"You receive: {items[item_key]['name']}")

            # Set flag if flagged
            if "sets_flag" in matched:
                player[matched["sets_flag"]] = True

            # Jack dismissal check
            check_jack_availability()
        else:
            print_wrapped("Choose a valid option.")


def talk_ghost_crew(npc):
    members = npc.get("members", {})
    if not members:
        return

    while True:
        print("")
        print("Who do you want to talk to?")
        member_list = list(members.items())
        for i, (key, member) in enumerate(member_list, 1):
            print(f"  [{i}] {member['name']}")
        print("  [0] Leave")
        print("")
        print("> ", end="")
        choice = input().strip()

        if choice == "0":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(member_list):
                member_key, member = member_list[idx]
                talk_ghost_member(member)
            else:
                print_wrapped("Choose a valid number.")
        except ValueError:
            print_wrapped("Choose a valid number.")


def talk_ghost_member(member):
    print("")
    print_wrapped(member["greeting"])
    print("")

    dialogue = member.get("dialogue", {})

    while True:
        available = []
        for key, opt in dialogue.items():
            cond = opt.get("condition")
            if cond is None or cond(player):
                available.append((key, opt))

        if not available:
            print_wrapped("They have nothing more to say.")
            break

        for key, opt in available:
            print(f"  [{key}] {opt['text']}")
        print("  [0] Back")
        print("")
        print("> ", end="")
        choice = input().strip()

        if choice == "0":
            break

        matched = None
        for key, opt in available:
            if choice == key:
                matched = opt
                break

        if matched:
            print("")
            print_wrapped(matched["response"])
            apply_effects(matched.get("effects", {}))

            if "gives_item" in matched:
                item_key = matched["gives_item"]
                if item_key not in player["inventory"]:
                    player["inventory"].append(item_key)
                    print_wrapped(f"You receive: {items[item_key]['name']}")
        else:
            print_wrapped("Choose a valid option.")


def talk_witch(npc):
    dialogue = npc["dialogue"]

    # Check jack vouched
    if player["jack_trust"] >= 4:
        print_wrapped(dialogue["greeting"]["jack_vouched"])
    else:
        print_wrapped(dialogue["greeting"]["default"])

    options = dialogue.get("options", {})

    while True:
        print("")
        available = []
        for key, opt in options.items():
            cond = opt.get("condition")
            if cond is None or cond(player):
                available.append((key, opt))

        if not available:
            print_wrapped("She has said what she's willing to say.")
            break

        for key, opt in available:
            print(f"  [{key}] {opt['text']}")
        print("  [0] Leave")
        print("")
        print("> ", end="")
        choice = input().strip()

        if choice == "0":
            break

        matched = None
        for key, opt in available:
            if choice == key:
                matched = opt
                break

        if matched:
            if matched["response"] == "trade_menu":
                witch_trade_menu(npc)
            else:
                print("")
                print_wrapped(matched["response"])
                apply_effects(matched.get("effects", {}))
        else:
            print_wrapped("Choose a valid option.")


def witch_trade_menu(npc):
    trade = npc["trade"]
    print("")
    print_wrapped(trade["greeting"])

    # Populate witch wants on first visit
    if not trade["wants"]:
        tradeable = [k for k in player["inventory"]
                     if k not in ("tidemark_cutlass", "enhanced_compass",
                                  "compass_of_the_dead", "captains_coat")]
        if tradeable:
            trade["wants"] = random.sample(
                tradeable, min(2, len(tradeable))
            )

    rates = trade["rates"]

    while True:
        print("")
        print("She will trade:")
        for reward, cost in rates.items():
            if reward in items:
                print(f"  {items[reward]['name']} — costs {cost} items")
        print("")
        print("Your inventory:")
        if player["inventory"]:
            for i, key in enumerate(player["inventory"], 1):
                if key in items:
                    print(f"  [{i}] {items[key]['name']}")
        else:
            print("  (nothing)")
        print("  [0] Leave")
        print("")
        print("Choose a reward to trade for > ", end="")
        choice = input().strip().lower()

        if choice == "0":
            break

        # Match reward by name
        reward_key = None
        for key in rates:
            if choice in key or choice in items.get(key, {}).get("name", "").lower():
                reward_key = key
                break

        if not reward_key:
            print_wrapped("She doesn't have that. Choose from her list.")
            continue

        cost = rates[reward_key]
        tradeable_inv = [k for k in player["inventory"]
                         if k not in ("tidemark_cutlass", "enhanced_compass",
                                      "compass_of_the_dead")]

        if len(tradeable_inv) < cost:
            print_wrapped(
                f"You need {cost} items for that. "
                f"You have {len(tradeable_inv)} tradeable items."
            )
            continue

        print(f"\nWhich {cost} items will you trade?")
        traded = []
        for i in range(cost):
            print_current = [k for k in tradeable_inv if k not in traded]
            for j, key in enumerate(print_current, 1):
                if key in items:
                    print(f"  [{j}] {items[key]['name']}")
            print(f"Choose item {i+1} > ", end="")
            sel = input().strip()
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(print_current):
                    traded.append(print_current[idx])
                else:
                    print_wrapped("Invalid choice. Trade cancelled.")
                    traded = []
                    break
            except ValueError:
                print_wrapped("Invalid choice. Trade cancelled.")
                traded = []
                break

        if len(traded) == cost:
            for key in traded:
                player["inventory"].remove(key)
            player["inventory"].append(reward_key)
            player["witch_trades"].append(reward_key)
            print_wrapped(
                f"She takes your items without comment. "
                f"You receive: {items[reward_key]['name']}"
            )
        else:
            print_wrapped("Trade cancelled.")


def talk_event_npc(npc_key, npc):
    events = npc.get("events", [])
    if not events:
        print_wrapped("Nothing happens.")
        return

    # Find first visit event
    if npc_key not in player.get("triggered_events", []):
        if "triggered_events" not in player:
            player["triggered_events"] = []

        first_event = next(
            (e for e in events if e.get("trigger") == "first_visit"), None
        )
        if first_event:
            print("")
            print_wrapped(first_event["text"])
            apply_effects(first_event.get("effects", {}))
            player["triggered_events"].append(npc_key)

        # Deep presence — sit and wait
        if npc_key == "deep_presence":
            npc_condition = npc.get("condition")
            if npc_condition and not npc_condition(player):
                print_wrapped(
                    "Something is here. You can feel it. "
                    "But you need a light that can find what hides."
                )
                return
            if not player["tidal_vision_seen"]:
                print("")
                print_wrapped("Do you sit and wait? [y/n]")
                choice = input().strip().lower()
                if choice == "y":
                    event = next(
                        (e for e in events
                         if e.get("trigger") == "sit_and_wait"), None
                    )
                    if event:
                        print("")
                        print_wrapped(event["text"])
                        apply_effects(event.get("effects", {}))
                        if "sets_flag" in event:
                            player[event["sets_flag"]] = True
            else:
                print_wrapped(
                    "The presence stirs, but you have already seen "
                    "what it has to show. It rests."
                )

        # Kraken hatchling
        if npc_key == "kraken_hatchling":
            print("")
            print("The hatchling struggles beneath the rock.")
            print("  [1] Free it")
            print("  [2] Walk past")
            print("  [3] Leave it")
            print("> ", end="")
            choice = input().strip()
            if choice == "1":
                event = next(
                    (e for e in events
                     if e.get("trigger") == "free_hatchling"), None
                )
                if event:
                    print_wrapped(event["text"])
                    apply_effects(event.get("effects", {}))
            else:
                event = next(
                    (e for e in events
                     if e.get("trigger") == "ignore_hatchling"), None
                )
                if event:
                    print_wrapped(event["text"])
    else:
        print_wrapped(
            "They surface briefly. Regard you. Submerge."
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ROOM EVENTS (first visit triggers)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def trigger_room_event(room_key):
    time.sleep(0.3)

    events = {
        "jungle_path": (
            "The ground pulses. Once. Deliberate. Like a heartbeat."
        ),
        "mangrove_maze": (
            "Something stands very still between the roots. "
            "It knows you're here."
        ),
        "ghost_camp": (
            "The dead don't look up when you arrive. "
            "They've seen this before."
        ),
        "sea_cave": (
            "The cutlass catches the light at the far end. "
            "The thing holding it turns toward you with the calm "
            "of something that has never lost."
        ),
        "bone_bridge": (
            "You stop. You read a name carved into the bone beneath "
            "your feet. Then another. Then you stop reading."
        ),
        "the_ruins": (
            "The floor is warm beneath your boots. "
            "Something beneath it is very aware of you."
        ),
        "sunken_crypt": (
            "His handwriting is small and precise. "
            "It gets slower toward the end."
        ),
        "tidal_pool": (
            "The silence here is complete. "
            "Something at the bottom stirs."
        ),
        "hidden_grotto": (
            "Someone painted this. "
            "Someone who needed it to be found."
        ),
        "clifftop": (
            "The ocean tears open far below. "
            "Something is rising."
        ),
        "volcanic_ridge": (
            "The rock is hot underfoot. The island breathes here "
            "more than anywhere else."
        ),
        "storm_altar": (
            "The lightning strikes in rhythm. "
            "The stones are covered in script you almost understand."
        ),
        "shipwreck_hollow": (
            "Thirty ships. The island keeps what it takes."
        ),
        "ruined_lighthouse": (
            "The mirror array catches the light and throws it nowhere. "
            "With the right tool, you could send a signal."
        )
    }

    if room_key in events:
        print("")
        print_wrapped(events[room_key])

    # Hidden grotto Jack moment
    if room_key == "hidden_grotto" and player["jack_trust"] >= 3:
        time.sleep(1)
        print("")
        print_slow("Jack appears beside you without being summoned.")
        time.sleep(0.5)
        print_wrapped(
            "'We painted this,' he says. 'I'd forgotten.' "
            "A pause. 'We thought someone would find it sooner.' "
            "He turns to you. 'Ask me anything. I'm done being careful.'"
        )
        player["jack_trust"] += 2
        player["morality"] += 1

    # Sunken crypt — reading the journal sets the flag
    if room_key == "sunken_crypt":
        if "jones_journal" in rooms["sunken_crypt"]["items"]:
            print_wrapped(
                "The journal is still here. "
                "Take it and read it."
            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# REACTIVE SYSTEM CHECKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def check_jack_availability():
    if player["jack_dismissed_count"] >= 3 and not player["jack_vanished"]:
        player["jack_vanished"] = True
        print("")
        print_slow("The air feels emptier.")
        time.sleep(0.5)
        print_slow("Jack has stopped appearing.")
        print_slow("You dismissed him one too many times.")
        print_slow("Whatever he would have told you, he won't now.")


def check_jones_stalking():
    if not player["heart_destroyed"]:
        if "the_ruins" in player["visited_rooms"]:
            if random.randint(1, 10) <= 2:
                lines = [
                    "The air shifts. Davy Jones materializes in the corner "
                    "— glances at you — vanishes.",
                    "His voice, from nowhere: 'Still alive. Impressive.'",
                    "The floor pulses beneath you. The Heart beats faster "
                    "for a moment. Then steadies.",
                    "Jones steps from shadow long enough to straighten his "
                    "coat. Then he's gone. The temperature drops."
                ]
                print("")
                print_wrapped(random.choice(lines))
                player["stamina"] = max(0, player["stamina"] - 5)
                player["reputation"] -= 1


def check_tide_timer():
    t = player["turn_count"]

    if t == 60:
        print("")
        print_wrapped("The tide is rising. The island groans.")

    if t == 80:
        print("")
        print_wrapped(
            "Water reaches your ankles in the lower passages. "
            "Something is running out."
        )
        if "tidal_pool" not in player["visited_rooms"]:
            rooms["tidal_pool"]["npc"] = None
            rooms["tidal_pool"]["description"] = (
                "The pool is gone. Swallowed by the rising tide. "
                "Whatever lived at its bottom is beyond reach now."
            )

    if t == 100:
        print("")
        print_wrapped(
            "The island is sinking. "
            "The clifftop is your only option now."
        )

    if t >= 120 and player["current_room"] != "clifftop":
        player_death("tide")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PERMADEATH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def player_death(source):
    clear_screen()
    time.sleep(0.5)
    divider()

    death_scenes = {
        "cave_guardian": (
            "The guardian doesn't pause. Doesn't hesitate. "
            "It has been waiting three centuries for someone to try this. "
            "You are not the first. You will not be the last. "
            "The cutlass stays where it is."
        ),
        "davy_jones": (
            "He watches you drown. Theatrically. "
            "His expression suggests he finds this mildly disappointing. "
            "'You were doing so well,' he says. "
            "The black water closes over you."
        ),
        "sovereign": (
            "Head #3 is the one that gets you. "
            "It looks smug about it. "
            "It will be talking about this for centuries."
        ),
        "bone_bridge": (
            "The sea was waiting at the bottom of the gorge. "
            "Patient. It had time. "
            "Your name joins the others carved into the bone."
        ),
        "storm_altar": (
            "The island decides you're not worthy. "
            "The lightning agrees. "
            "You don't have time to disagree."
        ),
        "tide": (
            "The island sinks. You sink with it. "
            "The sea takes everything eventually. "
            "It was always going to take you too."
        ),
        "both_enemy": (
            "The colossals don't fight the Sovereign. "
            "They fight you. "
            "The Sovereign watches, mildly impressed."
        )
    }

    scene = death_scenes.get(
        source,
        "The island takes you. Everything does, eventually."
    )

    print_slow(scene)
    time.sleep(1)
    print("")
    print_slow("Your name is added to the Bone Bridge.")
    time.sleep(1)
    divider()
    print_slow("        U N C H A I N E D")
    divider()
    print("")
    print("Play again? [y/n] > ", end="")
    choice = input().strip().lower()

    if choice == "y":
        restart_game()
    else:
        print_slow("The sea remembers.")
        time.sleep(1)
        sys.exit()


def restart_game():
    """Reset player state and restart."""
    global player

    player = {
        "name": "Adventurer",
        "current_room": "shore",
        "inventory": [],
        "visited_rooms": [],
        "turn_count": 0,
        "health": 100,
        "max_health": 100,
        "stamina": 50,
        "max_stamina": 50,
        "stamina_regen": 5,
        "momentum": 0,
        "status_effects": [],
        "in_combat": False,
        "combat_target": None,
        "morality": 0,
        "reputation": 0,
        "jack_trust": 0,
        "terror_allegiance": 0,
        "crown_allegiance": 0,
        "witch_trades": [],
        "heart_destroyed": False,
        "heart_weakened": False,
        "colossals_freed": False,
        "jones_confronted": False,
        "jones_knows_journals": False,
        "tidal_vision_seen": False,
        "lighthouse_signaled": False,
        "altar_ritual_done": False,
        "coat_worn": False,
        "guardian_defeated": False,
        "ghost_sailor_named": False,
        "jack_dismissed_count": 0,
        "jack_vanished": False,
        "colossal_cooldown": 0,
        "game_over": False,
        "ending": None,
        "triggered_events": [],
        "cutlass_oiled": False
    }
    rooms["wreck_of_ship"]["items"] = ["old_logbook", "boarding_axe", "locked_chest"]
    rooms["crows_perch"]["items"] = ["spyglass", "compass_shard", "island_map"]
    rooms["volcanic_ridge"]["items"] = ["volcanic_shard"]
    rooms["shipwreck_hollow"]["items"] = ["captains_logbook"]
    rooms["sunken_crypt"]["items"] = ["jones_journal"]
    rooms["the_ruins"]["items"] = ["heart_of_the_locker"]
    rooms["tidal_pool"]["npc"] = "deep_presence"
    rooms["tidal_pool"]["description"] = (
        "A natural pool, connected to the open sea through channels "
        "you can't see. Luminescent creatures drift through it like "
        "living stars that got turned around on the way somewhere "
        "better. The water is warm. The silence here is complete — "
        "no wind, no waves, no island heartbeat. At the bottom of "
        "the pool, something vast and patient waits. Not a monster. "
        "Not a threat. Something old enough that those categories "
        "stopped applying to it centuries ago."
    )

    # Reshuffle witch wants
    npcs["witch"]["trade"]["wants"] = []

    # Reset guardian
    npcs["cave_guardian"]["combat_stats"]["health"] = 80
    npcs["cave_guardian"]["combat_stats"]["tiredness"] = 0

    title_sequence()
    game_loop()



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# COMBAT ENGINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ── Status effect definitions ─────────────────────────────────
STATUS_EFFECTS = {
    "Bleeding":  {"per_turn_damage": 5,  "desc": "Losing blood. -5 HP per turn."},
    "Drowned":   {"stamina_regen_mult": 0.5, "desc": "Waterlogged. Stamina regens at half speed."},
    "Terrified": {"momentum_mult": 0.5, "desc": "Fear dulls your edge. Momentum gains halved."},
    "Saltbound": {"no_dodge": True,     "desc": "Muscles seized. Cannot dodge."},
    "Stunned":   {"skip_turn": True,    "desc": "Head spinning. Skip next action."},
    "Bound":     {"no_items": True,     "desc": "Arms pinned. Cannot use items."},
}


def has_effect(effect_name):
    return effect_name in player["status_effects"]


def add_effect(effect_name):
    if effect_name not in player["status_effects"]:
        player["status_effects"].append(effect_name)
        print_wrapped(f"  [STATUS] {effect_name}: {STATUS_EFFECTS[effect_name]['desc']}")


def remove_effect(effect_name):
    if effect_name in player["status_effects"]:
        player["status_effects"].remove(effect_name)
        print_wrapped(f"  [STATUS cleared] {effect_name}")


def tick_status_effects():
    """Apply per-turn status effect damage/penalties."""
    if has_effect("Bleeding"):
        player["health"] = max(0, player["health"] - 5)
        print_wrapped("  [Bleeding] -5 HP")
    if has_effect("Stunned"):
        remove_effect("Stunned")
    if player.get("colossal_cooldown", 0) > 0:
        player["colossal_cooldown"] -= 1


def apply_stamina_regen():
    regen = player["stamina_regen"]
    if has_effect("Drowned"):
        regen = max(1, regen // 2)
    player["stamina"] = min(player["max_stamina"], player["stamina"] + regen)


def gain_momentum(amount):
    mult = 0.5 if has_effect("Terrified") else 1.0
    player["momentum"] = min(10, player["momentum"] + int(amount * mult))


# ── Combat entry ──────────────────────────────────────────────

def enter_combat(npc_key):
    """Trigger combat with the given NPC."""
    npc = npcs[npc_key]
    if npc["type"] != "combat":
        return

    # Check condition (e.g. guardian already defeated)
    condition = npc.get("condition")
    if condition and not condition(player):
        return

    player["in_combat"] = True
    player["combat_target"] = npc_key
    player["momentum"] = 0
    player["status_effects"] = []

    clear_screen()
    divider()
    print(f"  {npc['name'].upper()}")
    divider()
    print("")
    print_slow(npc["dialogue"]["combat_start"])
    time.sleep(1)
    print("")

    combat_loop(npc_key)


def check_room_combat():
    """Called on room entry — starts combat if room has a live enemy."""
    room = rooms[player["current_room"]]
    if not room["combat_room"]:
        return
    npc_key = room.get("npc")
    if not npc_key:
        return
    npc = npcs.get(npc_key)
    if not npc or npc["type"] != "combat":
        return
    condition = npc.get("condition")
    if condition and not condition(player):
        return
    enter_combat(npc_key)


# ── Combat display ────────────────────────────────────────────

def show_combat_status(npc_key):
    npc = npcs[npc_key]
    stats = npc["combat_stats"]
    hp_bar_player = make_bar(player["health"], player["max_health"], 20)
    hp_bar_enemy  = make_bar(stats["health"], stats["health_max"], 20)
    print("")
    print(f"  YOU  {hp_bar_player} {player['health']}/{player['max_health']} HP")
    print(f"  {npc['name'][:8]:<8} {hp_bar_enemy} {stats['health']}/{stats['health_max']} HP")
    sta_bar = make_bar(player["stamina"], player["max_stamina"], 10)
    mom_bar = "★" * player["momentum"] + "☆" * (5 - player["momentum"])
    print(f"  Stamina {sta_bar} {player['stamina']}  Momentum [{mom_bar}]")
    if player["status_effects"]:
        print(f"  Status: {', '.join(player['status_effects'])}")
    print("")


def make_bar(current, maximum, length):
    filled = int((current / max(maximum, 1)) * length)
    return "[" + "█" * filled + "░" * (length - filled) + "]"


def show_combat_options(npc_key):
    room = rooms[player["current_room"]]
    print("  ─────────────────────────────────")
    if npc_key == "davy_jones" and player.get("jones_knows_journals"):
        print("  [t] talk           I read your journals.")
    print("  [1] attack         Standard strike")
    print("  [2] heavy attack   High damage, costs 15 stamina")
    print("  [3] parry          Block and counter")
    print("  [4] dodge          Avoid attack, gain momentum")
    if player["momentum"] >= 5:
        print("  [5] FINISHER       Devastating blow (momentum 5+)")
    if any(k in player["inventory"] for k in
           ("saltwater_salve", "abyssal_oil", "ghost_rope", "tide_lantern")):
        print("  [6] use item")
    if room["environment_actions"]:
        for i, action in enumerate(room["environment_actions"], 7):
            print(f"  [{i}] {action}")
    print("  ─────────────────────────────────")
    print("")


# ── Player actions ────────────────────────────────────────────

def player_attack(npc_key, heavy=False):
    npc = npcs[npc_key]
    stats = npc["combat_stats"]

    stamina_cost = 15 if heavy else 5
    if player["stamina"] < stamina_cost:
        print_wrapped("  Not enough stamina.")
        return False

    player["stamina"] -= stamina_cost

    # Base damage
    has_cutlass = "tidemark_cutlass" in player["inventory"]
    has_ashblade = "ashblade" in player["inventory"]

    if heavy:
        base = 20 if has_cutlass else (15 if has_ashblade else 10)
    else:
        base = 12 if has_cutlass else (9 if has_ashblade else 6)

    # Abyssal oil bonus
    if player.get("cutlass_oiled") and has_cutlass:
        base += 8
        player["cutlass_oiled"] = False
        print_wrapped("  The abyssal oil flares. The blade cuts deep.")

    # Jones heals unless heart destroyed
    if npc_key == "davy_jones" and not player["heart_destroyed"]:
        print_wrapped(npc["dialogue"]["heart_intact"])
        base = max(0, base - 10)

    damage = max(1, base + random.randint(-2, 3))
    stats["health"] = max(0, stats["health"] - damage)

    hit_lines = [
        f"  You strike. {damage} damage.",
        f"  The blade connects. {damage} damage.",
        f"  A solid hit. {damage} damage.",
        f"  You find an opening. {damage} damage.",
    ]
    print_wrapped(random.choice(hit_lines))

    # Momentum
    gain_momentum(2 if heavy else 1)

    # Guardian tiredness
    if npc_key == "cave_guardian":
        stats["tiredness"] = stats.get("tiredness", 0) + 1
        if stats["tiredness"] == 6:
            print("")
            print_slow(npc["dialogue"]["tiring"])

    return True


def player_parry(npc_key):
    npc = npcs[npc_key]
    stats = npc["combat_stats"]

    if player["stamina"] < 8:
        print_wrapped("  Not enough stamina to hold the parry.")
        return False

    player["stamina"] -= 8

    # 60% success rate, modified by momentum
    success_chance = 60 + player["momentum"] * 5
    if random.randint(1, 100) <= success_chance:
        counter = random.randint(5, 12)
        stats["health"] = max(0, stats["health"] - counter)
        gain_momentum(2)
        print_wrapped(
            f"  You catch the blow and counter. "
            f"{counter} damage."
        )
        if npc_key == "cave_guardian":
            print_wrapped(npc["dialogue"]["player_parry"])
    else:
        # Failed parry — take partial damage
        partial = stats["attack_power"] // 2
        player["health"] = max(0, player["health"] - partial)
        print_wrapped(
            f"  The parry breaks. You take {partial} damage."
        )
    return True


def player_dodge(npc_key):
    if has_effect("Saltbound"):
        print_wrapped("  You can't dodge — Saltbound.")
        return False

    if player["stamina"] < 5:
        print_wrapped("  Not enough stamina.")
        return False

    player["stamina"] -= 5

    if random.randint(1, 100) <= 70:
        gain_momentum(1)
        print_wrapped("  You sidestep cleanly. The attack finds nothing.")
        return True
    else:
        # Partial graze
        graze = npcs[npc_key]["combat_stats"]["attack_power"] // 3
        player["health"] = max(0, player["health"] - graze)
        print_wrapped(f"  You mostly dodge. Graze for {graze} damage.")
        return True


def player_finisher(npc_key):
    if player["momentum"] < 5:
        print_wrapped("  Not enough momentum for a finisher.")
        return False

    npc = npcs[npc_key]
    stats = npc["combat_stats"]

    player["momentum"] = 0
    player["stamina"] -= 10

    has_cutlass = "tidemark_cutlass" in player["inventory"]
    damage = random.randint(30, 45) if has_cutlass else random.randint(20, 32)

    # Jones finisher response
    if npc_key == "davy_jones" and not player["heart_destroyed"]:
        damage = max(0, damage - 10)

    stats["health"] = max(0, stats["health"] - damage)

    print("")
    print_slow(f"  FINISHER — {damage} damage.")
    if npc_key == "davy_jones" and damage >= 25:
        print("")
        print_wrapped(npc["finisher_response"])
    time.sleep(0.5)
    return True


def player_use_item_combat():
    if has_effect("Bound"):
        print_wrapped("  Your arms are pinned. Can't use items.")
        return False

    usable = [k for k in player["inventory"]
              if k in ("saltwater_salve", "abyssal_oil",
                       "ghost_rope", "tide_lantern")]
    if not usable:
        print_wrapped("  Nothing usable in combat.")
        return False

    print("")
    for i, k in enumerate(usable, 1):
        print(f"  [{i}] {items[k]['name']}")
    print("  [0] Cancel")
    print("> ", end="")
    choice = input().strip()

    if choice == "0":
        return False

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(usable):
            key = usable[idx]
            use_combat_item(key)
            return True
    except ValueError:
        pass

    print_wrapped("  Invalid choice.")
    return False


def use_combat_item(key):
    if key == "saltwater_salve":
        heal = min(40, player["max_health"] - player["health"])
        player["health"] += heal
        player["inventory"].remove(key)
        # Clear bleeding
        if has_effect("Bleeding"):
            remove_effect("Bleeding")
        if has_effect("Drowned"):
            remove_effect("Drowned")
        print_wrapped(f"  The salve closes your wounds. +{heal} HP.")

    elif key == "abyssal_oil":
        if "tidemark_cutlass" in player["inventory"]:
            player["cutlass_oiled"] = True
            player["inventory"].remove(key)
            print_wrapped(
                "  The cutlass darkens. Next strike hits harder."
            )
        else:
            print_wrapped("  Nothing to apply it to.")

    elif key == "ghost_rope":
        # Binds enemy for 2 turns — stored as combat flag
        player["enemy_bound_turns"] = 2
        player["inventory"].remove(key)
        print_wrapped(
            "  The ghost rope passes through reality and binds them. "
            "Two turns."
        )

    elif key == "tide_lantern":
        print_wrapped(
            "  The blue-white flame throws the guardian's shadow large "
            "against the cave wall. It flinches. Just for a moment."
        )
        gain_momentum(2)


# ── Environment actions ───────────────────────────────────────

def player_environment_action(action, npc_key):
    npc = npcs[npc_key]
    stats = npc["combat_stats"]
    room_key = player["current_room"]

    # ── Sea Cave ──────────────────────────────────────
    if room_key == "sea_cave":
        if "stalactite" in action:
            if player.get("stalactite_used"):
                print_wrapped(
                    "  There are no more stalactites in reach. "
                    "You already threw the good ones."
                )
                return False
            if player["stamina"] < 10:
                print_wrapped("  Not enough stamina.")
                return False
            player["stamina"] -= 10
            dmg = random.randint(15, 25)
            stats["health"] = max(0, stats["health"] - dmg)
            player["stalactite_used"] = True
            gain_momentum(2)
            print_wrapped(
                f"  You wrench a stalactite from the ceiling and hurl it. "
                f"It connects solidly. {dmg} damage."
            )
            return True

        elif "cave walls" in action or "wall" in action:
            player["health"] = min(
                player["max_health"],
                player["health"] + 10
            )
            gain_momentum(1)
            print_wrapped(
                "  You use the cave walls to brace and redirect the "
                "next blow. Recover 10 HP and gain footing."
            )
            return True

        elif "flood" in action:
            if npc_key == "cave_guardian":
                add_effect("Drowned")
                # Also slow the guardian
                stats["attack_power"] = max(5, stats["attack_power"] - 3)
                print_wrapped(
                    "  You herd the guardian into the flooded corner. "
                    "The cold water slows it. Its attacks weaken."
                )
                return True

        elif "use water" in action or action == "water":
            if has_effect("Bleeding"):
                remove_effect("Bleeding")
            print_wrapped(
                "  The cold cave water cleans the wound. "
                "Bleeding stops."
            )
            return True

    # ── The Ruins ─────────────────────────────────────
    elif room_key == "the_ruins":
        if "altar" in action:
            if player.get("altar_overturned"):
                print_wrapped("  The altar is already overturned.")
                return False
            player["altar_overturned"] = True
            # Weakens Jones' heal
            player["heart_weakened"] = True
            gain_momentum(2)
            print_wrapped(
                "  You overturn the altar. Something in the Heart's "
                "rhythm stutters. Jones feels it."
            )
            if npc_key == "davy_jones":
                if player["heart_destroyed"]:
                    print_wrapped(npc["dialogue"]["heart_destroyed"])
                else:
                    print_wrapped(npc["dialogue"]["heart_intact"])
            return True

        elif "pillar" in action:
            if player.get("pillar_smashed"):
                print_wrapped("  There are no more pillars to use.")
                return False
            player["pillar_smashed"] = True
            dmg = random.randint(20, 30)
            stats["health"] = max(0, stats["health"] - dmg)
            add_effect("Stunned")  # stuns the enemy next turn
            player["enemy_stunned"] = True
            gain_momentum(3)
            print_wrapped(
                f"  You bring down a pillar. Coral and stone scatter. "
                f"{dmg} damage. Jones staggers."
            )
            return True

        elif "invoke" in action or "heart" in action:
            if not player["heart_weakened"]:
                print_wrapped(
                    "  The Heart pulses back, full strength. "
                    "It's not weakened enough. Overturn the altar first."
                )
                return False
            # Damages both — high risk, high reward
            dmg_enemy = random.randint(25, 40)
            dmg_self  = random.randint(10, 20)
            stats["health"] = max(0, stats["health"] - dmg_enemy)
            player["health"] = max(0, player["health"] - dmg_self)
            player["heart_destroyed"] = True
            gain_momentum(3)
            print("")
            print_slow("  You reach into the Heart's pulse and tear.")
            time.sleep(0.5)
            print_wrapped(
                f"  The Heart of the Locker shatters. "
                f"Jones takes {dmg_enemy} damage. "
                f"You take {dmg_self}."
            )
            print("")
            print_wrapped(npc["dialogue"]["heart_destroyed"])
            return True

    # ── Clifftop ──────────────────────────────────────
    elif room_key == "clifftop":
        if "chain" in action:
            if not ("tidemark_cutlass" in player["inventory"] or
                    "ashblade" in player["inventory"]):
                print_wrapped(
                    "  You need a blade for this. "
                    "The boarding axe won't cut it."
                )
                return False
            if player.get("chain_cut"):
                print_wrapped("  The chain is already cut.")
                return False
            player["chain_cut"] = True
            dmg = random.randint(30, 50)
            stats["health"] = max(0, stats["health"] - dmg)
            gain_momentum(5)
            print("")
            print_slow("  You cut the chain.")
            time.sleep(0.5)
            print_wrapped(
                f"  Something fundamental in the Sovereign severs. "
                f"{dmg} damage. The ocean shudders."
            )
            return True

        elif "colossals" in action or "call" in action:
            terror = player.get("terror_allegiance", 0)
            crown  = player.get("crown_allegiance", 0)
            if terror < 2 and crown < 2:
                print_wrapped(
                    "  You call out. Nothing answers. "
                    "You didn't earn this."
                )
                return False
            if player.get("colossal_cooldown", 0) > 0:
                print_wrapped(
                    f"  The colossals are recovering. "
                    f"{player['colossal_cooldown']} turns remaining."
                )
                return False
            dmg = 0
            if terror >= 2:
                d = random.randint(20, 35)
                dmg += d
                print_wrapped(
                    f"  The Six-Crowned Terror surfaces. "
                    f"Head #3: 'We see you.' "
                    f"Three heads strike the Sovereign. {d} damage."
                )
            if crown >= 2:
                d = random.randint(20, 35)
                dmg += d
                print_wrapped(
                    f"  The Abyssal Crown rises from the deep. "
                    f"Kraken arms the size of masts drag the Sovereign "
                    f"back. {d} damage."
                )
            stats["health"] = max(0, stats["health"] - dmg)
            gain_momentum(3)
            player["colossals_freed"] = True
            player["colossal_cooldown"] = 5
            return True

        elif "compass" in action:
            if "enhanced_compass" not in player["inventory"]:
                print_wrapped(
                    "  You don't have the compass. Or not the right one."
                )
                return False
            print("")
            print_slow("  The compass pulls toward the Sovereign's core.")
            time.sleep(0.5)
            dmg = random.randint(40, 60)
            stats["health"] = max(0, stats["health"] - dmg)
            player["inventory"].remove("enhanced_compass")
            gain_momentum(5)
            print_wrapped(
                f"  The needle drives into the core like a key. "
                f"{dmg} damage. The compass is gone."
            )
            return True

    print_wrapped(
        "  The moment passes. That didn't work here."
    )
    return False


# ── Enemy AI ──────────────────────────────────────────────────

def enemy_turn(npc_key):
    npc = npcs[npc_key]
    stats = npc["combat_stats"]

    # Bound check
    if player.get("enemy_bound_turns", 0) > 0:
        player["enemy_bound_turns"] -= 1
        print_wrapped(
            f"  {npc['name']} strains against the ghost rope. "
            f"It holds."
        )
        return

    # Stunned check
    if player.get("enemy_stunned"):
        player["enemy_stunned"] = False
        print_wrapped(f"  {npc['name']} staggers. Loses its turn.")
        return

    ai = stats.get("ai_type", "brute")

    if ai == "brute":
        enemy_ai_brute(npc_key)
    elif ai == "manipulator":
        enemy_ai_manipulator(npc_key)
    elif ai == "multi_phase":
        enemy_ai_sovereign(npc_key)
    else:
        enemy_ai_brute(npc_key)


def enemy_ai_brute(npc_key):
    """Cave Guardian — relentless, gets tired, four arms."""
    npc = npcs[npc_key]
    stats = npc["combat_stats"]
    tiredness = stats.get("tiredness", 0)

    # Weighted ability selection, modified by tiredness
    abilities = npc["abilities"]
    pool = []
    for name, ab in abilities.items():
        w = ab["weight"]
        if tiredness >= 6:
            # Tiring — crush more, slam less
            if name == "slam":
                w = max(5, w - 15)
            if name == "crush":
                w += 10
        pool.extend([name] * w)

    chosen = random.choice(pool)
    ab = abilities[chosen]

    print("")
    print_wrapped(ab["description"])

    # Apply damage
    dmg = ab["damage"]
    if dmg > 0:
        # Player dodge reflex on high momentum
        if player["momentum"] >= 3 and random.randint(1, 100) <= 25:
            print_wrapped("  Your momentum carries you clear. Dodge!")
        else:
            player["health"] = max(0, player["health"] - dmg)
            player["momentum"] = max(0, player["momentum"] - 1)
            print_wrapped(f"  You take {dmg} damage.")
            if "applies_effect" in ab:
                add_effect(ab["applies_effect"])


def enemy_ai_manipulator(npc_key):
    """Davy Jones — theatrical, taunts, drains stamina, heals."""
    npc = npcs[npc_key]
    stats = npc["combat_stats"]
    abilities = npc["abilities"]

    # Jones heals at low health if heart intact
    if (stats["health"] < 40 and not player["heart_destroyed"]
            and random.randint(1, 100) <= 40):
        heal = abilities["heal"]["heal_amount"]
        stats["health"] = min(stats["health_max"], stats["health"] + heal)
        print("")
        print_wrapped(abilities["heal"]["description"])
        return

    # Pick action
    pool = []
    for name, ab in abilities.items():
        if name == "heal":
            continue
        cond = ab.get("condition")
        if cond and not cond(player):
            continue
        pool.extend([name] * ab.get("weight", 10))

    chosen = random.choice(pool)
    ab = abilities[chosen]

    print("")

    if chosen == "taunt":
        line = random.choice(npc["taunt_lines"])
        print_wrapped(line)
        drain = ab.get("stamina_drain", 15)
        player["stamina"] = max(0, player["stamina"] - drain)
        print_wrapped(f"  Stamina drained by {drain}.")
        return

    if chosen == "drain_stamina":
        print_wrapped(ab["description"])
        drain = ab.get("stamina_drain", 20)
        player["stamina"] = max(0, player["stamina"] - drain)
        print_wrapped(f"  Stamina drained by {drain}.")
        return

    # Standard attack
    print_wrapped(ab["description"])
    dmg = ab.get("damage", 0)
    if dmg > 0:
        player["health"] = max(0, player["health"] - dmg)
        player["momentum"] = max(0, player["momentum"] - 2)
        print_wrapped(f"  You take {dmg} damage.")


def enemy_ai_sovereign(npc_key):
    """The Sovereign — multi-phase, escalating."""
    npc = npcs[npc_key]
    stats = npc["combat_stats"]
    phase = stats.get("phase", 1)

    # Phase transitions
    transitions = npc.get("phase_transitions", {})
    if phase == 1 and stats["health"] <= transitions.get("phase_2", {}).get("health_threshold", 9999):
        stats["phase"] = 2
        print("")
        print_slow(transitions["phase_2"]["description"])
        time.sleep(1)
        print_slow(npc["dialogue"]["phase_2_start"])
        time.sleep(1)

    if phase == 2 and stats["health"] <= transitions.get("phase_3", {}).get("health_threshold", 9999):
        stats["phase"] = 3
        print("")
        print_slow(transitions["phase_3"]["description"])
        time.sleep(1)
        print_slow(npc["dialogue"]["phase_3_start"])
        time.sleep(1)

    phase = stats["phase"]
    phase_key = f"phase_{phase}"
    abilities = npc["abilities"].get(phase_key, {})
    if not abilities:
        return

    pool = []
    for name, ab in abilities.items():
        cond = ab.get("condition")
        if cond and cond == "player_did_not_use_heavy":
            # Only triggers if player hasn't used heavy recently
            if player.get("last_action") == "heavy":
                continue
        pool.extend([name] * ab.get("weight", 10))

    if not pool:
        return

    chosen = random.choice(pool)
    ab = abilities[chosen]

    print("")

    if chosen == "head_bite":
        descs = ab.get("descriptions", ["The Sovereign strikes."])
        print_wrapped(random.choice(descs))
    else:
        print_wrapped(ab.get("description", "The Sovereign attacks."))

    # Colossal commentary
    if random.randint(1, 6) == 1:
        commentary = npc["dialogue"].get("head_3_commentary", [])
        if commentary:
            print_wrapped(random.choice(commentary))

    dmg = ab.get("damage", 0)
    if dmg > 0:
        player["health"] = max(0, player["health"] - dmg)
        player["momentum"] = max(0, player["momentum"] - 2)
        print_wrapped(f"  You take {dmg} damage.")
        if "applies_effect" in ab:
            add_effect(ab["applies_effect"])

    heal = ab.get("heal_amount", 0)
    if heal:
        stats["health"] = min(stats["health_max"], stats["health"] + heal)
        print_wrapped(f"  The Sovereign reforms. +{heal} HP.")

    if ab.get("resets_momentum"):
        player["momentum"] = 0
        print_wrapped("  Momentum reset to zero.")


# ── Victory and defeat ────────────────────────────────────────

def combat_victory(npc_key):
    npc = npcs[npc_key]
    print("")
    divider()
    print_slow(npc["dialogue"]["defeated"])
    time.sleep(1)

    # Loot
    loot = npc.get("loot", [])
    for item_key in loot:
        if item_key not in player["inventory"]:
            player["inventory"].append(item_key)
            print("")
            print_wrapped(f"  You receive: {items[item_key]['name']}")
            print_wrapped(items[item_key]["description"])

    # Conditional loot
    cond_loot = npc.get("conditional_loot")
    if cond_loot:
        cond = cond_loot.get("condition")
        if cond and cond(player):
            item_key = cond_loot["item"]
            if item_key not in player["inventory"]:
                player["inventory"].append(item_key)
                print("")
                print_wrapped(f"  You also find: {items[item_key]['name']}")

    # Set flags
    if npc_key == "cave_guardian":
        player["guardian_defeated"] = True
        rooms["sea_cave"]["npc"] = None
        rooms["sea_cave"]["combat_room"] = False

    elif npc_key == "davy_jones":
        player["jones_confronted"] = True
        rooms["the_ruins"]["npc"] = None
        rooms["the_ruins"]["combat_room"] = False
        # Check for final ending path
        if player["heart_destroyed"]:
            print("")
            print_wrapped(
                "The floor cracks. The Heart is gone. "
                "The ruins begin to shake. "
                "There is only one place left to go."
            )

    elif npc_key == "sovereign":
        trigger_ending()
        return

    player["in_combat"] = False
    player["combat_target"] = None
    player["momentum"] = 0
    player["status_effects"] = []

    time.sleep(1)
    divider()
    input("Press Enter to continue...")
    show_room()


def combat_defeat(npc_key):
    player["in_combat"] = False
    player["combat_target"] = None
    player_death(npc_key)


# ── Ending triggers ───────────────────────────────────────────

def trigger_ending():
    clear_screen()
    time.sleep(1)
    divider()

    morality = player["morality"]
    heart    = player["heart_destroyed"]
    jack     = not player["jack_vanished"]
    colossals = player["colossals_freed"]

    if heart and colossals and jack and morality >= 3:
        ending_liberation()
    elif heart and morality >= 0:
        ending_freedom()
    else:
        ending_survival()


def ending_liberation():
    print_slow("        E N D I N G   I")
    print_slow("        LIBERATION")
    divider()
    time.sleep(1)
    print_wrapped(
        "The Sovereign dissolves. The chains that have held the "
        "colossals for three centuries finally break — not with "
        "violence, but with the simple absence of the thing that "
        "bound them. The Abyssal Crown and the Six-Crowned Terror "
        "surface together for the first time without fighting. "
        "They regard each other. They regard you. "
        "They descend, together, into water that is finally their own."
    )
    time.sleep(1)
    print("")
    print_wrapped(
        "Barnacle Jack stands beside you at the clifftop edge. "
        "'Gerald would've cried,' he says. A long pause. "
        "'So would I, if I still could.' "
        "He looks at his hands — more translucent now, barely there. "
        "'I think I can go now.' He doesn't wait for an answer. "
        "He simply stops being present, the way tides do."
    )
    time.sleep(1)
    print("")
    print_wrapped(
        "The island exhales. The heartbeat beneath your feet goes quiet "
        "for the first time in three hundred years. "
        "A ship appears on the horizon. "
        "It sees your signal."
    )
    divider()
    end_game()


def ending_freedom():
    print_slow("        E N D I N G   I I")
    print_slow("        FREEDOM")
    divider()
    time.sleep(1)
    print_wrapped(
        "The Sovereign falls. The Heart is destroyed. "
        "Whether that was the right thing or the only thing "
        "is a question you'll carry. "
        "The island doesn't stop breathing — but it breathes differently now. "
        "Something has been removed from it, and what fills the space "
        "is not yet clear."
    )
    time.sleep(1)
    print("")
    print_wrapped(
        "The colossals are still out there. Still circling. "
        "Whether they're free now or simply directionless, "
        "you can't tell from here. "
        "Maybe it doesn't matter. "
        "Maybe it's the same thing."
    )
    time.sleep(1)
    print("")
    print_wrapped(
        "A ship appears on the horizon. "
        "You don't know if it's coming for you. "
        "You walk toward the shore anyway."
    )
    divider()
    end_game()


def ending_survival():
    print_slow("        E N D I N G   I I I")
    print_slow("        SURVIVAL")
    divider()
    time.sleep(1)
    print_wrapped(
        "You survive. That's the whole of it. "
        "The Heart isn't destroyed — something else is. "
        "The island watches you go with the patient attention "
        "of something that has seen this before and will see it again."
    )
    time.sleep(1)
    print("")
    print_wrapped(
        "The colossals are still fighting. "
        "Jack never appeared. "
        "The chains hold."
    )
    time.sleep(1)
    print("")
    print_wrapped(
        "You find a piece of wreckage large enough to float on. "
        "The tide takes you away from the island, slowly. "
        "You don't look back. "
        "The island doesn't need you to."
    )
    divider()
    end_game()


def end_game():
    player["game_over"] = True
    time.sleep(1)
    print("")
    print_slow("        U N C H A I N E D")
    print_slow("  The Curse of the Sunken Compass")
    divider()
    print("")
    print("Play again? [y/n] > ", end="")
    choice = input().strip().lower()
    if choice == "y":
        restart_game()
    else:
        print_slow("The sea remembers.")
        time.sleep(1)
        sys.exit()


# ── Main combat loop ──────────────────────────────────────────

def combat_loop(npc_key):
    npc = npcs[npc_key]
    stats = npc["combat_stats"]

    while player["health"] > 0 and stats["health"] > 0:
        room = rooms[player["current_room"]]

        # Status effect tick
        tick_status_effects()
        apply_stamina_regen()

        if player["health"] <= 0:
            combat_defeat(npc_key)
            return

        # Display
        show_combat_status(npc_key)
        show_combat_options(npc_key)

        # Skip turn if stunned
        if has_effect("Stunned"):
            print_wrapped("  You're stunned — skipping your turn.")
            remove_effect("Stunned")
            enemy_turn(npc_key)
            player["last_action"] = "stunned"
            continue

        # Get player input
        print("> ", end="")
        raw = input().strip().lower()
        print("")

        acted = False

        # Jones journals talk option
        if raw in ("talk", "t", "journals", "i read your journals") and                 npc_key == "davy_jones" and player["jones_knows_journals"]:
            print("")
            print_wrapped(npcs["davy_jones"]["dialogue"]["journals_unlocked"])
            gain_momentum(2)
            npcs["davy_jones"]["combat_stats"]["attack_power"] = max(
                10, npcs["davy_jones"]["combat_stats"]["attack_power"] - 3
            )
            acted = True
            player["last_action"] = "talk"

        elif raw in ("1", "attack", "a"):
            acted = player_attack(npc_key, heavy=False)
            player["last_action"] = "attack"

        elif raw in ("2", "heavy", "heavy attack", "h"):
            acted = player_attack(npc_key, heavy=True)
            player["last_action"] = "heavy"

        elif raw in ("3", "parry", "p"):
            acted = player_parry(npc_key)
            player["last_action"] = "parry"

        elif raw in ("4", "dodge", "d"):
            acted = player_dodge(npc_key)
            player["last_action"] = "dodge"

        elif raw in ("5", "finisher", "f") and player["momentum"] >= 5:
            acted = player_finisher(npc_key)
            player["last_action"] = "finisher"

        elif raw in ("6", "use", "use item", "item"):
            acted = player_use_item_combat()
            player["last_action"] = "item"

        else:
            # Check environment actions (numbered 7+)
            env_actions = room.get("environment_actions", [])
            matched = False

            # Number shortcut
            try:
                idx = int(raw) - 7
                if 0 <= idx < len(env_actions):
                    acted = player_environment_action(env_actions[idx], npc_key)
                    player["last_action"] = "environment"
                    matched = True
            except ValueError:
                pass

            # Name match
            if not matched:
                for action in env_actions:
                    if any(word in raw for word in action.split()):
                        acted = player_environment_action(action, npc_key)
                        player["last_action"] = "environment"
                        matched = True
                        break

            if not matched:
                print_wrapped(
                    "  In combat: attack, heavy, parry, dodge, "
                    "use item, or an environment action."
                )
                continue

        # Check enemy death
        if stats["health"] <= 0:
            combat_victory(npc_key)
            return

        # Check player death
        if player["health"] <= 0:
            combat_defeat(npc_key)
            return

        # Enemy turn (only if player acted)
        if acted:
            time.sleep(0.4)
            enemy_turn(npc_key)

            # Check deaths after enemy turn
            if player["health"] <= 0:
                combat_defeat(npc_key)
                return
            if stats["health"] <= 0:
                combat_victory(npc_key)
                return

            player["turn_count"] += 1

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN GAME LOOP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def game_loop():
    show_room()
    check_room_combat()

    while not player["game_over"]:
        if player["in_combat"]:
            npc_key = player["combat_target"]
            if npc_key:
                combat_loop(npc_key)
        else:
            check_jack_availability()
            check_jones_stalking()
            check_tide_timer()

            command, target = get_input()

            # Heart destruction shortcut commands
            if command in ("invoke", "destroy", "break", "shatter") and "heart" in target:
                cmd_use("heart of the locker")
                continue

            resolve_command(command, target)
            # Re-check combat after each action (e.g. entering a room triggers it)
            if not player["in_combat"] and not player["game_over"]:
                check_room_combat()


def main():
    title_sequence()
    game_loop()


if __name__ == "__main__":
    main()