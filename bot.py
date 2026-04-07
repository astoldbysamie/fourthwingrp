import os
import discord
from discord.ext import commands
import random
import re

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def threshing(ctx):
    colors = ["Black","Red","Red","Orange","Orange","Blue","Blue","Brown","Brown","Green","Green"]
    tails = ["Morningstar tail","Swordtail","Swordtail","Scorpion tail","Scorpion tail","Club tail","Club tail","Daggertail","Daggertail"]
    await ctx.send(
        f"**Threshing Result**\n"
        f"Dragon: {random.choice(colors)}\n"
        f"Tail: {random.choice(tails)}"
    )

@bot.command()
async def infantry(ctx):
    options = [
        ("Vanguard", "Frontline fighters. First to engage, built for direct combat and sustained pressure."),
        ("Bastion", "Defensive specialists. Shielding, protection, and holding formation under attack."),
        ("Skirmisher", "Fast and mobile. Flanking, scouting, and hit-and-run tactics."),
        ("Breaker", "Heavy force. Used to overwhelm defenses and break enemy lines."),
        ("Ranger", "Ranged specialists. Precision strikes, overwatch, and distance control."),
        ("Tactician", "Strategy-focused. Coordination, positioning, and battlefield awareness.")
    ]
    roll = random.randint(1, 6)
    name, desc = options[roll - 1]
    await ctx.send(f"**Infantry Result**\nRoll: {roll}\n{name}\n{desc}")

@bot.command()
async def scribe(ctx):
    options = [
        ("Archive", "Preservation of records, ancient texts, and restricted materials."),
        ("Chronicle", "Documentation of events, reports, and historical accounts."),
        ("Lexicon", "Languages, translation, and interpretation of foreign or coded texts."),
        ("Intelligence", "Information gathering, analysis, and strategic insight."),
        ("Cipher", "Codes, encryption, and protection of sensitive information."),
        ("Restricted", "Forbidden knowledge and sealed records.")
    ]
    roll = random.randint(1, 6)
    name, desc = options[roll - 1]
    await ctx.send(f"**Scribe Result**\nRoll: {roll}\n{name}\n{desc}")

@bot.command()
async def healing(ctx):
    options = [
        ("Battlefield", "Healers trained to operate within active combat."),
        ("Surgical", "Healers specializing in controlled, precision-based procedures."),
        ("Recovery", "Healers focused on long-term care and rehabilitation."),
        ("Emergency", "Healers trained for critical intervention."),
        ("Experimental", "Healers who utilize unproven or evolving methods."),
        ("Dragonkind", "Healers trained to treat dragons and manage rider-bond injuries.")
    ]
    roll = random.randint(1, 6)
    name, desc = options[roll - 1]
    await ctx.send(f"**Healing Result**\nRoll: {roll}\n{name}\n{desc}")

# -----------------------------
# HELPERS (needed for commands)
# -----------------------------
def find_existing_assignment(data, name):
    target = name.lower().strip()

    for wing_name, wing in data.items():
        if wing["wingleader"] and wing["wingleader"].lower() == target:
            return True

        for section in wing["sections"].values():
            if section["section_leader"] and section["section_leader"].lower() == target:
                return True

            for squad in section["squads"].values():
                if squad["squad_leader"] and squad["squad_leader"].lower() == target:
                    return True
                if squad["executive_squad_leader"] and squad["executive_squad_leader"].lower() == target:
                    return True
                if target in [c.lower() for c in squad["cadets"]]:
                    return True

    return False


def get_open_slots(data):
    slots = []

    for wing_name, wing in data.items():
        if wing["wingleader"] is None:
            slots.append(("Wingleader", wing_name))

        for section_name, section in wing["sections"].items():
            if section["section_leader"] is None:
                slots.append(("Section Leader", wing_name, section_name))

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
    wing = data[slot[1]]

    if role == "Wingleader":
        wing["wingleader"] = name

    elif role == "Section Leader":
        wing["sections"][slot[2]]["section_leader"] = name

    elif role == "Squad Leader":
        wing["sections"][slot[2]]["squads"][slot[3]]["squad_leader"] = name

    elif role == "Executive Squad Leader":
        wing["sections"][slot[2]]["squads"][slot[3]]["executive_squad_leader"] = name

    elif role == "Cadet":
        wing["sections"][slot[2]]["squads"][slot[3]]["cadets"].append(name)


def format_assignment(name, slot):
    role = slot[0]
    path = " → ".join(slot[1:])
    return f"**{name}** assigned as **{role}** in **{path}**."


def format_taken(data):
    lines = []

    for wing_name, wing in data.items():
        wing_lines = []

        if wing["wingleader"]:
            wing_lines.append(f"Wingleader: {wing['wingleader']}")

        for section_name, section in wing["sections"].items():
            if section["section_leader"]:
                wing_lines.append(f"{section_name} Section Leader: {section['section_leader']}")

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

    return "\n".join(lines) if lines else "No assignments yet."


# -----------------------------
# COMMANDS
# -----------------------------
@bot.command()
async def assignrider(ctx, *, name: str):
    global assignment_data

    if find_existing_assignment(assignment_data, name):
        await ctx.send(f"{name} is already assigned.")
        return

    slots = get_open_slots(assignment_data)

    if not slots:
        await ctx.send("No slots left.")
        return

    slot = random.choice(slots)
    assign_slot(assignment_data, name, slot)
    save_data(assignment_data)

    await ctx.send(format_assignment(name, slot))


@bot.command()
async def riderslots(ctx):
    output = format_taken(assignment_data)

    if len(output) <= 2000:
        await ctx.send(output)
    else:
        for i in range(0, len(output), 2000):
            await ctx.send(output[i:i+2000])


@bot.command()
async def resetriders(ctx):
    global assignment_data
    assignment_data = json.loads(json.dumps(DEFAULT_STRUCTURE))
    save_data(assignment_data)
    await ctx.send("Riders reset.")

@bot.command()
async def dragonspeak(ctx):
    approval = [
        "Your dragon rumbles low in approval.",
        "A warm pulse of satisfaction brushes through the bond.",
        "Your dragon lowers their head, clearly pleased."
    ]
    disapproval = [
        "Your dragon lets out a sharp, irritated snort.",
        "A cold flash of disapproval cuts through the bond.",
        "Your dragon turns their head away, unimpressed."
    ]
    if random.choice([True, False]):
        await ctx.send(f"**Dragon Approval**\n{random.choice(approval)}")
    else:
        await ctx.send(f"**Dragon Disapproval**\n{random.choice(disapproval)}")

@bot.command()
async def dragonaction(ctx):
    actions = [
        "Your dragon spreads their wings in dominance.",
        "Your dragon crouches low, ready to spring.",
        "Your dragon circles once, watching everything carefully.",
        "Your dragon gives a warning growl to everyone nearby.",
        "Your dragon nudges you with their snout."
    ]
    await ctx.send(f"**Dragon Action**\n{random.choice(actions)}")

@bot.command()
async def roll(ctx, *, dice: str):
    match = re.fullmatch(r"(\\d*)d(\\d+)([+-]\\d+)?", dice.strip())
    if not match:
        await ctx.send("Use: `!roll d20`, `!roll 2d6`, or `!roll 1d20+3`")
        return

    num = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    mod = int(match.group(3)) if match.group(3) else 0

    if num < 1 or num > 100:
        await ctx.send("Number of dice must be between 1 and 100.")
        return

    rolls = [random.randint(1, sides) for _ in range(num)]
    total = sum(rolls) + mod
    mod_text = f"{mod:+d}" if mod else "+0"
    await ctx.send(f"🎲 Rolls: {rolls}\nSubtotal: {sum(rolls)}\nModifier: {mod_text}\n**Total: {total}**")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is missing.")

bot.run(TOKEN)
