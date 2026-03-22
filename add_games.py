import json

with open('scripts_data.js', 'r', encoding='utf-8') as f:
    text = f.read()
    json_text = text.replace('const gamesData = ', '').strip().rstrip(';')
    games = json.loads(json_text)

existing_games = {g['name'].lower() for g in games}

new_scripts = [
    {
        "category": "combat",
        "game": "Slap Battles",
        "name": "Slap Battles Hub",
        "desc": "Auto farm slaps, get all gloves, infinite reach.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/SlackerHub/Scripts/main/SlapBattles'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "obby",
        "game": "Survive The Killer",
        "name": "Survive The Killer Hub",
        "desc": "ESP, auto escape, speedhack, and infinite jump.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/ShadowScripts/SurviveTheKiller/main/loader.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "obby",
        "game": "Flee the Facility",
        "name": "Flee the Facility ESP",
        "desc": "Beast ESP, auto hack computers, no slow down.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/ExampleScripts/FleeTheFacility/main/main.lua'))()",
        "hasKey": True,
        "verified": True
    },
    {
        "category": "combat",
        "game": "Ro-Ghoul",
        "name": "Ro-Ghoul Auto Farm",
        "desc": "Auto farm reputation, auto boss, auto trainers.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/RoGhoulScripts/AutoFarm/main/script.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "meme",
        "game": "Funky Friday",
        "name": "Funky Friday Autoplayer",
        "desc": "Perfect accuracy auto-player, customizable hit chance.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/wally-rblx/funky-friday-autoplay/main/main.lua'))()",
        "hasKey": False,
        "verified": True
    },
    {
        "category": "sim",
        "game": "Islands",
        "name": "Islands Utility Hub",
        "desc": "Auto farm crops, auto mine ores, infinite coins.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/IslandsScripts/Utility/main/loader.lua'))()",
        "hasKey": True,
        "verified": True
    },
    {
        "category": "sim",
        "game": "Natural Disaster Survival",
        "name": "NDS Safe Hub",
        "desc": "Auto teleport to safe zone, notify disaster, balloon giver.",
        "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/NDSScripts/SafeHub/main/script.lua'))()",
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
