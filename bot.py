import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import re
import json
import copy
from datetime import datetime

# -----------------------------
# LOAD TOKEN
# -----------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN not found in .env file")

# -----------------------------
# LOGGING
# -----------------------------
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

# -----------------------------
# INTENTS
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# -----------------------------
# BOT SETUP
# -----------------------------
bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
# FILES
# -----------------------------
RIDER_FILE = "rider_formation.json"
INFANTRY_FILE = "infantry_formation.json"
SCRIBE_FILE = "scribe_formation.json"
HEALER_FILE = "healer_formation.json"
FIGHT_FILE = "fight_records.json"

# -----------------------------
# RIDER FORMATION DATA
# -----------------------------
DEFAULT_RIDER_STRUCTURE = {
    "First Wing": {
        "wingleader": "genevieve nguyen",
        "executive_officer": None,
        "sections": {
            "Flame Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            },
            "Claw Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            },
            "Tail Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            }
        }
    },
    "Second Wing": {
        "wingleader": None,
        "executive_officer": None,
        "sections": {
            "Flame Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            },
            "Claw Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            },
            "Tail Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            }
        }
    },
    "Third Wing": {
        "wingleader": None,
        "executive_officer": None,
        "sections": {
            "Flame Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": "marina kalisa",
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            },
            "Claw Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            },
            "Tail Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            }
        }
    },
    "Fourth Wing": {
        "wingleader": None,
        "executive_officer": None,
        "sections": {
            "Flame Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            },
            "Claw Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            },
            "Tail Section": {
                "section_leader": None,
                "executive_officer": None,
                "squads": {
                    "First Squad": {
                        "squad_leader": None,
                        "executive_squad_leader": None,
                        "cadets": []
                    }
                }
            }
        }
    }
}

# -----------------------------
# INFANTRY FORMATION DATA
# -----------------------------
DEFAULT_INFANTRY_STRUCTURE = {
    "_chain": {
        "High Commander": None,
        "Commander": None
    },
    "First Division": {
        "Captain": None,
        "Sergeant": None,
        "Corporal": None,
        "Soldier": None,
        "Cadets": []
    },
    "Second Division": {
        "Captain": None,
        "Sergeant": None,
        "Corporal": None,
        "Soldier": None,
        "Cadets": []
    },
    "Third Division": {
        "Captain": None,
        "Sergeant": None,
        "Corporal": None,
        "Soldier": None,
        "Cadets": []
    },
    "Fourth Division": {
        "Captain": None,
        "Sergeant": None,
        "Corporal": None,
        "Soldier": None,
        "Cadets": []
    }
}

# -----------------------------
# SCRIBE FORMATION DATA
# -----------------------------
DEFAULT_SCRIBE_STRUCTURE = {
    "_chain": {
        "Grand Maester": None,
        "Head Archivist": None
    },
    "First Order": {
        "Master Scholar": None,
        "Curator": None,
        "Archivist": None,
        "Senior Scribe": None,
        "Scribes": []
    },
    "Second Order": {
        "Master Scholar": None,
        "Curator": None,
        "Archivist": None,
        "Senior Scribe": None,
        "Scribes": []
    },
    "Third Order": {
        "Master Scholar": None,
        "Curator": None,
        "Archivist": None,
        "Senior Scribe": None,
        "Scribes": []
    },
    "Fourth Order": {
        "Master Scholar": None,
        "Curator": None,
        "Archivist": None,
        "Senior Scribe": None,
        "Scribes": []
    }
}

# -----------------------------
# HEALER FORMATION DATA
# -----------------------------
DEFAULT_HEALER_STRUCTURE = {
    "_chain": {
        "Arch Healer": None,
        "Healer": None
    },
    "First Circle": {
        "Senior Practitioner": None,
        "Practitioner": None,
        "Medic": None,
        "Acolyte": None,
        "Trainees": []
    },
    "Second Circle": {
        "Senior Practitioner": None,
        "Practitioner": None,
        "Medic": None,
        "Acolyte": None,
        "Trainees": []
    },
    "Third Circle": {
        "Senior Practitioner": None,
        "Practitioner": None,
        "Medic": None,
        "Acolyte": None,
        "Trainees": []
    },
    "Fourth Circle": {
        "Senior Practitioner": None,
        "Practitioner": None,
        "Medic": None,
        "Acolyte": None,
        "Trainees": []
    }
}

# -----------------------------
# CHARACTER GENERATOR DATA
# -----------------------------
FIRST_NAMES = [
    "Aelin", "Mira", "Talia", "Nessa", "Elira", "Kaia", "Lyra", "Seren", "Veda", "Rhea",
    "Dorian", "Cassian", "Rhys", "Bren", "Matthias", "Lucan", "Gideon", "Theron", "Kieran", "Rowan",
    "Sable", "Aster", "Indra", "Valen", "Noa", "Ari", "Emery", "Ren", "Cai", "Briar"
]

LAST_NAMES = [
    "Sorren", "Vale", "Dane", "Aurell", "Mercer", "Thorne", "Kallis", "Morcant", "Arden", "Voss",
    "Ravelle", "Ashdown", "Corven", "Damaris", "Ellowen", "Drake", "Morrow", "Wren", "Keir", "Halden"
]

ALIASES = [
    "Red", "Ash", "Birdie", "Storm", "Lucky", "Fox", "Rook", "Blade", "Ghost", "Crow",
    "Blue", "Rune", "Torch", "Thorn", "Echo", "Vex", "Sparrow", "Bolt", "Rose", "Flint"
]

PRONOUN_SETS = [
    ("woman", "she/her"),
    ("man", "he/him"),
    ("nonbinary", "they/them")
]

POSITIVE_TRAITS = [
    "loyal", "disciplined", "charming", "sharp-witted", "resourceful", "steady", "fearless", "observant",
    "ambitious", "clever", "protective", "devoted", "resilient", "charismatic", "strategic", "patient"
]

NEGATIVE_TRAITS = [
    "stubborn", "reckless", "guarded", "blunt", "secretive", "impatient", "prideful", "sarcastic",
    "vengeful", "moody", "argumentative", "restless", "cold", "impulsive", "ruthless", "suspicious"
]

AESTHETICS = [
    "ink-stained fingers", "sword belts and leather gloves", "storm clouds and silver rings", "pressed flowers in books",
    "burnished gold details", "moonlit balconies", "cracked marble and candle smoke", "black uniforms and sharp boots",
    "daggers hidden in lace", "dragon scales and soot", "velvet collars", "midnight blue silk", "rain on stone",
    "worn journals", "copper clasps", "obsidian jewelry", "sun-faded maps", "smoked glass"
]

ALLIANCES = ["Navarre", "Navarre", "Navarre", "Navarre", "Rebellion"]

DRAGON_NAMES = [
    "Tairnith", "Arixa", "Velmora", "Soryn", "Kaelor", "Nysera", "Vharyn", "Torvek", "Mireth", "Zalara",
    "Rhykor", "Aethra", "Vorryn", "Selka", "Draevik", "Maelis", "Kovara", "Zephrys", "Orynth", "Thessra"
]

DRAGON_PRONOUNS = ["she/her", "he/him", "they/them"]
DRAGON_COLORS = ["Black", "Red", "Red", "Orange", "Orange", "Blue", "Blue", "Brown", "Brown", "Green", "Green"]
DRAGON_TAILS = ["Morningstar tail", "Swordtail", "Swordtail", "Scorpion tail", "Scorpion tail", "Club tail", "Club tail", "Daggertail", "Daggertail"]
SIGNETS = [
    "shadow wielding", "lightning wielding", "truth-sensing", "distance wielding", "ice wielding", "fire wielding",
    "mindwork", "shielding", "dreamwalking", "metal manipulation", "wind wielding", "poison detection",
    "healing amplification", "precognition flashes", "illusion casting", "gravity manipulation"
]
RIDER_TITLES = ["", "Squad hopeful", "Marked cadet", "Reluctant prodigy", "Wingleader's headache", "Dragon-bonded menace"]

INFANTRY_SPECIALTIES = ["Vanguard", "Bastion", "Skirmisher", "Breaker", "Ranger", "Tactician"]
COMBAT_TRAITS = [
    "excellent with a blade", "strong defensive instincts", "fast on their feet", "excellent formation discipline",
    "brutal in close combat", "steady under pressure", "deadly at range", "good battlefield awareness"
]
INFANTRY_DIVISIONS = ["First Division", "Second Division", "Third Division", "Fourth Division"]
INFANTRY_TITLES = ["", "Frontline menace", "Shield wall darling", "Too stubborn to die", "Captain's favorite problem"]

SCRIBE_SPECIALTIES = ["Archive", "Chronicle", "Lexicon", "Intelligence", "Cipher", "Restricted"]
ACADEMIC_STRENGTHS = [
    "languages", "historical recall", "rapid transcription", "pattern recognition", "codebreaking", "research",
    "political analysis", "memorization"
]
SCRIBE_ORDERS = ["First Order", "Second Order", "Third Order", "Fourth Order"]
SCRIBE_TITLES = ["", "Archivist's nightmare", "Ink-stained prodigy", "Forbidden stacks enthusiast", "Faculty favorite"]

HEALER_CIRCLES = ["First Circle", "Second Circle", "Third Circle", "Fourth Circle"]
HEALER_SPECIALTIES = ["Battlefield", "Surgical", "Recovery", "Emergency", "Experimental", "Dragonkind"]
HEALER_TITLES = ["", "Calm in chaos", "Battle-born medic", "Sleep-deprived miracle worker", "Senior healer's headache"]

MENTION_REPLIES = [
    "You rang, cadet?",
    "Basgiath sees all.",
    "Try not to die today.",
    "At your service, menace.",
    "State your business before the dragons get impatient.",
    "You called. I judged. I'm listening.",
    "Reporting for chaos.",
    "Careful. Tag me twice and I'll start assigning signets.",
    "What is it now, rider?",
    "You have my attention. Briefly."
]

# -----------------------------
# JSON HELPERS
# -----------------------------
def load_json_file(filename, default_data):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return copy.deepcopy(default_data)


def save_json_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


rider_data = load_json_file(RIDER_FILE, DEFAULT_RIDER_STRUCTURE)
infantry_data = load_json_file(INFANTRY_FILE, DEFAULT_INFANTRY_STRUCTURE)
scribe_data = load_json_file(SCRIBE_FILE, DEFAULT_SCRIBE_STRUCTURE)
healer_data = load_json_file(HEALER_FILE, DEFAULT_HEALER_STRUCTURE)
fight_records = load_json_file(FIGHT_FILE, {})

# -----------------------------
# BASIC HELPERS
# -----------------------------
def normalize_name(name: str) -> str:
    return name.lower().strip()


def random_full_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def pick_two_unique(options):
    return random.sample(options, 2)


def pick_three_unique(options):
    return random.sample(options, 3)


def name_exists_anywhere(name: str) -> bool:
    return (
        find_existing_rider_assignment(rider_data, name)
        or find_name_in_simple_structure(infantry_data, name, "Cadets")
        or find_name_in_simple_structure(scribe_data, name, "Scribes")
        or find_name_in_simple_structure(healer_data, name, "Trainees")
    )


def generate_unique_full_name(max_attempts: int = 500) -> str:
    for _ in range(max_attempts):
        candidate = random_full_name()
        if not name_exists_anywhere(candidate):
            return candidate
    raise RuntimeError("Could not generate a unique character name. Add more names to the pools.")


def format_rider_path_from_slot(slot):
    if len(slot) == 2:
        return slot[1]
    if len(slot) == 3:
        return f"{slot[1]} / {slot[2]}"
    return f"{slot[1]} / {slot[2]} / {slot[3]}"


def create_character_profile(quadrant_choice: str | None = None) -> str:
    global rider_data, infantry_data, scribe_data, healer_data

    valid_quadrants = ["riders", "infantry", "scribes", "healers"]

    if quadrant_choice is None:
        quadrant = random.choice(valid_quadrants)
    else:
        quadrant = quadrant_choice.lower().strip()
        if quadrant not in valid_quadrants:
            quadrant = random.choice(valid_quadrants)

    name = generate_unique_full_name()
    alias = random.choice(ALIASES)
    age = random.randint(21, 27)
    gender, pronouns = random.choice(PRONOUN_SETS)
    alliance = random.choice(ALLIANCES)
    positive_1, positive_2 = pick_two_unique(POSITIVE_TRAITS)
    negative_1, negative_2 = pick_two_unique(NEGATIVE_TRAITS)
    aesthetic_1, aesthetic_2, aesthetic_3 = pick_three_unique(AESTHETICS)

    base = [
        f"**Title:** {name}",
        f"• **alias/nickname:** {alias}",
        f"• **age:** {age}",
        f"• **gender / pronouns:** {gender} / {pronouns}",
        f"• **quadrant:** {quadrant}",
        f"• **alliance:** {alliance}",
        "",
        f"• **positive traits:** {positive_1}, {positive_2}",
        f"• **negative traits:** {negative_1}, {negative_2}",
        f"• **aesthetics:** {aesthetic_1}, {aesthetic_2}, {aesthetic_3}",
        "",
        "***Chose One Of These:***",
        ""
    ]

    if quadrant == "riders":
        slots = get_open_rider_slots(rider_data)
        if not slots:
            raise RuntimeError("No rider slots left.")

        slot = random.choice(slots)
        assign_rider_slot(rider_data, name, slot)
        save_json_file(RIDER_FILE, rider_data)

        base.extend([
            "✦ **RIDERS**",
            f"• **dragon name:** {random.choice(DRAGON_NAMES)}",
            f"• **dragon color-tail:** {random.choice(DRAGON_COLORS)} {random.choice(DRAGON_TAILS)}",
            f"• **dragon pronouns:** {random.choice(DRAGON_PRONOUNS)}",
            f"• **signet:** {random.choice(SIGNETS)}",
            f"• **wing / section / squad:** {format_rider_path_from_slot(slot)}",
            f"• **title if applicable:** {slot[0]}"
        ])
    elif quadrant == "infantry":
        slots = get_simple_open_slots(
            infantry_data,
            ["High Commander", "Commander"],
            ["Captain", "Sergeant", "Corporal", "Soldier"],
            "Cadet",
            "Cadets"
        )
        if not slots:
            raise RuntimeError("No infantry slots left.")

        slot = random.choice(slots)
        assign_simple_slot(infantry_data, name, slot, "Cadet", "Cadets")
        save_json_file(INFANTRY_FILE, infantry_data)

        division_value = slot[1] if slot[1] != "_chain" else "High Chain"
        base.extend([
            "✦ **INFANTRY**",
            f"• **specialization:** {random.choice(INFANTRY_SPECIALTIES)}",
            f"• **combat trait:** {random.choice(COMBAT_TRAITS)}",
            f"• **division:** {division_value}",
            f"• **title if applicable:** {slot[0]}"
        ])
    elif quadrant == "scribes":
        slots = get_simple_open_slots(
            scribe_data,
            ["Grand Maester", "Head Archivist"],
            ["Master Scholar", "Curator", "Archivist", "Senior Scribe"],
            "Scribe",
            "Scribes"
        )
        if not slots:
            raise RuntimeError("No scribe slots left.")

        slot = random.choice(slots)
        assign_simple_slot(scribe_data, name, slot, "Scribe", "Scribes")
        save_json_file(SCRIBE_FILE, scribe_data)

        order_value = slot[1] if slot[1] != "_chain" else "High Chain"
        base.extend([
            "✦ **SCRIBES**",
            f"• **subject specialty:** {random.choice(SCRIBE_SPECIALTIES)}",
            f"• **academic strength:** {random.choice(ACADEMIC_STRENGTHS)}",
            f"• **archive order:** {order_value}",
            f"• **title if applicable:** {slot[0]}"
        ])
    else:
        slots = get_simple_open_slots(
            healer_data,
            ["Arch Healer", "Healer"],
            ["Senior Practitioner", "Practitioner", "Medic", "Acolyte"],
            "Trainee",
            "Trainees"
        )
        if not slots:
            raise RuntimeError("No healer slots left.")

        slot = random.choice(slots)
        assign_simple_slot(healer_data, name, slot, "Trainee", "Trainees")
        save_json_file(HEALER_FILE, healer_data)

        circle_value = slot[1] if slot[1] != "_chain" else "High Chain"
        base.extend([
            "✦ **HEALERS**",
            f"• **circle:** {circle_value}",
            f"• **specialization:** {random.choice(HEALER_SPECIALTIES)}",
            f"• **title if applicable:** {slot[0]}"
        ])

    return "\n".join(base)


def split_long_message(text: str, chunk_size: int = 1900):
    chunks = []
    remaining = text
    while len(remaining) > chunk_size:
        split_at = remaining.rfind("\n", 0, chunk_size)
        if split_at == -1:
            split_at = chunk_size
        chunks.append(remaining[:split_at])
        remaining = remaining[split_at:].lstrip("\n")
    if remaining:
        chunks.append(remaining)
    return chunks

# -----------------------------
# FIGHT TRACKING HELPERS
# -----------------------------
def get_all_active_characters():
    characters = {}

    for wing_name, wing in rider_data.items():
        if wing["wingleader"]:
            name = wing["wingleader"]
            characters[normalize_name(name)] = {
                "name": name,
                "quadrant": "riders",
                "role": "Wingleader",
                "assignment": wing_name
            }

        if wing["executive_officer"]:
            name = wing["executive_officer"]
            characters[normalize_name(name)] = {
                "name": name,
                "quadrant": "riders",
                "role": "Wing Executive Officer",
                "assignment": wing_name
            }

        for section_name, section in wing["sections"].items():
            if section["section_leader"]:
                name = section["section_leader"]
                characters[normalize_name(name)] = {
                    "name": name,
                    "quadrant": "riders",
                    "role": "Section Leader",
                    "assignment": f"{wing_name} / {section_name}"
                }

            if section["executive_officer"]:
                name = section["executive_officer"]
                characters[normalize_name(name)] = {
                    "name": name,
                    "quadrant": "riders",
                    "role": "Section Executive Officer",
                    "assignment": f"{wing_name} / {section_name}"
                }

            for squad_name, squad in section["squads"].items():
                if squad["squad_leader"]:
                    name = squad["squad_leader"]
                    characters[normalize_name(name)] = {
                        "name": name,
                        "quadrant": "riders",
                        "role": "Squad Leader",
                        "assignment": f"{wing_name} / {section_name} / {squad_name}"
                    }

                if squad["executive_squad_leader"]:
                    name = squad["executive_squad_leader"]
                    characters[normalize_name(name)] = {
                        "name": name,
                        "quadrant": "riders",
                        "role": "Executive Squad Leader",
                        "assignment": f"{wing_name} / {section_name} / {squad_name}"
                    }

                for cadet in squad["cadets"]:
                    characters[normalize_name(cadet)] = {
                        "name": cadet,
                        "quadrant": "riders",
                        "role": "Cadet",
                        "assignment": f"{wing_name} / {section_name} / {squad_name}"
                    }

    for role_name, assigned_name in infantry_data["_chain"].items():
        if assigned_name:
            characters[normalize_name(assigned_name)] = {
                "name": assigned_name,
                "quadrant": "infantry",
                "role": role_name,
                "assignment": "High Chain"
            }

    for division_name, division in infantry_data.items():
        if division_name == "_chain":
            continue
        for role_name, assigned_name in division.items():
            if role_name == "Cadets":
                for cadet in assigned_name:
                    characters[normalize_name(cadet)] = {
                        "name": cadet,
                        "quadrant": "infantry",
                        "role": "Cadet",
                        "assignment": division_name
                    }
            elif assigned_name:
                characters[normalize_name(assigned_name)] = {
                    "name": assigned_name,
                    "quadrant": "infantry",
                    "role": role_name,
                    "assignment": division_name
                }

    for role_name, assigned_name in scribe_data["_chain"].items():
        if assigned_name:
            characters[normalize_name(assigned_name)] = {
                "name": assigned_name,
                "quadrant": "scribes",
                "role": role_name,
                "assignment": "High Chain"
            }

    for order_name, order in scribe_data.items():
        if order_name == "_chain":
            continue
        for role_name, assigned_name in order.items():
            if role_name == "Scribes":
                for scribe in assigned_name:
                    characters[normalize_name(scribe)] = {
                        "name": scribe,
                        "quadrant": "scribes",
                        "role": "Scribe",
                        "assignment": order_name
                    }
            elif assigned_name:
                characters[normalize_name(assigned_name)] = {
                    "name": assigned_name,
                    "quadrant": "scribes",
                    "role": role_name,
                    "assignment": order_name
                }

    for role_name, assigned_name in healer_data["_chain"].items():
        if assigned_name:
            characters[normalize_name(assigned_name)] = {
                "name": assigned_name,
                "quadrant": "healers",
                "role": role_name,
                "assignment": "High Chain"
            }

    for circle_name, circle in healer_data.items():
        if circle_name == "_chain":
            continue
        for role_name, assigned_name in circle.items():
            if role_name == "Trainees":
                for trainee in assigned_name:
                    characters[normalize_name(trainee)] = {
                        "name": trainee,
                        "quadrant": "healers",
                        "role": "Trainee",
                        "assignment": circle_name
                    }
            elif assigned_name:
                characters[normalize_name(assigned_name)] = {
                    "name": assigned_name,
                    "quadrant": "healers",
                    "role": role_name,
                    "assignment": circle_name
                }

    return characters


def resolve_active_character(name: str):
    return get_all_active_characters().get(normalize_name(name))


def ensure_fight_record(name: str):
    key = normalize_name(name)
    if key not in fight_records:
        fight_records[key] = {
            "name": name,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "fights": []
        }
    return fight_records[key]


def record_fight_result(name, opponent, roll, opponent_roll, outcome):
    record = ensure_fight_record(name)
    record["name"] = name

    if outcome == "win":
        record["wins"] += 1
    elif outcome == "loss":
        record["losses"] += 1
    else:
        record["draws"] += 1

    record["fights"].append({
        "opponent": opponent,
        "roll": roll,
        "opponent_roll": opponent_roll,
        "outcome": outcome,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    })


def get_fight_summary(name: str):
    return fight_records.get(normalize_name(name))


def format_masterboard():
    active = get_all_active_characters()
    if not active:
        return "No active characters found."

    rows = []
    for info in active.values():
        record = fight_records.get(normalize_name(info["name"]), {"wins": 0, "losses": 0, "draws": 0, "fights": []})
        rows.append((
            info["quadrant"],
            info["name"],
            info["role"],
            info["assignment"],
            record["wins"],
            record["losses"],
            record["draws"],
            len(record["fights"])
        ))

    rows.sort(key=lambda x: (x[0], x[1].lower()))

    lines = ["**Masterboard**"]
    current_quadrant = None
    for quadrant, name, role, assignment, wins, losses, draws, total in rows:
        if quadrant != current_quadrant:
            current_quadrant = quadrant
            lines.append("")
            lines.append(f"**{quadrant.title()}**")
        lines.append(f"• **{name}** — {role} | {assignment} | W-L-D: {wins}-{losses}-{draws} | Fights: {total}")

    return "\n".join(lines)


def format_fight_log(name: str):
    info = resolve_active_character(name)
    record = get_fight_summary(name)

    if not info and not record:
        return None

    display_name = info["name"] if info else record["name"]
    role = info["role"] if info else "Inactive"
    quadrant = info["quadrant"].title() if info else "Unknown"
    assignment = info["assignment"] if info else "Not currently assigned"

    if not record or not record["fights"]:
        return (
            f"**Fight Log: {display_name}**\n"
            f"Quadrant: **{quadrant}**\n"
            f"Role: **{role}**\n"
            f"Assignment: **{assignment}**\n"
            f"Record: **0-0-0**\n"
            "No fights recorded yet."
        )

    lines = [
        f"**Fight Log: {display_name}**",
        f"Quadrant: **{quadrant}**",
        f"Role: **{role}**",
        f"Assignment: **{assignment}**",
        f"Record: **{record['wins']}-{record['losses']}-{record['draws']}**",
        "",
        "**Recent Fights**"
    ]

    for fight in record["fights"][-15:][::-1]:
        outcome = fight["outcome"].title()
        lines.append(f"• vs **{fight['opponent']}** — {outcome} ({fight['roll']} to {fight['opponent_roll']}) on {fight['timestamp']}")

    return "\n".join(lines)


# -----------------------------
# EVENTS
# -----------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user and bot.user in message.mentions:
        await message.channel.send(random.choice(MENTION_REPLIES))

    await bot.process_commands(message)

# -----------------------------
# BASGAITH COMMANDS
# -----------------------------
@bot.command()
async def threshing(ctx):
    await ctx.send(
        f"**Threshing Result**\n"
        f"Dragon Color: **{random.choice(DRAGON_COLORS)}**\n"
        f"Tail: **{random.choice(DRAGON_TAILS)}**"
    )


@bot.command()
async def infantry(ctx):
    specialties = [
        ("Vanguard", "Frontline fighters. First to engage, built for direct combat and sustained pressure."),
        ("Bastion", "Defensive specialists. Shielding, protection, and holding formation under attack."),
        ("Skirmisher", "Fast and mobile. Flanking, scouting, and hit-and-run tactics."),
        ("Breaker", "Heavy force. Used to overwhelm defenses and break enemy lines."),
        ("Ranger", "Ranged specialists. Precision strikes, overwatch, and distance control."),
        ("Tactician", "Strategy-focused. Coordination, positioning, and battlefield awareness.")
    ]

    roll_num = random.randint(1, 6)
    name, desc = specialties[roll_num - 1]

    await ctx.send(
        f"**Infantry Result**\n"
        f"Roll: **{roll_num}**\n"
        f"Combat Specialty: **{name}**\n"
        f"{desc}"
    )


@bot.command()
async def scribe(ctx):
    specialties = [
        ("Archive", "Preservation of records, ancient texts, and restricted materials."),
        ("Chronicle", "Documentation of events, reports, and historical accounts."),
        ("Lexicon", "Languages, translation, and interpretation of foreign or coded texts."),
        ("Intelligence", "Information gathering, analysis, and strategic insight."),
        ("Cipher", "Codes, encryption, and protection of sensitive information."),
        ("Restricted", "Forbidden knowledge and sealed records under strict oversight.")
    ]

    roll_num = random.randint(1, 6)
    name, desc = specialties[roll_num - 1]

    await ctx.send(
        f"**Scribe Result**\n"
        f"Roll: **{roll_num}**\n"
        f"Subject Specialty: **{name}**\n"
        f"{desc}"
    )


@bot.command()
async def healer(ctx):
    disciplines = [
        ("Battlefield", "Healers trained to operate within active combat."),
        ("Surgical", "Healers specializing in controlled, precision-based procedures."),
        ("Recovery", "Healers focused on long-term care and rehabilitation."),
        ("Emergency", "Healers trained for critical intervention."),
        ("Experimental", "Healers who utilize unproven or evolving methods."),
        ("Dragonkind", "Healers trained to treat dragons and rider-bond injuries.")
    ]

    roll_num = random.randint(1, 6)
    name, desc = disciplines[roll_num - 1]

    await ctx.send(
        f"**Healer Result**\n"
        f"Roll: **{roll_num}**\n"
        f"Healer Discipline: **{name}**\n"
        f"{desc}"
    )


@bot.command()
async def dragonspeak(ctx):
    approval = [
        "Your dragon rumbles low in approval.",
        "A warm pulse of satisfaction brushes through the bond.",
        "Your dragon lowers their head, clearly pleased.",
        "A proud huff escapes your dragon.",
        "Their tail flicks once in quiet approval.",
        "Your dragon's gaze sharpens with interest."
    ]

    disapproval = [
        "Your dragon lets out a sharp, irritated snort.",
        "A cold flash of disapproval cuts through the bond.",
        "Your dragon turns their head away, unimpressed.",
        "Their tail lashes once in annoyance.",
        "Your dragon's eyes narrow in clear judgment.",
        "A warning growl vibrates in their chest."
    ]

    if random.choice([True, False]):
        await ctx.send(f"**Dragon Approval**\n{random.choice(approval)}")
    else:
        await ctx.send(f"**Dragon Disapproval**\n{random.choice(disapproval)}")


@bot.command()
async def dragonaction(ctx):
    actions = [
        "Your dragon spreads their wings in a sudden display of dominance.",
        "Your dragon crouches low, ready to spring.",
        "Your dragon circles once, watching everything carefully.",
        "Your dragon gives a warning growl to everyone nearby.",
        "Your dragon nudges you with their snout.",
        "Your dragon snaps their teeth in irritation.",
        "Your dragon lifts their head and scents the air.",
        "Your dragon stalks a few steps forward, protective and alert.",
        "Your dragon curls their tail around themselves and waits.",
        "Your dragon lets out a sharp roar that silences the area."
    ]

    await ctx.send(f"**Dragon Action**\n{random.choice(actions)}")


@bot.command()
async def signet(ctx):
    roll = random.randint(1, 20)

    common_flavor = [
        "A steady warmth spreads through your veins as your dragon's power settles into you.",
        "The bond hums softly, controlled, grounded, and unmistakably yours.",
        "Power builds within you, quiet but constant, like a flame that will never go out.",
        "Your dragon's strength flows into you, shaping itself into something stable and reliable.",
        "The connection tightens, your abilities forming with deliberate, steady force."
    ]

    rare_flavor = [
        "Your dragon's power surges through you, wild, overwhelming, and impossible to ignore.",
        "The bond ignites violently, power cracking through you like lightning.",
        "Something ancient and immense awakens within you, far beyond control.",
        "The air itself seems to shift as your dragon's full strength floods your body.",
        "Your dragon's power doesn't settle, it erupts, claiming you completely."
    ]

    if roll >= 15:
        rarity = "**Once in a Lifetime Signet**"
        flavor = random.choice(rare_flavor)
    else:
        rarity = "**Common Signet**"
        flavor = random.choice(common_flavor)

    await ctx.send(
        f"**Signet Manifestation**\n"
        f"{flavor}\n\n"
        f"{rarity}"
    )

# -----------------------------
# CHARACTER CREATION COMMANDS
# -----------------------------
@bot.command(name="createcharacter", aliases=["character", "oc", "makecharacter"])
async def createcharacter(ctx, quadrant: str = None):
    try:
        profile = create_character_profile(quadrant)
    except RuntimeError as e:
        await ctx.send(f"**Character creation failed:** {e}")
        return

    for chunk in split_long_message(profile):
        await ctx.send(chunk)


@bot.command(name="charhelp")
async def charhelp(ctx):
    await ctx.send(
        "**Character Generator**\n"
        "`!createcharacter` → Generate a fully random character\n"
        "`!createcharacter riders` → Generate a rider\n"
        "`!createcharacter infantry` → Generate an infantry cadet\n"
        "`!createcharacter scribes` → Generate a scribe\n"
        "`!createcharacter healers` → Generate a healer"
    )

# -----------------------------
# DICE COMMANDS
# -----------------------------
VALID_DICE = [4, 6, 8, 10, 12, 20, 100]


@bot.command()
async def roll(ctx, dice: str = "d20"):
    match = re.fullmatch(r"(\d*)d(\d+)([+-]\d+)?", dice.strip().lower())

    if not match:
        await ctx.send(
            "**Invalid roll format.**\n"
            "Use examples like:\n"
            "`!roll d4`\n"
            "`!roll d6`\n"
            "`!roll d8`\n"
            "`!roll d10`\n"
            "`!roll d12`\n"
            "`!roll d20`\n"
            "`!roll d100`\n"
            "`!roll 2d6`\n"
            "`!roll 1d20+3`"
        )
        return

    num = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0

    if sides not in VALID_DICE:
        await ctx.send("Use a standard D&D die: `d4`, `d6`, `d8`, `d10`, `d12`, `d20`, or `d100`.")
        return

    if num < 1 or num > 100:
        await ctx.send("You can roll between 1 and 100 dice at once.")
        return

    rolls = [random.randint(1, sides) for _ in range(num)]
    subtotal = sum(rolls)
    total = subtotal + modifier

    if modifier > 0:
        mod_text = f" + {modifier}"
    elif modifier < 0:
        mod_text = f" - {abs(modifier)}"
    else:
        mod_text = ""

    await ctx.send(
        f"**Dice Roll: {dice.lower()}**\n"
        f"Rolls: **{rolls}**\n"
        f"Total: **{subtotal}{mod_text} = {total}**"
    )


@bot.command()
async def d4(ctx):
    await ctx.send(f"**d4 Roll**\nYou rolled: **{random.randint(1, 4)}**")


@bot.command()
async def d6(ctx):
    await ctx.send(f"**d6 Roll**\nYou rolled: **{random.randint(1, 6)}**")


@bot.command()
async def d8(ctx):
    await ctx.send(f"**d8 Roll**\nYou rolled: **{random.randint(1, 8)}**")


@bot.command()
async def d10(ctx):
    await ctx.send(f"**d10 Roll**\nYou rolled: **{random.randint(1, 10)}**")


@bot.command()
async def d12(ctx):
    await ctx.send(f"**d12 Roll**\nYou rolled: **{random.randint(1, 12)}**")


@bot.command()
async def d20(ctx):
    await ctx.send(f"**d20 Roll**\nYou rolled: **{random.randint(1, 20)}**")


@bot.command()
async def d100(ctx):
    await ctx.send(f"**d100 Roll**\nYou rolled: **{random.randint(1, 100)}**")

# -----------------------------
# RIDER FORMATION HELPERS
# -----------------------------
def find_existing_rider_assignment(data, name):
    target = normalize_name(name)

    for wing in data.values():
        if wing["wingleader"] and normalize_name(wing["wingleader"]) == target:
            return True

        if wing["executive_officer"] and normalize_name(wing["executive_officer"]) == target:
            return True

        for section in wing["sections"].values():
            if section["section_leader"] and normalize_name(section["section_leader"]) == target:
                return True

            if section["executive_officer"] and normalize_name(section["executive_officer"]) == target:
                return True

            for squad in section["squads"].values():
                if squad["squad_leader"] and normalize_name(squad["squad_leader"]) == target:
                    return True

                if squad["executive_squad_leader"] and normalize_name(squad["executive_squad_leader"]) == target:
                    return True

                if target in [normalize_name(cadet) for cadet in squad["cadets"]]:
                    return True

    return False


def get_open_rider_slots(data):
    slots = []

    for wing_name, wing in data.items():
        if wing["wingleader"] is None:
            slots.append(("Wingleader", wing_name))

        if wing["executive_officer"] is None:
            slots.append(("Wing Executive Officer", wing_name))

        for section_name, section in wing["sections"].items():
            if section["section_leader"] is None:
                slots.append(("Section Leader", wing_name, section_name))

            if section["executive_officer"] is None:
                slots.append(("Section Executive Officer", wing_name, section_name))

            for squad_name, squad in section["squads"].items():
                if squad["squad_leader"] is None:
                    slots.append(("Squad Leader", wing_name, section_name, squad_name))

                if squad["executive_squad_leader"] is None:
                    slots.append(("Executive Squad Leader", wing_name, section_name, squad_name))

                if len(squad["cadets"]) < 3:
                    slots.append(("Cadet", wing_name, section_name, squad_name))

    return slots


def assign_rider_slot(data, name, slot):
    role = slot[0]
    wing_name = slot[1]
    wing = data[wing_name]

    if role == "Wingleader":
        wing["wingleader"] = name
    elif role == "Wing Executive Officer":
        wing["executive_officer"] = name
    elif role == "Section Leader":
        section_name = slot[2]
        wing["sections"][section_name]["section_leader"] = name
    elif role == "Section Executive Officer":
        section_name = slot[2]
        wing["sections"][section_name]["executive_officer"] = name
    elif role == "Squad Leader":
        section_name = slot[2]
        squad_name = slot[3]
        wing["sections"][section_name]["squads"][squad_name]["squad_leader"] = name
    elif role == "Executive Squad Leader":
        section_name = slot[2]
        squad_name = slot[3]
        wing["sections"][section_name]["squads"][squad_name]["executive_squad_leader"] = name
    elif role == "Cadet":
        section_name = slot[2]
        squad_name = slot[3]
        wing["sections"][section_name]["squads"][squad_name]["cadets"].append(name)


def manual_assign_rider_slot(data, name, role, wing_name, section_name=None, squad_name=None):
    if wing_name not in data:
        return "That wing does not exist."

    wing = data[wing_name]

    if role == "Wingleader":
        if wing["wingleader"] is not None:
            return f"{wing_name} already has a Wingleader."
        wing["wingleader"] = name
        return None

    if role == "Wing Executive Officer":
        if wing["executive_officer"] is not None:
            return f"{wing_name} already has a Wing Executive Officer."
        wing["executive_officer"] = name
        return None

    if section_name is None:
        return "That role needs a section."

    if section_name not in wing["sections"]:
        return "That section does not exist in that wing."

    section = wing["sections"][section_name]

    if role == "Section Leader":
        if section["section_leader"] is not None:
            return f"{wing_name} → {section_name} already has a Section Leader."
        section["section_leader"] = name
        return None

    if role == "Section Executive Officer":
        if section["executive_officer"] is not None:
            return f"{wing_name} → {section_name} already has a Section Executive Officer."
        section["executive_officer"] = name
        return None

    if squad_name is None:
        return "That role needs a squad."

    if squad_name not in section["squads"]:
        return "That squad does not exist in that section."

    squad = section["squads"][squad_name]

    if role == "Squad Leader":
        if squad["squad_leader"] is not None:
            return f"{wing_name} → {section_name} → {squad_name} already has a Squad Leader."
        squad["squad_leader"] = name
        return None

    if role == "Executive Squad Leader":
        if squad["executive_squad_leader"] is not None:
            return f"{wing_name} → {section_name} → {squad_name} already has an Executive Squad Leader."
        squad["executive_squad_leader"] = name
        return None

    if role == "Cadet":
        if len(squad["cadets"]) >= 3:
            return f"{wing_name} → {section_name} → {squad_name} already has 3 cadets."
        squad["cadets"].append(name)
        return None

    return "That role is not valid."


def format_rider_assignment(name, slot):
    role = slot[0]
    path = " → ".join(slot[1:])
    return f"**{name}** assigned as **{role}** in **{path}**."


def format_manual_rider_assignment(name, role, wing_name, section_name=None, squad_name=None):
    parts = [wing_name]
    if section_name:
        parts.append(section_name)
    if squad_name:
        parts.append(squad_name)
    return f"**{name}** manually assigned as **{role}** in **{' → '.join(parts)}**."


def remove_rider(data, name):
    target = normalize_name(name)

    for wing_name, wing in data.items():
        if wing["wingleader"] and normalize_name(wing["wingleader"]) == target:
            wing["wingleader"] = None
            return f"Removed **{name}** from **Wingleader** in **{wing_name}**."

        if wing["executive_officer"] and normalize_name(wing["executive_officer"]) == target:
            wing["executive_officer"] = None
            return f"Removed **{name}** from **Wing Executive Officer** in **{wing_name}**."

        for section_name, section in wing["sections"].items():
            if section["section_leader"] and normalize_name(section["section_leader"]) == target:
                section["section_leader"] = None
                return f"Removed **{name}** from **Section Leader** in **{wing_name} → {section_name}**."

            if section["executive_officer"] and normalize_name(section["executive_officer"]) == target:
                section["executive_officer"] = None
                return f"Removed **{name}** from **Section Executive Officer** in **{wing_name} → {section_name}**."

            for squad_name, squad in section["squads"].items():
                if squad["squad_leader"] and normalize_name(squad["squad_leader"]) == target:
                    squad["squad_leader"] = None
                    return f"Removed **{name}** from **Squad Leader** in **{wing_name} → {section_name} → {squad_name}**."

                if squad["executive_squad_leader"] and normalize_name(squad["executive_squad_leader"]) == target:
                    squad["executive_squad_leader"] = None
                    return f"Removed **{name}** from **Executive Squad Leader** in **{wing_name} → {section_name} → {squad_name}**."

                for cadet in squad["cadets"]:
                    if normalize_name(cadet) == target:
                        squad["cadets"].remove(cadet)
                        return f"Removed **{name}** from **Cadet** in **{wing_name} → {section_name} → {squad_name}**."

    return None


def format_taken_riders(data):
    lines = []

    for wing_name, wing in data.items():
        wing_lines = []

        if wing["wingleader"]:
            wing_lines.append(f"Wingleader: {wing['wingleader']}")

        if wing["executive_officer"]:
            wing_lines.append(f"Executive Officer: {wing['executive_officer']}")

        for section_name, section in wing["sections"].items():
            if section["section_leader"]:
                wing_lines.append(f"{section_name} Section Leader: {section['section_leader']}")

            if section["executive_officer"]:
                wing_lines.append(f"{section_name} Executive Officer: {section['executive_officer']}")

            for squad_name, squad in section["squads"].items():
                if squad["squad_leader"]:
                    wing_lines.append(f"{section_name} {squad_name} Leader: {squad['squad_leader']}")

                if squad["executive_squad_leader"]:
                    wing_lines.append(f"{section_name} {squad_name} Exec: {squad['executive_squad_leader']}")

                if squad["cadets"]:
                    wing_lines.append(f"{section_name} {squad_name} Cadets: {', '.join(squad['cadets'])}")

        if wing_lines:
            lines.append(f"**{wing_name}**")
            lines.extend(wing_lines)
            lines.append("")

    return "\n".join(lines).strip() if lines else "No assignments yet."

# -----------------------------
# SIMPLE QUADRANT HELPERS
# -----------------------------
def find_name_in_simple_structure(data, name, lowest_plural):
    target = normalize_name(name)

    for assigned_name in data["_chain"].values():
        if assigned_name and normalize_name(assigned_name) == target:
            return True

    for group_name, group in data.items():
        if group_name == "_chain":
            continue

        for role_name, assigned_name in group.items():
            if role_name == lowest_plural:
                if target in [normalize_name(x) for x in assigned_name]:
                    return True
            else:
                if assigned_name and normalize_name(assigned_name) == target:
                    return True

    return False


def get_simple_open_slots(data, highest_roles, group_roles, lowest_singular, lowest_plural):
    slots = []

    for role in highest_roles:
        if data["_chain"][role] is None:
            slots.append((role, "_chain"))

    for group_name, group in data.items():
        if group_name == "_chain":
            continue

        for role in group_roles:
            if group[role] is None:
                slots.append((role, group_name))

        if len(group[lowest_plural]) < 3:
            slots.append((lowest_singular, group_name))

    return slots


def assign_simple_slot(data, name, slot, lowest_singular, lowest_plural):
    role, group_name = slot

    if group_name == "_chain":
        data["_chain"][role] = name
        return

    if role == lowest_singular:
        data[group_name][lowest_plural].append(name)
    else:
        data[group_name][role] = name


def remove_from_simple_structure(data, name, lowest_plural):
    target = normalize_name(name)

    for role_name, assigned_name in data["_chain"].items():
        if assigned_name and normalize_name(assigned_name) == target:
            data["_chain"][role_name] = None
            return f"Removed **{name}** from **{role_name}**."

    for group_name, group in data.items():
        if group_name == "_chain":
            continue

        for role_name, assigned_name in group.items():
            if role_name == lowest_plural:
                for entry in group[lowest_plural]:
                    if normalize_name(entry) == target:
                        group[lowest_plural].remove(entry)
                        singular_name = lowest_plural[:-1] if lowest_plural.endswith("s") else lowest_plural
                        return f"Removed **{name}** from **{singular_name}**."
            else:
                if assigned_name and normalize_name(assigned_name) == target:
                    group[role_name] = None
                    return f"Removed **{name}** from **{role_name}**."

    return None


def format_hidden_assignment(name, slot):
    role = slot[0]
    return f"**{name}** assigned as **{role}**."


def format_simple_taken(data, lowest_label):
    lines = []

    chain_lines = []
    for role_name, assigned_name in data["_chain"].items():
        if assigned_name:
            chain_lines.append(f"{role_name}: {assigned_name}")

    if chain_lines:
        lines.append("**High Chain**")
        lines.extend(chain_lines)
        lines.append("")

    for group_name, group in data.items():
        if group_name == "_chain":
            continue

        group_lines = []

        for role_name, assigned_name in group.items():
            if isinstance(assigned_name, list):
                if assigned_name:
                    group_lines.append(f"{lowest_label}: {', '.join(assigned_name)}")
            else:
                if assigned_name:
                    group_lines.append(f"{role_name}: {assigned_name}")

        if group_lines:
            lines.append(f"**{group_name}**")
            lines.extend(group_lines)
            lines.append("")

    return "\n".join(lines).strip() if lines else "No assignments yet."

# -----------------------------
# SIMPLE MANUAL ASSIGN HELPERS
# -----------------------------
def manual_assign_simple(data, name, role, group_name, highest_roles, group_roles, lowest_singular, lowest_plural):
    if role in highest_roles:
        if data["_chain"][role] is not None:
            return f"There is already someone assigned as **{role}**."
        data["_chain"][role] = name
        return None

    if group_name is None:
        return "That role needs a division/order/circle."

    if group_name not in data or group_name == "_chain":
        return "That group does not exist."

    if role == lowest_singular:
        if len(data[group_name][lowest_plural]) >= 3:
            return f"**{group_name}** already has 3 {lowest_plural.lower()}."
        data[group_name][lowest_plural].append(name)
        return None

    if role in group_roles:
        if data[group_name][role] is not None:
            return f"**{group_name}** already has a **{role}**."
        data[group_name][role] = name
        return None

    return "That role is not valid."

# -----------------------------
# RIDER FORMATION COMMANDS
# -----------------------------
@bot.command()
async def assignrider(ctx, *, name: str):
    global rider_data

    if find_existing_rider_assignment(rider_data, name):
        await ctx.send(f"**{name}** is already assigned.")
        return

    slots = get_open_rider_slots(rider_data)

    if not slots:
        await ctx.send("No rider slots left.")
        return

    slot = random.choice(slots)
    assign_rider_slot(rider_data, name, slot)
    save_json_file(RIDER_FILE, rider_data)

    await ctx.send(format_rider_assignment(name, slot))


@bot.command()
async def manualassign(ctx, *, args: str):
    global rider_data

    parts = [part.strip() for part in args.split("|")]

    if len(parts) < 3:
        await ctx.send(
            "**Use:** `!manualassign name | role | wing | section | squad`\n"
            "Only include section and squad if the role needs them."
        )
        return

    name = parts[0]
    role = parts[1]
    wing_name = parts[2]
    section_name = parts[3] if len(parts) >= 4 and parts[3] else None
    squad_name = parts[4] if len(parts) >= 5 and parts[4] else None

    if find_existing_rider_assignment(rider_data, name):
        await ctx.send(f"**{name}** is already assigned. Remove or reassign them first.")
        return

    error = manual_assign_rider_slot(rider_data, name, role, wing_name, section_name, squad_name)

    if error:
        await ctx.send(error)
        return

    save_json_file(RIDER_FILE, rider_data)
    await ctx.send(format_manual_rider_assignment(name, role, wing_name, section_name, squad_name))


@bot.command()
async def removerider(ctx, *, name: str):
    global rider_data

    result = remove_rider(rider_data, name)

    if result is None:
        await ctx.send(f"Could not find **{name}** in the rider formation.")
        return

    save_json_file(RIDER_FILE, rider_data)
    await ctx.send(result)


@bot.command()
async def reassignrider(ctx, *, name: str):
    global rider_data

    removed = remove_rider(rider_data, name)

    if removed is None:
        await ctx.send(f"Could not find **{name}** in the rider formation.")
        return

    slots = get_open_rider_slots(rider_data)

    if not slots:
        save_json_file(RIDER_FILE, rider_data)
        await ctx.send(f"{removed}\nNo open slots left to reassign them.")
        return

    slot = random.choice(slots)
    assign_rider_slot(rider_data, name, slot)
    save_json_file(RIDER_FILE, rider_data)

    await ctx.send(f"{removed}\n{format_rider_assignment(name, slot)}")


@bot.command()
async def riderslots(ctx):
    output = format_taken_riders(rider_data)
    for chunk in split_long_message(output):
        await ctx.send(chunk)


@bot.command()
async def resetriders(ctx):
    global rider_data
    rider_data = copy.deepcopy(DEFAULT_RIDER_STRUCTURE)
    save_json_file(RIDER_FILE, rider_data)
    await ctx.send("Rider formation has been reset.")

# -----------------------------
# INFANTRY FORMATION COMMANDS
# -----------------------------
@bot.command()
async def assigninfantry(ctx, *, name: str):
    global infantry_data

    if find_name_in_simple_structure(infantry_data, name, "Cadets"):
        await ctx.send(f"**{name}** is already assigned in infantry.")
        return

    slots = get_simple_open_slots(
        infantry_data,
        ["High Commander", "Commander"],
        ["Captain", "Sergeant", "Corporal", "Soldier"],
        "Cadet",
        "Cadets"
    )

    if not slots:
        await ctx.send("No infantry slots left.")
        return

    slot = random.choice(slots)
    assign_simple_slot(infantry_data, name, slot, "Cadet", "Cadets")
    save_json_file(INFANTRY_FILE, infantry_data)

    await ctx.send(format_hidden_assignment(name, slot))


@bot.command()
async def manualinfantry(ctx, *, args: str):
    global infantry_data

    parts = [p.strip() for p in args.split("|")]

    if len(parts) < 2:
        await ctx.send("Use: `!manualinfantry name | role | division`")
        return

    name = parts[0]
    role = parts[1]
    division = parts[2] if len(parts) >= 3 and parts[2] else None

    if find_name_in_simple_structure(infantry_data, name, "Cadets"):
        await ctx.send(f"**{name}** is already assigned in infantry.")
        return

    error = manual_assign_simple(
        infantry_data,
        name,
        role,
        division,
        ["High Commander", "Commander"],
        ["Captain", "Sergeant", "Corporal", "Soldier"],
        "Cadet",
        "Cadets"
    )

    if error:
        await ctx.send(error)
        return

    save_json_file(INFANTRY_FILE, infantry_data)
    await ctx.send(f"⚔️ **{name}** manually assigned as **{role}**.")


@bot.command()
async def removeinfantry(ctx, *, name: str):
    global infantry_data

    result = remove_from_simple_structure(infantry_data, name, "Cadets")

    if result is None:
        await ctx.send(f"Could not find **{name}** in infantry.")
        return

    save_json_file(INFANTRY_FILE, infantry_data)
    await ctx.send(result)


@bot.command()
async def reassigninfantry(ctx, *, name: str):
    global infantry_data

    removed = remove_from_simple_structure(infantry_data, name, "Cadets")

    if removed is None:
        await ctx.send(f"Could not find **{name}** in infantry.")
        return

    slots = get_simple_open_slots(
        infantry_data,
        ["High Commander", "Commander"],
        ["Captain", "Sergeant", "Corporal", "Soldier"],
        "Cadet",
        "Cadets"
    )

    if not slots:
        save_json_file(INFANTRY_FILE, infantry_data)
        await ctx.send(f"{removed}\nNo open infantry slots left.")
        return

    slot = random.choice(slots)
    assign_simple_slot(infantry_data, name, slot, "Cadet", "Cadets")
    save_json_file(INFANTRY_FILE, infantry_data)

    await ctx.send(f"{removed}\n{format_hidden_assignment(name, slot)}")


@bot.command()
async def infantryslots(ctx):
    output = format_simple_taken(infantry_data, "Cadets")
    for chunk in split_long_message(output):
        await ctx.send(chunk)


@bot.command()
async def resetinfantry(ctx):
    global infantry_data
    infantry_data = copy.deepcopy(DEFAULT_INFANTRY_STRUCTURE)
    save_json_file(INFANTRY_FILE, infantry_data)
    await ctx.send("Infantry formation has been reset.")

# -----------------------------
# SCRIBE FORMATION COMMANDS
# -----------------------------
@bot.command()
async def assignscribe(ctx, *, name: str):
    global scribe_data

    if find_name_in_simple_structure(scribe_data, name, "Scribes"):
        await ctx.send(f"**{name}** is already assigned in the scribes quadrant.")
        return

    slots = get_simple_open_slots(
        scribe_data,
        ["Grand Maester", "Head Archivist"],
        ["Master Scholar", "Curator", "Archivist", "Senior Scribe"],
        "Scribe",
        "Scribes"
    )

    if not slots:
        await ctx.send("No scribe slots left.")
        return

    slot = random.choice(slots)
    assign_simple_slot(scribe_data, name, slot, "Scribe", "Scribes")
    save_json_file(SCRIBE_FILE, scribe_data)

    await ctx.send(format_hidden_assignment(name, slot))


@bot.command()
async def manualscribe(ctx, *, args: str):
    global scribe_data

    parts = [p.strip() for p in args.split("|")]

    if len(parts) < 2:
        await ctx.send("Use: `!manualscribe name | role | order`")
        return

    name = parts[0]
    role = parts[1]
    order = parts[2] if len(parts) >= 3 and parts[2] else None

    if find_name_in_simple_structure(scribe_data, name, "Scribes"):
        await ctx.send(f"**{name}** is already assigned in the scribes quadrant.")
        return

    error = manual_assign_simple(
        scribe_data,
        name,
        role,
        order,
        ["Grand Maester", "Head Archivist"],
        ["Master Scholar", "Curator", "Archivist", "Senior Scribe"],
        "Scribe",
        "Scribes"
    )

    if error:
        await ctx.send(error)
        return

    save_json_file(SCRIBE_FILE, scribe_data)
    await ctx.send(f"📚 **{name}** manually assigned as **{role}**.")


@bot.command()
async def removescribe(ctx, *, name: str):
    global scribe_data

    result = remove_from_simple_structure(scribe_data, name, "Scribes")

    if result is None:
        await ctx.send(f"Could not find **{name}** in the scribes quadrant.")
        return

    save_json_file(SCRIBE_FILE, scribe_data)
    await ctx.send(result)


@bot.command()
async def reassignscribe(ctx, *, name: str):
    global scribe_data

    removed = remove_from_simple_structure(scribe_data, name, "Scribes")

    if removed is None:
        await ctx.send(f"Could not find **{name}** in the scribes quadrant.")
        return

    slots = get_simple_open_slots(
        scribe_data,
        ["Grand Maester", "Head Archivist"],
        ["Master Scholar", "Curator", "Archivist", "Senior Scribe"],
        "Scribe",
        "Scribes"
    )

    if not slots:
        save_json_file(SCRIBE_FILE, scribe_data)
        await ctx.send(f"{removed}\nNo open scribe slots left.")
        return

    slot = random.choice(slots)
    assign_simple_slot(scribe_data, name, slot, "Scribe", "Scribes")
    save_json_file(SCRIBE_FILE, scribe_data)

    await ctx.send(f"{removed}\n{format_hidden_assignment(name, slot)}")


@bot.command()
async def scribeslots(ctx):
    output = format_simple_taken(scribe_data, "Scribes")
    for chunk in split_long_message(output):
        await ctx.send(chunk)


@bot.command()
async def resetscribes(ctx):
    global scribe_data
    scribe_data = copy.deepcopy(DEFAULT_SCRIBE_STRUCTURE)
    save_json_file(SCRIBE_FILE, scribe_data)
    await ctx.send("Scribe formation has been reset.")

# -----------------------------
# HEALER FORMATION COMMANDS
# -----------------------------
@bot.command()
async def assignhealer(ctx, *, name: str):
    global healer_data

    if find_name_in_simple_structure(healer_data, name, "Trainees"):
        await ctx.send(f"**{name}** is already assigned in healers.")
        return

    slots = get_simple_open_slots(
        healer_data,
        ["Arch Healer", "Healer"],
        ["Senior Practitioner", "Practitioner", "Medic", "Acolyte"],
        "Trainee",
        "Trainees"
    )

    if not slots:
        await ctx.send("No healer slots left.")
        return

    slot = random.choice(slots)
    assign_simple_slot(healer_data, name, slot, "Trainee", "Trainees")
    save_json_file(HEALER_FILE, healer_data)

    await ctx.send(format_hidden_assignment(name, slot))


@bot.command()
async def manualhealer(ctx, *, args: str):
    global healer_data

    parts = [p.strip() for p in args.split("|")]

    if len(parts) < 2:
        await ctx.send("Use: `!manualhealer name | role | circle`")
        return

    name = parts[0]
    role = parts[1]
    circle = parts[2] if len(parts) >= 3 and parts[2] else None

    if find_name_in_simple_structure(healer_data, name, "Trainees"):
        await ctx.send(f"**{name}** is already assigned in healers.")
        return

    error = manual_assign_simple(
        healer_data,
        name,
        role,
        circle,
        ["Arch Healer", "Healer"],
        ["Senior Practitioner", "Practitioner", "Medic", "Acolyte"],
        "Trainee",
        "Trainees"
    )

    if error:
        await ctx.send(error)
        return

    save_json_file(HEALER_FILE, healer_data)
    await ctx.send(f"🌿 **{name}** manually assigned as **{role}**.")


@bot.command()
async def removehealer(ctx, *, name: str):
    global healer_data

    result = remove_from_simple_structure(healer_data, name, "Trainees")

    if result is None:
        await ctx.send(f"Could not find **{name}** in healers.")
        return

    save_json_file(HEALER_FILE, healer_data)
    await ctx.send(result)


@bot.command()
async def reassignhealer(ctx, *, name: str):
    global healer_data

    removed = remove_from_simple_structure(healer_data, name, "Trainees")

    if removed is None:
        await ctx.send(f"Could not find **{name}** in healers.")
        return

    slots = get_simple_open_slots(
        healer_data,
        ["Arch Healer", "Healer"],
        ["Senior Practitioner", "Practitioner", "Medic", "Acolyte"],
        "Trainee",
        "Trainees"
    )

    if not slots:
        save_json_file(HEALER_FILE, healer_data)
        await ctx.send(f"{removed}\nNo open healer slots left.")
        return

    slot = random.choice(slots)
    assign_simple_slot(healer_data, name, slot, "Trainee", "Trainees")
    save_json_file(HEALER_FILE, healer_data)

    await ctx.send(f"{removed}\n{format_hidden_assignment(name, slot)}")


@bot.command()
async def healerslots(ctx):
    output = format_simple_taken(healer_data, "Trainees")
    for chunk in split_long_message(output):
        await ctx.send(chunk)


@bot.command()
async def resethealers(ctx):
    global healer_data
    healer_data = copy.deepcopy(DEFAULT_HEALER_STRUCTURE)
    save_json_file(HEALER_FILE, healer_data)
    await ctx.send("Healer formation has been reset.")


# -----------------------------
# GAUNTLET + MAT COMMANDS
# -----------------------------
GAUNTLET_OBSTACLES = [
    "a rain-slick beam that narrows halfway across",
    "a broken ladder missing two key rungs",
    "a swinging rope over an open drop",
    "a cracked stone ledge with barely enough room for your boots",
    "a vertical climb with loose handholds",
    "a narrow bridge shuddering in the wind",
    "a sequence of uneven platforms set too far apart",
    "a warped beam angled over open air",
    "a shattered stair run with gaps between steps",
    "a hanging chain route that bites cold into your hands",
    "a low crawl through splintered supports",
    "a blind turn where the only way forward is a jump"
]

GAUNTLET_APPROACHES = [
    "moves with careful precision, testing every foothold before committing",
    "pushes forward fast, trusting momentum over caution",
    "keeps low and balanced, refusing to waste a single motion",
    "takes the riskier path to gain time",
    "pauses just long enough to study the structure, then commits",
    "uses brute determination rather than grace",
    "keeps their breathing even and their focus brutally narrow",
    "recovers quickly from a slip and keeps moving",
    "treats the whole run like a fight to be won",
    "leans into instinct, moving before fear can settle in"
]

GAUNTLET_COMPLICATIONS = [
    "A board shifts under their weight.",
    "A crosswind hits at the worst possible moment.",
    "Their grip slips for one sickening second.",
    "Another cadet's earlier mistake has left debris in the way.",
    "Their shoulder clips a support hard enough to bruise.",
    "The next foothold is farther than it first looked.",
    "The route creaks loud enough to rattle everyone's nerves.",
    "A boot skids on damp wood.",
    "Their hand catches a splintered edge.",
    "They have to choose between speed and balance in a heartbeat."
]

GAUNTLET_OUTCOMES = [
    "They make it across cleanly.",
    "They stumble at the end but recover before falling.",
    "They finish hard, scraped up, and breathing like they've swallowed fire.",
    "They clear the obstacle with seconds to spare.",
    "They hang for a terrifying moment, then haul themselves up.",
    "They fall short, catch themselves, and drag their weight back into position.",
    "They miss the clean route and force their way through on sheer stubbornness.",
    "They go down, hit a lower level, and have to start again from there.",
    "They freeze for half a breath, then choose motion over fear.",
    "They fail the obstacle and drop out of the run."
]

GAUNTLET_INJURIES = [
    "bloody palms",
    "a twisted wrist",
    "a bruised rib",
    "a torn sleeve and a cut shoulder",
    "splinters buried in one hand",
    "a badly scraped knee",
    "a cracked lip from hitting a beam",
    "a wrenched ankle",
    "a deep bruise across the back",
    "shaking hands they can't quite steady"
]

GAUNTLET_FLAVOR = [
    "Below, the stones wait without mercy.",
    "The whole structure groans like it wants them dead.",
    "Every cadet behind them feels the pressure of the delay.",
    "One mistake is all the Gauntlet ever needs.",
    "The wind turns the height into its own kind of enemy.",
    "No one speaks. No one needs to.",
    "Failure here is public, immediate, and unforgettable.",
    "For one brutal stretch of time, there is only the next move."
]

MAT_CHALLENGES = [
    "knife disarm drill",
    "close-combat spar",
    "shield-break exercise",
    "grappling round",
    "speed-and-footwork bout",
    "endurance spar",
    "wooden blade match",
    "paired takedown drill",
    "reaction test",
    "two-minute pressure round"
]


def collect_active_rider_names(data):
    names = []

    for wing in data.values():
        if wing["wingleader"]:
            names.append(wing["wingleader"])
        if wing["executive_officer"]:
            names.append(wing["executive_officer"])

        for section in wing["sections"].values():
            if section["section_leader"]:
                names.append(section["section_leader"])
            if section["executive_officer"]:
                names.append(section["executive_officer"])

            for squad in section["squads"].values():
                if squad["squad_leader"]:
                    names.append(squad["squad_leader"])
                if squad["executive_squad_leader"]:
                    names.append(squad["executive_squad_leader"])
                names.extend(squad["cadets"])

    return names


def collect_active_infantry_names(data):
    names = []

    for assigned_name in data["_chain"].values():
        if assigned_name:
            names.append(assigned_name)

    for group_name, group in data.items():
        if group_name == "_chain":
            continue

        for assigned_name in group.values():
            if isinstance(assigned_name, list):
                names.extend(assigned_name)
            elif assigned_name:
                names.append(assigned_name)

    return names


def collect_active_mat_characters():
    seen = set()
    active = []

    for name in collect_active_rider_names(rider_data) + collect_active_infantry_names(infantry_data):
        normalized = normalize_name(name)
        if normalized not in seen:
            seen.add(normalized)
            active.append(name)

    return active


def make_mat_pairs(names):
    shuffled = names[:]
    random.shuffle(shuffled)
    pairs = []
    bye = None

    if len(shuffled) % 2 == 1:
        bye = shuffled.pop()

    for i in range(0, len(shuffled), 2):
        pairs.append((shuffled[i], shuffled[i + 1], random.choice(MAT_CHALLENGES)))

    return pairs, bye


@bot.command()
async def gauntlet(ctx):
    obstacle = random.choice(GAUNTLET_OBSTACLES)
    approach = random.choice(GAUNTLET_APPROACHES)
    complication = random.choice(GAUNTLET_COMPLICATIONS)
    outcome = random.choice(GAUNTLET_OUTCOMES)
    flavor = random.choice(GAUNTLET_FLAVOR)

    await ctx.send(
        f"**The Gauntlet**\n"
        f"Obstacle: **{obstacle}**\n"
        f"Approach: **{ctx.author.display_name}** {approach}.\n"
        f"Complication: **{complication}**\n"
        f"Outcome: **{outcome}**\n"
        f"{flavor}"
    )


@bot.command()
async def gauntlethazard(ctx):
    hazard = random.choice(GAUNTLET_OBSTACLES)
    complication = random.choice(GAUNTLET_COMPLICATIONS)
    await ctx.send(
        f"**Gauntlet Hazard**\n"
        f"The next obstacle is **{hazard}**.\n"
        f"Complication: **{complication}**"
    )


@bot.command()
async def gauntletaction(ctx):
    approach = random.choice(GAUNTLET_APPROACHES)
    flavor = random.choice(GAUNTLET_FLAVOR)
    await ctx.send(
        f"**Gauntlet Action**\n"
        f"**{ctx.author.display_name}** {approach}.\n"
        f"{flavor}"
    )


@bot.command()
async def gauntletinjury(ctx):
    injury = random.choice(GAUNTLET_INJURIES)
    await ctx.send(
        f"**Gauntlet Consequence**\n"
        f"The run leaves them with **{injury}**."
    )


@bot.command()
async def gauntletoutcome(ctx):
    outcome = random.choice(GAUNTLET_OUTCOMES)
    await ctx.send(
        f"**Gauntlet Outcome**\n"
        f"**{outcome}**"
    )


@bot.command(name="activemats")
async def activemats(ctx):
    active_names = collect_active_mat_characters()

    if not active_names:
        await ctx.send("No active rider or infantry characters found.")
        return

    lines = ["**Active Mat Pool**"]
    lines.extend([f"• {name}" for name in active_names])

    for chunk in split_long_message("\n".join(lines)):
        await ctx.send(chunk)


@bot.command(name="matpairs", aliases=["matchallenge", "mats"])
async def matpairs(ctx):
    active_names = collect_active_mat_characters()

    if len(active_names) < 2:
        await ctx.send("Not enough active rider and infantry characters to make mat pairings.")
        return

    pairs, bye = make_mat_pairs(active_names)
    lines = ["**Mat Challenge Pairings**"]

    for index, (first, second, challenge) in enumerate(pairs, start=1):
        lines.append(f"{index}. **{first}** vs **{second}** : {challenge}")

    if bye:
        lines.append("")
        lines.append(f"**Unpaired this round:** {bye}")

    for chunk in split_long_message("\n".join(lines)):
        await ctx.send(chunk)


# -----------------------------
# FIGHT COMMANDS
# -----------------------------
@bot.command()
async def fight(ctx, *, args: str):
    global fight_records

    parts = [part.strip() for part in args.split("|")]
    if len(parts) != 2 or not parts[0] or not parts[1]:
        await ctx.send("Use: `!fight character one | character two`")
        return

    char_one = resolve_active_character(parts[0])
    char_two = resolve_active_character(parts[1])

    if not char_one:
        await ctx.send(f"Could not find an active character named **{parts[0]}**.")
        return

    if not char_two:
        await ctx.send(f"Could not find an active character named **{parts[1]}**.")
        return

    if normalize_name(char_one["name"]) == normalize_name(char_two["name"]):
        await ctx.send("A character cannot fight themselves.")
        return

    roll_one = random.randint(1, 20)
    roll_two = random.randint(1, 20)

    if roll_one > roll_two:
        result_text = f"**Winner:** {char_one['name']}"
        outcome_one = "win"
        outcome_two = "loss"
    elif roll_two > roll_one:
        result_text = f"**Winner:** {char_two['name']}"
        outcome_one = "loss"
        outcome_two = "win"
    else:
        result_text = "**Result:** Draw"
        outcome_one = "draw"
        outcome_two = "draw"

    record_fight_result(char_one["name"], char_two["name"], roll_one, roll_two, outcome_one)
    record_fight_result(char_two["name"], char_one["name"], roll_two, roll_one, outcome_two)
    save_json_file(FIGHT_FILE, fight_records)

    await ctx.send(
        f"**Mat Challenge**\n"
        f"{char_one['name']}: **{roll_one}**\n"
        f"{char_two['name']}: **{roll_two}**\n"
        f"{result_text}"
    )


@bot.command(aliases=["fightrecord", "record", "fights"])
async def fightlog(ctx, *, name: str):
    output = format_fight_log(name)
    if output is None:
        await ctx.send(f"Could not find any character or fight record for **{name}**.")
        return

    for chunk in split_long_message(output):
        await ctx.send(chunk)


@bot.command()
async def masterboard(ctx):
    output = format_masterboard()
    for chunk in split_long_message(output):
        await ctx.send(chunk)


# -----------------------------
# HELP COMMAND
# -----------------------------
@bot.command()
async def rphelp(ctx):
    help_text = """**📖 Basgaith Command List**

**Creating A Character By Hand**
> For Riders
`!threshing` → Roll dragon color + tail
`!assignrider name` → Assign a rider to a random open slot
`!manualassign name | role | wing | section | squad` → Manually assign a rider
`!removerider name` → Remove one rider
`!reassignrider name` → Remove and reroll one rider
`!riderslots` → Show filled rider slots


** Interacting with your Dragon**
`!dragonspeak` → Dragon approval or disapproval
`!dragonaction` → Random dragon action

**✨ Signets**
`!signet` → Manifest your signet

**🪵 The Gauntlet**
`!gauntlet` → Full Gauntlet obstacle + complication + outcome
`!gauntlethazard` → Roll the next obstacle
`!gauntletaction` → Roll a Gauntlet action beat
`!gauntletinjury` → Roll an injury or consequence
`!gauntletoutcome` → Roll the final result

**🥊 Mat Challenges**
`!activemats` → Show all active rider + infantry characters in the mat pool
`!matpairs` → Randomly pair every active rider + infantry character for mat challenges

**🧾 Character Creation**
`!createcharacter` → Fully random character
`!createcharacter riders` → Rider character
`!createcharacter infantry` → Infantry character
`!createcharacter scribes` → Scribe character
`!createcharacter healers` → Healer character

**The Quadrants**
`!infantry` → Roll for a combat specialty
`!scribe` → Roll for a subject specialty
`!healer` → Roll for a healer discipline


**⚔️ Infantry Formation**
`!assigninfantry name` → Assign infantry rank
`!manualinfantry name | role | division` → Manually assign infantry rank
`!removeinfantry name` → Remove infantry assignment
`!reassigninfantry name` → Reroll infantry rank
`!infantryslots` → Show filled infantry slots
`!resetinfantry` → Reset infantry formation

**📚 Scribe Formation**
`!assignscribe name` → Assign scribe rank
`!manualscribe name | role | order` → Manually assign scribe rank
`!removescribe name` → Remove scribe assignment
`!reassignscribe name` → Reroll scribe rank
`!scribeslots` → Show filled scribe slots
`!resetscribes` → Reset scribe formation

**🌿 Healer Formation**
`!assignhealer name` → Assign healer rank
`!manualhealer name | role | circle` → Manually assign healer rank
`!removehealer name` → Remove healer assignment
`!reassignhealer name` → Reroll healer rank
`!healerslots` → Show filled healer slots
`!resethealers` → Reset healer formation

**🎲 Standard D&D Dice**
`!d4`
`!d6`
`!d8`
`!d10`
`!d12`
`!d20`
`!d100`

**🎲 Custom Dice Rolls**
`!roll d4`
`!roll d6`
`!roll d8`
`!roll d10`
`!roll d12`
`!roll d20`
`!roll d100`
`!roll 2d6`
`!roll 1d20+3`
`!roll 2d8-1`"""
    for chunk in split_long_message(help_text):
        await ctx.send(chunk)

# -----------------------------
# RUN BOT
# -----------------------------
bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
