import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import re
import json
import copy

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
# RIDER FORMATION DATA
# -----------------------------
FORMATION_FILE = "rider_formation.json"

DEFAULT_STRUCTURE = {
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


def load_formation_data():
    if os.path.exists(FORMATION_FILE):
        with open(FORMATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return copy.deepcopy(DEFAULT_STRUCTURE)


def save_formation_data():
    with open(FORMATION_FILE, "w", encoding="utf-8") as f:
        json.dump(assignment_data, f, indent=4)


assignment_data = load_formation_data()

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
    await bot.process_commands(message)

# -----------------------------
# BASGAITH COMMANDS
# -----------------------------
@bot.command()
async def threshing(ctx):
    dragon_colors = [
        "Black",
        "Red", "Red",
        "Orange", "Orange",
        "Blue", "Blue",
        "Brown", "Brown",
        "Green", "Green"
    ]

    dragon_tails = [
        "Morningstar tail",
        "Swordtail", "Swordtail",
        "Scorpion tail", "Scorpion tail",
        "Club tail", "Club tail",
        "Daggertail", "Daggertail"
    ]

    await ctx.send(
        f"**Threshing Result**\n"
        f"Dragon Color: **{random.choice(dragon_colors)}**\n"
        f"Tail: **{random.choice(dragon_tails)}**"
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
        ("Archive", "Preservation of records, ancient texts, and restricted materials. Responsible for maintaining the Quadrant’s most valuable knowledge."),
        ("Chronicle", "Documentation of events, reports, and historical accounts. Tasked with recording truth as it happens."),
        ("Lexicon", "Languages, translation, and interpretation of foreign or coded texts. Essential for communication and deciphering unknown scripts."),
        ("Intelligence", "Information gathering, analysis, and strategic insight. Works closely with leadership to interpret and apply knowledge."),
        ("Cipher", "Codes, encryption, and protection of sensitive information. Ensures that what must remain hidden, stays hidden."),
        ("Restricted", "Forbidden knowledge and sealed records. Access is limited, and those assigned here operate under strict oversight.")
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
async def healing(ctx):
    disciplines = [
        ("Battlefield", "Healers trained to operate within active combat, prioritizing rapid stabilization under pressure."),
        ("Surgical", "Healers specializing in controlled, precision-based procedures requiring skill and exact technique."),
        ("Recovery", "Healers focused on long-term care, rehabilitation, and the restoration of strength over time."),
        ("Emergency", "Healers trained for critical intervention, where immediate action determines survival."),
        ("Experimental", "Healers who utilize unproven or evolving methods, often working beyond standard practice."),
        ("Dragonkind", "Healers trained to treat dragons and manage injuries tied to the rider bond.")
    ]

    roll_num = random.randint(1, 6)
    name, desc = disciplines[roll_num - 1]

    await ctx.send(
        f"**Healing Result**\n"
        f"Roll: **{roll_num}**\n"
        f"Healing Discipline: **{name}**\n"
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
        "Your dragon’s gaze sharpens with interest."
    ]

    disapproval = [
        "Your dragon lets out a sharp, irritated snort.",
        "A cold flash of disapproval cuts through the bond.",
        "Your dragon turns their head away, unimpressed.",
        "Their tail lashes once in annoyance.",
        "Your dragon’s eyes narrow in clear judgment.",
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
        "A steady warmth spreads through your veins as your dragon’s power settles into you.",
        "The bond hums softly—controlled, grounded, and unmistakably yours.",
        "Power builds within you, quiet but constant, like a flame that will never go out.",
        "Your dragon’s strength flows into you, shaping itself into something stable and reliable.",
        "The connection tightens, your abilities forming with deliberate, steady force."
    ]

    rare_flavor = [
        "Your dragon’s power surges through you—wild, overwhelming, and impossible to ignore.",
        "The bond ignites violently, power cracking through you like lightning.",
        "Something ancient and immense awakens within you, far beyond control.",
        "The air itself seems to shift as your dragon’s full strength floods your body.",
        "Your dragon’s power doesn’t settle—it erupts, claiming you completely."
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
    result = random.randint(1, 4)
    await ctx.send(f"**d4 Roll**\nYou rolled: **{result}**")


@bot.command()
async def d6(ctx):
    result = random.randint(1, 6)
    await ctx.send(f"**d6 Roll**\nYou rolled: **{result}**")


@bot.command()
async def d8(ctx):
    result = random.randint(1, 8)
    await ctx.send(f"**d8 Roll**\nYou rolled: **{result}**")


@bot.command()
async def d10(ctx):
    result = random.randint(1, 10)
    await ctx.send(f"**d10 Roll**\nYou rolled: **{result}**")


@bot.command()
async def d12(ctx):
    result = random.randint(1, 12)
    await ctx.send(f"**d12 Roll**\nYou rolled: **{result}**")


@bot.command()
async def d20(ctx):
    result = random.randint(1, 20)
    await ctx.send(f"**d20 Roll**\nYou rolled: **{result}**")


@bot.command()
async def d100(ctx):
    result = random.randint(1, 100)
    await ctx.send(f"**d100 Roll**\nYou rolled: **{result}**")

# -----------------------------
# RIDER FORMATION HELPERS
# -----------------------------
def normalize_name(name: str) -> str:
    return name.lower().strip()


def find_existing_assignment(data, name):
    target = normalize_name(name)

    for wing_name, wing in data.items():
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


def get_open_slots(data):
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


def assign_slot(data, name, slot):
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


def manual_assign_slot(data, name, role, wing_name, section_name=None, squad_name=None):
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


def format_assignment(name, slot):
    role = slot[0]
    path = " → ".join(slot[1:])
    return f"**{name}** assigned as **{role}** in **{path}**."


def format_manual_assignment(name, role, wing_name, section_name=None, squad_name=None):
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


def format_taken(data):
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
# RIDER FORMATION COMMANDS
# -----------------------------
@bot.command()
async def assignrider(ctx, *, name: str):
    global assignment_data

    if find_existing_assignment(assignment_data, name):
        await ctx.send(f"**{name}** is already assigned.")
        return

    slots = get_open_slots(assignment_data)

    if not slots:
        await ctx.send("No rider slots left.")
        return

    slot = random.choice(slots)
    assign_slot(assignment_data, name, slot)
    save_formation_data()

    await ctx.send(format_assignment(name, slot))


@bot.command()
async def manualassign(ctx, *, args: str):
    global assignment_data

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

    if find_existing_assignment(assignment_data, name):
        await ctx.send(f"**{name}** is already assigned. Remove or reassign them first.")
        return

    error = manual_assign_slot(
        assignment_data,
        name,
        role,
        wing_name,
        section_name,
        squad_name
    )

    if error:
        await ctx.send(error)
        return

    save_formation_data()
    await ctx.send(format_manual_assignment(name, role, wing_name, section_name, squad_name))


@bot.command()
async def removerider(ctx, *, name: str):
    global assignment_data

    result = remove_rider(assignment_data, name)

    if result is None:
        await ctx.send(f"Could not find **{name}** in the rider formation.")
        return

    save_formation_data()
    await ctx.send(result)


@bot.command()
async def reassignrider(ctx, *, name: str):
    global assignment_data

    removed = remove_rider(assignment_data, name)

    if removed is None:
        await ctx.send(f"Could not find **{name}** in the rider formation.")
        return

    slots = get_open_slots(assignment_data)

    if not slots:
        save_formation_data()
        await ctx.send(f"{removed}\nNo open slots left to reassign them.")
        return

    slot = random.choice(slots)
    assign_slot(assignment_data, name, slot)
    save_formation_data()

    await ctx.send(f"{removed}\n{format_assignment(name, slot)}")


@bot.command()
async def riderslots(ctx):
    output = format_taken(assignment_data)

    if len(output) <= 2000:
        await ctx.send(output)
    else:
        for i in range(0, len(output), 2000):
            await ctx.send(output[i:i + 2000])


@bot.command()
async def resetriders(ctx):
    global assignment_data
    assignment_data = copy.deepcopy(DEFAULT_STRUCTURE)
    save_formation_data()
    await ctx.send("Rider formation has been reset.")

# -----------------------------
# HELP COMMAND
# -----------------------------
@bot.command()
async def rphelp(ctx):
    await ctx.send(
        "**📖 Basgaith Command List**\n\n"

        "**🐉 Dragon Commands**\n"
        "`!threshing` → Roll dragon color + tail\n"
        "`!dragonspeak` → Dragon approval or disapproval\n"
        "`!dragonaction` → Random dragon action\n\n"

        "**✨ Signets**\n"
        "`!signet` → Manifest your signet\n\n"

        "**⚔️ Quadrants**\n"
        "`!infantry` → Roll combat specialty\n"
        "`!scribe` → Roll subject specialty\n"
        "`!healing` → Roll healing discipline\n\n"

        "**🪽 Rider Formation**\n"
        "`!assignrider name` → Assign a rider to a random open slot\n"
        "`!manualassign name | role | wing | section | squad` → Manually assign a rider\n"
        "`!removerider name` → Remove one rider\n"
        "`!reassignrider name` → Remove and reroll one rider\n"
        "`!riderslots` → Show filled formation slots\n"
        "`!resetriders` → Reset rider formation\n\n"

        "**🎲 Standard D&D Dice**\n"
        "`!d4`\n"
        "`!d6`\n"
        "`!d8`\n"
        "`!d10`\n"
        "`!d12`\n"
        "`!d20`\n"
        "`!d100`\n\n"

        "**🎲 Custom Dice Rolls**\n"
        "`!roll d4`\n"
        "`!roll d6`\n"
        "`!roll d8`\n"
        "`!roll d10`\n"
        "`!roll d12`\n"
        "`!roll d20`\n"
        "`!roll d100`\n"
        "`!roll 2d6`\n"
        "`!roll 1d20+3`\n"
        "`!roll 2d8-1`\n"
    )

# -----------------------------
# RUN BOT
# -----------------------------
bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
