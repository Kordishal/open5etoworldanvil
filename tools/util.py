import re

speed_pattern = re.compile(r"^(?P<speed>\d+) ft\.(, fly (?P<speed_fly>\d+) ft\. ((?P<hover>\(hover\))|.+)?)?")


sizes = {
    'T': 'Tiny',
    'S': 'Small',
    'M': 'Medium',
    'L': 'Large',
    'H': 'Huge',
    'G': 'Gargantuan',
}

alignment = {
    'L': 'Lawful',
    'N': 'Neutral',
    'C': 'Chaotic',
    'G': 'Good',
    'E': 'Evil',
}

proficiency_bonus = {
    "0": "+2",
    "1/8": "+2",
    "1/4": "+2",
    "1/2": "+2",
    "1": "+2",
    "2": "+2",
    "3": "+2",
    "4": "+2",
    "5": "+3",
    "6": "+3",
    "7": "+3",
    "8": "+3",
    "9": "+4",
    "10": "+4",
    "11": "+4",
    "12": "+4",
    "13": "+5",
    "14": "+5",
    "15": "+5",
    "16": "+5",
    "17": "+6",
    "18": "+6",
    "19": "+6",
    "20": "+6",
    "21": "+7",
    "22": "+7",
    "23": "+7",
    "24": "+7",
    "25": "+8",
    "26": "+8",
    "27": "+8",
    "28": "+8",
    "29": "+9",
    "30": "+9"
}

xp = {
    "0": "10",
    "1/8": "25",
    "1/4": "50",
    "1/2": "100",
    "1": "200",
    "2": "450",
    "3": "700",
    "4": "1'100",
    "5": "1'800",
    "6": "2'300",
    "7": "2'900",
    "8": "3'900",
    "9": "5'000",
    "10": "5'900",
    "11": "7'200",
    "12": "8'400",
    "13": "10'000",
    "14": "11'500",
    "15": "13'000",
    "16": "15'000",
    "17": "18'000",
    "18": "20'000",
    "19": "22'000",
    "20": "25'000",
    "21": "33'000",
    "22": "41'000",
    "23": "50'000",
    "24": "62'000",
    "25": "75'000",
    "26": "90'000",
    "27": "105'000",
    "28": "120'000",
    "29": "135'000",
    "30": "155'000"
}


def get_hit(entry: re.Match[str]):
    if entry:
        return f"+{entry.group(1)}"
    else:
        raise Exception("No hit found")


def get_roll(entry: re.Match[str]):
    if entry:
        return f"[roll:{entry.group(1)}]"
    else:
        raise Exception("No roll found")

def get_dc(entry: re.Match[str]):
    if entry:
        return f"DC {entry.group(1)}"
    else:
        raise Exception("No DC found")

def get_condition(entry: re.Match[str]):
    if entry:
        return f"{entry.group(1)}"
    else:
        raise Exception("No condition found")


unit_conversion = {
    'ft.': ' sq.',
    'feet': ' square',
    '-foot': '-square',
}


def transform_feet(entry: re.Match[str]):
    if entry:
        try:
            unit = unit_conversion[entry.group(2)]
            return f"{int(entry.group(1)) // 5}{unit}"
        except IndexError:
            raise Exception(f"No unit for entry: {entry}")
    else:
        raise Exception("No feet found")


def transform_range(entry: re.Match[str]):
    if entry:
        return f"{int(entry.group(1)) // 5}/{int(entry.group(2)) // 5} sq."
    else:
        raise Exception("No range found")


def transform_entries(entries: list):
    polished_entries = []
    for entry in entries:
        entry = re.sub(r'\{@atk mw}', '[i]Melee Weapon Attack:[/i]', entry)
        entry = re.sub(r'\{@atk rw}', '[i]Ranged Weapon Attack:[/i]', entry)
        entry = re.sub(r'\{@hit (\d+)}', get_hit, entry)
        entry = re.sub(r'\{@h}', '[i]Hit:[/i] ', entry)
        entry = re.sub(r'\{@damage (.+?)}', get_roll, entry)
        entry = re.sub(r'\{@dc (\d+)}', get_dc, entry)
        entry = re.sub(r'\{@condition (.+?)}', get_condition, entry)
        entry = re.sub(r'range (\d+)/(\d+) ft\.', transform_range, entry)
        entry = re.sub(r'(\d+) (ft\.|feet)', transform_feet, entry)
        entry = re.sub(r'(\d)(-foot)', transform_feet, entry)
        if '@' in entry:
            raise Exception(f"Unexpected character '@' in entry: {entry}")
        polished_entries.append(entry)
    return '\\n\\n'.join(polished_entries)


def transform_name(name: str):
    name = re.sub(r'\{@recharge 5}', '(Recharge [roll:1d6>=5])', name)
    name = re.sub(r'\{@recharge 6}', '(Recharge [roll:1d6>=6])', name)
    if '@' in name:
        raise Exception(f"Unexpected character '@' in name: {name}")
    return name




def update(data: dict):
    hit_points = f"{data['hp']['average']} [roll:{data['hp']['formula']}]"
    ac = data['ac'][0]
    if isinstance(ac, dict) and 'from' in ac:
        ac = f"{ac['ac']} ({', '.join(ac['from'])})"
    else:
        ac = ac

    senses = list()
    if 'senses' in data:
        senses.extend([re.sub(r'(\d+) (ft\.)', transform_feet, sense) for sense in data['senses']])

    if 'passive' in data:
        senses.append(f"passive Perception {data['passive']}")

    special_abilities = ""
    if 'trait' in data:
        special_abilities = '\\n\\n'.join(
            [f"[i][b]{transform_name(trait['name'])}.[/b][/i] {transform_entries(trait['entries'])}" for trait in data['trait']]
        )

    actions = ""
    if 'action' in data:
        actions = '\\n\\n'.join(
            [f"[i][b]{transform_name(action['name'])}.[/b][/i] {transform_entries(action['entries'])}" for action in data['action']]
        )

    return f"""
name: {data['name']}
challenge_rating: "{data['cr']}"
xp: "{xp[data['cr']]}"
types: "{data['type'].capitalize()}"
pb: '{proficiency_bonus[data['cr']]}'
size: {', '.join([sizes[size] for size in data['size']])}
sizer: NONE
languages: '{', '.join(re.sub(r'(\d+) (ft\.)', transform_feet, language) for language in data['languages'])}'
alignment: '{data['alignmentPrefix']}{' '.join([alignment[align] for align in data['alignment']])}'
description: ''
suggested_environments: '{', '.join(filter(lambda x: x != 'none', data['_fEnvironment']))}'
armor_class: '{ac}'
hit_points: '{hit_points}'
strength: '{data['str']}'
dexterity: '{data['dex']}'
constitution: '{data['con']}'
intelligence: '{data['int']}'
wisdom: '{data['wis']}'
charisma: '{data['cha']}'
base_movement_units: "sq."
base_movement_in_ft: '{data['speed']['walk'] // 5}'
fly_movement_in_ft: '{data['speed']['fly']['number'] // 5 if 'fly' in data['speed'] else ''}'
burrow_movement_in_ft: ''
swim_movement_in_ft: ''
climb_movement_in_ft: ''
can_hover: '{'1' if 'fly' in data['speed'] and data['speed']['fly']['condition'] == 'hover' else '0'}'
senses: '{', '.join(senses)}'
skills: '{', '.join([f"{key.capitalize()} {value}" for key, value in data['skill'].items()]) if 'skill' in data else ''}'
saving_throws: '{', '.join([f"{key.capitalize()} {value}" for key, value in data['save'].items()]) if 'save' in data else ''}'
damage_vulnerabilities: '{', '.join(data['vulnerable']) if 'vulnerable' in data else ''}'
damage_resistances: '{', '.join(data['resist']) if 'resist' in data else ''}'
damage_immunities: '{', '.join(data['immune']) if 'immune' in data else ''}'
condition_immunities: '{', '.join(data['conditionImmune']) if 'conditionImmune' in data else ''}'
spellcasting: ''
cast_at_will: ''
cast_one_per_day: ''
cast_twice_per_day: ''
cast_thrice_per_day: ''
special_abilities: "{special_abilities}"
actions: "{actions}"
bonus_actions: ''
reactions: ''
legendary_actions: ''
lair_description: ''
lair_actions: ''
regional_effects: ''
motivation: ''
tactics: ''
image_gallery_id: ''
source: '{data['source']} p. {data['page']}'
"""
