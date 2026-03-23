import json

with open('scripts_data.js', 'r', encoding='utf-8') as f:
    text = f.read()
    json_text = text.replace('const gamesData = ', '').strip().rstrip(';')
    games = json.loads(json_text)

existing_games = {g['name'].lower() for g in games}

new_scripts = [
    {
        "category": "combat",
        "game": "Blade Ball",
        "name": "Blade Ball AI Auto-Parry",
        "desc": "Perfect timing auto-block, aimbot, and curve control.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/StrivonHub/BladeBall/main/main.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "rpg",
        "game": "Bloop Fruits",
        "name": "Bloop Fruits Absolute Hub",
        "desc": "Auto max level, auto chest, devil fruit sniper, sea event farmer.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/BloxScripts/BloopHub/main/source.lua'))()",
        "hasKey": True,
        "verified": True
    },
    {
        "category": "sim",
        "game": "Pet Simulator 99",
        "name": "PS99 OP Farmer",
        "desc": "Auto break coins, auto egg hatch, huge pet sniper.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/PS99x/Farm/main/script.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "shooter",
        "game": "Arsenal",
        "name": "Arsenal Silent Aim & ESP",
        "desc": "Hitbox expander, silent aim, infinite ammo, wallbang.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/TenseHub/Arsenal/main/aim.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "rpg",
        "game": "Anime Defenders",
        "name": "AD Infinite Gems",
        "desc": "Auto story, auto infinite mode, auto summon, trait rerolling.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/ADScripts/Gems/main/loader.lua'))()",
        "hasKey": True,
        "verified": True
    },
    {
        "category": "rp",
        "game": "Brookhaven RP",
        "name": "Brookhaven Admin & Troll",
        "desc": "Fling others, bypass ban, speed hack, free premium items.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/IceHub/Brookhaven/main/troll.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "shooter",
        "game": "Da Hood",
        "name": "Da Hood Lock-on",
        "desc": "Target lock-on, anti-stomp, cash drop, speed exploit.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/HoodScripts/Lock/main/aim.lua'))()",
        "hasKey": True,
        "verified": True
    },
    {
        "category": "horror",
        "game": "DOORS",
        "name": "DOORS Entity ESP",
        "desc": "Avoid entities, auto seek chase, lighter infinite.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/DoorsExploit/EntityESP/main/doors.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "combat",
        "game": "King Legacy",
        "name": "King Legacy Auto Raid",
        "desc": "Auto farm level, auto sea king, auto raid.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/KLHub/Scripts/main/SeaKing.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "combat",
        "game": "Ninja Legends",
        "name": "Ninja Auto-Swing & Sell",
        "desc": "Fastest auto-swing, instant teleport to bosses, infinite double jump.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/NinjaScripts/Legends/main/loader.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "sim",
        "game": "Build A Boat",
        "name": "Auto Win Build A Boat",
        "desc": "Teleport to end instantly, auto farm gold blocks.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/BaBHub/AutoWin/main/script.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "sim",
        "game": "Lumber Tycoon 2",
        "name": "LT2 Wood Dupe",
        "desc": "Dupe money, auto bring wood, teleport all axes.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/LumberScripts/Tycoon/main/dupe.lua'))()",
        "hasKey": True,
        "verified": True
    },
    {
        "category": "rp",
        "game": "Murder Mystery 2",
        "name": "MM2 Sheriff ESP",
        "desc": "Gun drops ESP, auto grab gun, kill murderer aura.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/MM2God/ESP/main/script.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "combat",
        "game": "Grand Piece Online",
        "name": "GPO Dungeon Farmer",
        "desc": "Auto block, fast attack, auto dungeon completion.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/GPOHub/Farmer/main/dungeon.lua'))()",
        "hasKey": True,
        "verified": True
    },
    {
        "category": "sim",
        "game": "Bee Swarm Simulator",
        "name": "BSS Macro Script",
        "desc": "Auto farm pollen, auto dispenser, vicious bee sniper.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/BSSHack/Macro/main/script.lua'))()",
        "hasKey": False,
        "verified": True
    }
]

added = 0
for s in new_scripts:
    g_name = s['game']
    if g_name.lower() not in existing_games:
        games.append({
            "name": g_name,
            "category": s['category'],
            "scripts": [{
                "name": s['name'],
                "desc": s['desc'],
                "code": s['code'],
                "hasKey": s['hasKey'],
                "verified": s['verified']
            }]
        })
        added += 1

with open('scripts_data.js', 'w', encoding='utf-8') as f:
    f.write('const gamesData = ' + json.dumps(games, indent=4) + ';\n')

print(f"Added {added} more games!")
