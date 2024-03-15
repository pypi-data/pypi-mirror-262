import math


def check_framerate_multiples(lst):
    if len(lst) < 2:
        return True

    smallest = min(lst)
    for num in lst:
        if num % smallest != 0:
            return False

    return smallest


def adjust_to_framerate(timepoints, framerate):
    adjusted_list = []
    for num in timepoints:
        adjusted_num = math.ceil(num * framerate) / framerate
        adjusted_list.append(adjusted_num)
    return adjusted_list


def seconds_to_timecode(seconds, include_milliseconds=False, force_hours=True):
    # Extract hours
    hours = int(seconds // 3600)
    seconds %= 3600

    # Extract minutes
    minutes = int(seconds // 60)
    seconds %= 60

    if include_milliseconds:
        ms = (seconds - int(seconds)) * 1000
        return "{:02d}:{:02d}:{:02d}.{:03d}".format(
            hours, minutes, int(seconds), int(ms)
        )
    else:
        if hours == 0 and not force_hours:
            return "{:02d}:{:02d}".format(minutes, int(seconds))
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, int(seconds))
