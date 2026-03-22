import json
import random

with open('scripts_data.js', 'r', encoding='utf-8') as f:
    text = f.read()
    # Strip `const scriptsData = ` and `;`
    json_text = text.replace('const scriptsData = ', '').strip().rstrip(';')
    scripts = json.loads(json_text)

# Add Voidware and CatVape for BedWars
scripts.append({
    "category": "combat",
    "game": "BedWars",
    "name": "Voidware Hub",
    "desc": "Elite performance BedWars combat client. Keyless and highly optimized.",
    "code": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/VapeVoidware/vapevoidware/main/NewMainScript.lua"))()',
    "hasKey": False,
    "verified": True
})
scripts.append({
    "category": "combat",
    "game": "BedWars",
    "name": "CatVape",
    "desc": "Custom user-provided CatVape modular loader.",
    "code": "loadstring(game:HttpGet('https://raw.githubusercontent.com/MaxlaserTech/CatV6/main/init.lua'), 'init.lua')({})",
    "hasKey": False,
    "verified": True
})

# Group scripts by game
games_dict = {}

for s in scripts:
    g_name = s['game']
    
    # Assign random key requirement if name contains 'Hub', unless we know specifically
    has_key = s.get('hasKey', False)
    if not has_key and "Hub" in s['name']:
        has_key = random.choice([True, False])

    script_obj = {
        "name": s['name'],
        "desc": s['desc'],
        "code": s['code'],
        "hasKey": has_key,
        "verified": s['verified']
    }
    
    if g_name not in games_dict:
        games_dict[g_name] = {
            "name": g_name,
            "category": s['category'],
            "scripts": []
        }
    games_dict[g_name]['scripts'].append(script_obj)

# Convert to list
games_list = list(games_dict.values())

with open('scripts_data.js', 'w', encoding='utf-8') as f:
    f.write('const gamesData = ' + json.dumps(games_list, indent=4) + ';\n')

print(f"Grouped into {len(games_list)} games with multiple scripts!")
