SCENARIO_DICT = {
    1: "URA Finals",
    2: "Aoharu Cup",
    3: "Grand Live",
    4: "Make a New Track",
    5: "Grand Masters",
    6: "Project L'Arc"
}

MOTIVATION_DICT = {
    5: "Very High",
    4: "High",
    3: "Normal",
    2: "Low",
    1: "Very Low"
}

SUPPORT_CARD_RARITY_DICT = {
    1: "R",
    2: "SR",
    3: "SSR"
}

SUPPORT_CARD_TYPE_DICT = {
    (101, 1): "speed",
    (105, 1): "stamina",
    (102, 1): "power",
    (103, 1): "guts",
    (106, 1): "wiz",
    (0, 2): "friend",
    (0, 3): "group"
}

SUPPORT_CARD_TYPE_DISPLAY_DICT = {
    "speed": "Speed",
    "stamina": "Stamina",
    "power": "Power",
    "guts": "Guts",
    "wiz": "Wisdom",
    "friend": "Friend",
    "group": "Group"
}

SUPPORT_TYPE_TO_COMMAND_IDS = {
    "speed": [101, 601, 1101],
    "stamina": [105, 602, 1102],
    "power": [102, 603, 1103],
    "guts": [103, 604, 1104],
    "wiz": [106, 605, 1105],
    "friend": [],
    "group": []
}

COMMAND_ID_TO_KEY = {
    101: "speed",
    105: "stamina",
    102: "power",
    103: "guts",
    106: "wiz",
    601: "speed",
    602: "stamina",
    603: "power",
    604: "guts",
    605: "wiz",
    1101: "speed",
    1102: "stamina",
    1103: "power",
    1104: "guts",
    1105: "wiz",
    "ss_match": "ss_match"
}

TARGET_TYPE_TO_KEY = {
    1: "speed",
    2: "stamina",
    3: "power",
    4: "guts",
    5: "wiz"
}

MONTH_DICT = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

GL_TOKEN_LIST = [
    'dance',
    'passion',
    'vocal',
    'visual',
    'mental'
]

ORIENTATION_DICT = {
    True: 's_game_position_portrait',
    False: 's_game_position_landscape',
    's_game_position_portrait': True,
    's_game_position_landscape': False,
}

# Request packets contain keys that should not be kept for privacy reasons.
REQUEST_KEYS_TO_BE_REMOVED = [
    "device",
    "device_id",
    "device_name",
    "graphics_device_name",
    "ip_address",
    "platform_os_version",
    "carrier",
    "keychain",
    "locale",
    "button_info",
    "dmm_viewer_id",
    "dmm_onetime_token",
]

HEROES_SCORE_TO_LEAGUE_DICT = {
    0: "Bronze 1",
    1000: "Bronze 2",
    2000: "Bronze 3",
    3000: "Bronze 4",
    4000: "Silver 1",
    5500: "Silver 2",
    7000: "Silver 3",
    8500: "Silver 4",
    10000: "Gold 1",
    12500: "Gold 2",
    15000: "Gold 3",
    17500: "Gold 4",
    20000: "Platinum 1",
    23000: "Platinum 2",
    26000: "Platinum 3",
    30000: "Platinum 4"
}

SCOUTING_SCORE_TO_RANK_DICT = {
          0: "No rank",
     60_000: "E",
     63_000: "E1",
     66_000: "E2",
     69_000: "E3",
     72_000: "D",
     76_000: "D1",
     80_000: "D2",
     85_000: "D3",
     90_000: "C",
     95_000: "C1",
    100_000: "C2",
    105_000: "C3",
    110_000: "B",
    115_000: "B1",
    120_000: "B2",
    125_000: "B3",
    130_000: "A",
    135_000: "A1",
    140_000: "A2",
    145_000: "A3",
    150_000: "A4",
    155_000: "A5",
    160_000: "S",
    165_000: "S1",
    170_000: "S2",
    180_000: "S3",
    190_000: "S4",
    200_000: "S5",
    210_000: "SS"
}

BOND_COLOR_DICT = {
    0: "#2AC0FF",
    60: "#A2E61E",
    80: "#FFAD1E",
    100: "#FFEB78"
}