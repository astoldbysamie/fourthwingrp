import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import re

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

# -----------------------------
# DICE COMMANDS
# -----------------------------
VALID_DICE = [4, 6, 8, 10, 12, 20, 100]

@bot.command()
async def roll(ctx, dice: str = "d20"):
    """
    Supports:
    !roll d20
    !roll d6
    !roll 2d6
    !roll 1d20+3
    !roll 2d8-1
    """

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
        "`!signet` → Manifest your signet (rarity determined by a d20 roll)\n\n"

        "**⚔️ Quadrants**\n"
        "`!infantry` → Roll combat specialty\n"
        "`!scribe` → Roll subject specialty\n"
        "`!healing` → Roll healing discipline\n\n"

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
