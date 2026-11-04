"""Lure suitability advisor.

Rather than recommending specific named products (which go out of stock and
go stale), this scores how well the *attributes* of a lure the angler
already has -- colour, finish, action, running depth -- suit the current
conditions, and explains what to change if the fit is poor.
"""

COLOURS = ["natural", "bright", "dark", "white/pale"]
FINISHES = ["flashy", "matte"]
ACTIONS = ["subtle", "vibrating", "erratic"]
DEPTHS = ["shallow", "deep"]


def _score_depth(depth, target_depth):
    return 10 if depth == target_depth else 3


def _score_colour(colour, water_clarity):
    if water_clarity == "murky":
        return {"bright": 10, "dark": 8, "white/pale": 5, "natural": 3}[colour]
    return {"natural": 10, "white/pale": 7, "bright": 5, "dark": 4}[colour]  # clear


def _score_flash(finish, weather_tags):
    if "clear" in weather_tags:
        return {"flashy": 9, "matte": 6}[finish]
    if "overcast" in weather_tags or "rain" in weather_tags:
        return {"flashy": 6, "matte": 8}[finish]
    return {"flashy": 7, "matte": 7}[finish]  # windy with no other weather tag


def _score_action(action, water_clarity, weather_tags):
    if "windy" in weather_tags:
        return {"vibrating": 10, "erratic": 8, "subtle": 5}[action]
    if water_clarity == "murky":
        return {"vibrating": 10, "erratic": 7, "subtle": 4}[action]
    return {"subtle": 9, "erratic": 7, "vibrating": 5}[action]  # clear water, calm


def assess_lure(colour, finish, action, depth, water_clarity, target_depth, weather_tags):
    """Score (0-10) how well a described lure suits the current conditions,
    plus a list of plain-English suggestions for whatever scored poorly."""

    depth_score = _score_depth(depth, target_depth)
    colour_score = _score_colour(colour, water_clarity)
    flash_score = _score_flash(finish, weather_tags)
    action_score = _score_action(action, water_clarity, weather_tags)

    overall = (depth_score + colour_score + flash_score + action_score) / 4

    feedback = []
    if depth_score < 10:
        feedback.append(f"These conditions call for a {target_depth}-running lure, but yours runs {depth}.")
    if colour_score < 7:
        better = "bright or dark" if water_clarity == "murky" else "natural or pale"
        feedback.append(f"In {water_clarity} water, {better} colours usually outfish {colour} ones.")
    if flash_score < 7:
        better = "matte" if finish == "flashy" else "flashy"
        feedback.append(f"Given the current weather, a {better} finish would likely draw more attention than {finish}.")
    if action_score < 7:
        better = "vibrating" if ("windy" in weather_tags or water_clarity == "murky") else "subtle"
        feedback.append(f"A more {better} action would suit these conditions better than {action}.")

    return overall, feedback
