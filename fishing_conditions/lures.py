"""Tag-based lure database and recommender.

Each lure is tagged along four dimensions instead of being buried in a wall of
nested if/elif statements. To add a new lure, just append a dict here -- no
branching logic needs to change.

    species:       which fish it's designed to target
    water_clarity: "clear" and/or "murky"
    depth:         "shallow" and/or "deep"
    weather:       any of "clear", "overcast", "windy", "rain"
    style:         the retrieve/type, shown to the user for context
"""

LURES = [
    {
        "name": "McHybrid (Perch pattern)",
        "species": ["Pike"],
        "water_clarity": ["clear"],
        "depth": ["shallow"],
        "weather": ["clear"],
        "style": "swimbait",
    },
    {
        "name": "Westin Swim (Golden 3D Perch)",
        "species": ["Pike"],
        "water_clarity": ["clear"],
        "depth": ["shallow"],
        "weather": ["clear"],
        "style": "swimbait",
    },
    {
        "name": "Westin Mike the Pike",
        "species": ["Pike"],
        "water_clarity": ["clear"],
        "depth": ["shallow", "deep"],
        "weather": ["clear", "overcast"],
        "style": "jerkbait",
    },
    {
        "name": "Westin R&R ShadTeez (Motoroil Burbot)",
        "species": ["Pike"],
        "water_clarity": ["clear"],
        "depth": ["shallow"],
        "weather": ["clear", "windy"],
        "style": "shadtail swimbait",
    },
    {
        "name": "Berkley Zilla Flanker (Ayu Green)",
        "species": ["Pike"],
        "water_clarity": ["clear"],
        "depth": ["deep"],
        "weather": ["clear"],
        "style": "jointed swimbait",
    },
    {
        "name": "Copper Abu Garcia Atom Spoon",
        "species": ["Pike"],
        "water_clarity": ["clear", "murky"],
        "depth": ["deep"],
        "weather": ["clear", "overcast"],
        "style": "spoon",
    },
    {
        "name": "Headbanger Shad (Firetiger)",
        "species": ["Pike"],
        "water_clarity": ["murky"],
        "depth": ["shallow"],
        "weather": ["clear"],
        "style": "swimbait",
    },
    {
        "name": "Firetiger Spinnerbait",
        "species": ["Pike"],
        "water_clarity": ["murky"],
        "depth": ["shallow"],
        "weather": ["clear"],
        "style": "spinnerbait",
    },
    {
        "name": "Savage Gear Deviator Swim (Firetiger)",
        "species": ["Pike"],
        "water_clarity": ["murky"],
        "depth": ["shallow", "deep"],
        "weather": ["clear", "overcast", "windy"],
        "style": "swimbait",
    },
    {
        "name": "Storm RIP Curly Tail (Demon)",
        "species": ["Pike"],
        "water_clarity": ["murky"],
        "depth": ["deep"],
        "weather": ["clear", "overcast"],
        "style": "soft plastic curly tail",
    },
    {
        "name": "Storm RIP Curly Tail (Hot Pike)",
        "species": ["Pike"],
        "water_clarity": ["murky"],
        "depth": ["shallow", "deep"],
        "weather": ["overcast", "windy"],
        "style": "soft plastic curly tail",
    },
    {
        "name": "Pike Chatterbait",
        "species": ["Pike"],
        "water_clarity": ["murky"],
        "depth": ["deep"],
        "weather": ["clear", "overcast", "windy"],
        "style": "chatterbait",
    },
    {
        "name": "McMio Fegis",
        "species": ["Pike"],
        "water_clarity": ["clear"],
        "depth": ["shallow", "deep"],
        "weather": ["overcast"],
        "style": "jerkbait",
    },
    {
        "name": "Abu Garcia Tormentor Jointed Crankbait",
        "species": ["Pike"],
        "water_clarity": ["clear"],
        "depth": ["shallow", "deep"],
        "weather": ["overcast"],
        "style": "crankbait",
    },
    {
        "name": "Rapala XRap Otis (Hot Pike)",
        "species": ["Pike"],
        "water_clarity": ["clear"],
        "depth": ["shallow", "deep"],
        "weather": ["windy"],
        "style": "jerkbait",
    },
    {
        "name": "White Spinnerbait",
        "species": ["Pike"],
        "water_clarity": ["clear"],
        "depth": ["shallow", "deep"],
        "weather": ["windy"],
        "style": "spinnerbait",
    },
    {
        "name": "Abu Garcia Beast Fegis",
        "species": ["Pike"],
        "water_clarity": ["murky"],
        "depth": ["deep"],
        "weather": ["windy"],
        "style": "jerkbait",
    },
]

ALL_SPECIES = sorted({species for lure in LURES for species in lure["species"]})


def recommend_lures(species, water_clarity, depth, weather_tags, top_n=3):
    """Rank lures by how many of the requested tags they match.

    species, water_clarity and depth are single strings; weather_tags is an
    iterable of tags (a lure can match on more than one, e.g. both "clear"
    and "windy").
    """
    weather_tags = set(weather_tags)
    scored = []

    for lure in LURES:
        score = 0
        if species in lure["species"]:
            score += 3
        if water_clarity in lure["water_clarity"]:
            score += 3
        if depth in lure["depth"]:
            score += 3
        score += 2 * len(weather_tags & set(lure["weather"]))

        if score > 0:
            scored.append((score, lure))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [lure for _, lure in scored[:top_n]]
