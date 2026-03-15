"""
Day/Night cycle system.
Controls time-of-day for time-sensitive evolutions, encounters, and other effects.
"""

from __future__ import annotations
import datetime


class TimeOfDay:
    MORNING = "morning"   # 06:00 - 09:59
    DAY     = "day"       # 10:00 - 17:59
    EVENING = "evening"   # 18:00 - 19:59
    NIGHT   = "night"     # 20:00 - 05:59


def get_time_of_day(hour: int | None = None) -> str:
    """
    Return the current time of day period.
    If hour is None, uses the actual system clock.
    """
    if hour is None:
        hour = datetime.datetime.now().hour
    if 6 <= hour < 10:
        return TimeOfDay.MORNING
    elif 10 <= hour < 18:
        return TimeOfDay.DAY
    elif 18 <= hour < 20:
        return TimeOfDay.EVENING
    else:
        return TimeOfDay.NIGHT


def is_daytime(hour: int | None = None) -> bool:
    """Return True during morning, day, or evening."""
    tod = get_time_of_day(hour)
    return tod in (TimeOfDay.MORNING, TimeOfDay.DAY, TimeOfDay.EVENING)


def is_nighttime(hour: int | None = None) -> bool:
    """Return True during night."""
    return get_time_of_day(hour) == TimeOfDay.NIGHT


def get_shiny_bonus(hour: int | None = None) -> float:
    """
    At night, shinies are slightly more likely to be encountered
    (in locations where this lore applies).
    Returns 1.0 (no bonus) or 1.5 during night.
    """
    return 1.5 if is_nighttime(hour) else 1.0


def describe_time(hour: int | None = None) -> str:
    """Human-readable description of the current time period."""
    tod = get_time_of_day(hour)
    descriptions = {
        TimeOfDay.MORNING: "It's morning — the sun is rising!",
        TimeOfDay.DAY:     "It's daytime — the sun shines brightly.",
        TimeOfDay.EVENING: "It's evening — the sun is setting.",
        TimeOfDay.NIGHT:   "It's nighttime — the stars glitter overhead.",
    }
    return descriptions[tod]
