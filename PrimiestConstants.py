from re import compile
from math import floor, log10

DT_FMT_PATTERN = compile("^([A-Z]+)?-?([A-Z]+)?-?([A-Z]+)? ?([a-z]+)?:?([a-z]+)?:?([a-z]+)?(_\(12 hour\))?")

DATE_FILTER_YEAR = "Year"
DATE_FILTER_YEAR_2 = "Short Year"
DATE_FILTER_MONTH = "Month"
DATE_FILTER_DAY = "Day"
DATE_FILTER_ISO4 = "YYYY-MM-DD"
DATE_FILTER_EU4 = "DD-MM-YYYY"
DATE_FILTER_EU4_NO_PAD = "D-M-YYYY"
DATE_FILTER_US4 = "MM-DD-YYYY"
DATE_FILTER_US4_NO_PAD = "M-D-YYYY"
DATE_FILTER_ISO2 = "YY-MM-DD"
DATE_FILTER_EU2 = "DD-MM-YY"
DATE_FILTER_EU2_NO_PAD = "D-M-YY"
DATE_FILTER_US2 = "MM-DD-YY"
DATE_FILTER_US2_NO_PAD = "M-D-YY"

DATE_FILTER_LABELS = [
    DATE_FILTER_YEAR,
    DATE_FILTER_YEAR_2,
    DATE_FILTER_MONTH,
    DATE_FILTER_DAY,
    DATE_FILTER_ISO4,
    DATE_FILTER_EU4,
    DATE_FILTER_EU4_NO_PAD,
    DATE_FILTER_US4,
    DATE_FILTER_US4_NO_PAD,
    DATE_FILTER_ISO2,
    DATE_FILTER_EU2,
    DATE_FILTER_EU2_NO_PAD,
    DATE_FILTER_US2,
    DATE_FILTER_US2_NO_PAD
]

TIME_FILTER_12_H_SUF = "_(12 hour)"

TIME_FILTER_HOUR = "Hour (24)"
TIME_FILTER_HOUR_12 = "Hour (12)"
TIME_FILTER_MINUTE = "Minute"
TIME_FILTER_SECOND = "Second"
TIME_FILTER_HOUR_MINUTE = "hh:mm"
TIME_FILTER_HOUR_MINUTE_12 = "hh:mm" + TIME_FILTER_12_H_SUF
TIME_FILTER_TS24 = "hh:mm:ss"
TIME_FILTER_TS12 = "hh:mm:ss" + TIME_FILTER_12_H_SUF
TIME_FILTER_SOD = "Second of day"

TIME_FILTER_LABELS = [
    TIME_FILTER_HOUR,
    TIME_FILTER_HOUR_12,
    TIME_FILTER_MINUTE,
    TIME_FILTER_SECOND,
    TIME_FILTER_HOUR_MINUTE,
    TIME_FILTER_HOUR_MINUTE_12,
    TIME_FILTER_TS24,
    TIME_FILTER_TS12,
    TIME_FILTER_SOD
]

DATE_TIME_FILTER_ISO_24 = "YYYY-MM-DD hh:mm:ss"
DATE_TIME_FILTER_ISO_12 = "YYYY-MM-DD hh:mm:ss" + TIME_FILTER_12_H_SUF
DATE_TIME_FILTER_EU_24 = "DD-MM-YYYY hh:mm:ss"
DATE_TIME_FILTER_EU_24_NO_PAD = "D-M-YYYY h:mm:ss"
DATE_TIME_FILTER_EU_12 = "DD-MM-YYYY hh:mm:ss" + TIME_FILTER_12_H_SUF
DATE_TIME_FILTER_EU_12_NO_PAD = "D-M-YYYY h:mm:ss" + TIME_FILTER_12_H_SUF
DATE_TIME_FILTER_US_24 = "MM-DD-YYYY hh:mm:ss"
DATE_TIME_FILTER_US_24_NO_PAD = "M-D-YYYY h:mm:ss"
DATE_TIME_FILTER_US_12 = "MM-DD-YYYY hh:mm:ss" + TIME_FILTER_12_H_SUF
DATE_TIME_FILTER_US_12_NO_PAD = "M-D-YYYY h:mm:ss" + TIME_FILTER_12_H_SUF
DATE_TIME_FILTER_ISO_24_2Y = "YY-MM-DD hh:mm:ss"
DATE_TIME_FILTER_ISO_12_2Y = "YY-MM-DD hh:mm:ss" + TIME_FILTER_12_H_SUF
DATE_TIME_FILTER_EU_24_2Y = "DD-MM-YY hh:mm:ss"
DATE_TIME_FILTER_EU_24_2Y_NO_PAD = "D-M-YY h:mm:ss"
DATE_TIME_FILTER_EU_12_2Y = "DD-MM-YY hh:mm:ss" + TIME_FILTER_12_H_SUF
DATE_TIME_FILTER_EU_12_2Y_NO_PAD = "D-M-YY h:mm:ss" + TIME_FILTER_12_H_SUF
DATE_TIME_FILTER_US_24_2Y = "MM-DD-YY hh:mm:ss"
DATE_TIME_FILTER_US_24_2Y_NO_PAD = "M-D-YY h:mm:ss"
DATE_TIME_FILTER_US_12_2Y = "MM-DD-YY hh:mm:ss" + TIME_FILTER_12_H_SUF
DATE_TIME_FILTER_US_12_2Y_NO_PAD = "M-D-YY h:mm:ss" + TIME_FILTER_12_H_SUF

DATE_TIME_FILTER_LABELS = [
    DATE_TIME_FILTER_ISO_24,
    DATE_TIME_FILTER_ISO_12,
    DATE_TIME_FILTER_EU_24,
    DATE_TIME_FILTER_EU_24_NO_PAD,
    DATE_TIME_FILTER_EU_12,
    DATE_TIME_FILTER_EU_12_NO_PAD,
    DATE_TIME_FILTER_US_24,
    DATE_TIME_FILTER_US_24_NO_PAD,
    DATE_TIME_FILTER_US_12,
    DATE_TIME_FILTER_US_12_NO_PAD,
    DATE_TIME_FILTER_ISO_24_2Y,
    DATE_TIME_FILTER_ISO_12_2Y,
    DATE_TIME_FILTER_EU_24_2Y,
    DATE_TIME_FILTER_EU_24_2Y_NO_PAD,
    DATE_TIME_FILTER_EU_12_2Y,
    DATE_TIME_FILTER_EU_12_2Y_NO_PAD,
    DATE_TIME_FILTER_US_24_2Y,
    DATE_TIME_FILTER_US_24_2Y_NO_PAD,
    DATE_TIME_FILTER_US_12_2Y,
    DATE_TIME_FILTER_US_12_2Y_NO_PAD
]

NON_FORMAT_FILTERS = [
    DATE_FILTER_YEAR,
    DATE_FILTER_YEAR_2,
    DATE_FILTER_MONTH,
    DATE_FILTER_DAY,
    TIME_FILTER_HOUR,
    TIME_FILTER_HOUR_12,
    TIME_FILTER_MINUTE,
    TIME_FILTER_SECOND,
]

DEFAULT_FILTERS = [
    DATE_FILTER_YEAR,
    DATE_FILTER_MONTH,
    DATE_FILTER_DAY,
    DATE_FILTER_ISO4,
    DATE_FILTER_EU4,
    DATE_FILTER_US4,
    TIME_FILTER_HOUR,
    TIME_FILTER_MINUTE,
    TIME_FILTER_SECOND,
    TIME_FILTER_HOUR_MINUTE,
    TIME_FILTER_TS24,
    DATE_TIME_FILTER_ISO_24,
    DATE_TIME_FILTER_EU_24,
    DATE_TIME_FILTER_US_24,
]

DEFAULT_START_YEAR = 1900
DEFAULT_END_YEAR = 3000

FILTER_GROUP_DISPLAY_NAMES = {
    id(DATE_FILTER_LABELS): "Date Primeness",
    id(TIME_FILTER_LABELS): "Time Primeness",
    id(DATE_TIME_FILTER_LABELS): "Date+Time Primeness"
}

FMT_FILTER_ARG_PAD = (None, None, None)


def dt_fmt_to_func(filter_fmt):
    filter_groups = DT_FMT_PATTERN.match(filter_fmt)
    year_mod_100 = False
    time_12_h = filter_groups.group(7)
    paddings = {}
    for group_index in range(len(filter_groups.groups()) - 1, 0, -1):
        group_str = filter_groups.group(group_index)
        if not group_str:
            continue
        if group_str == "YY":
            year_mod_100 = True
        group_span = filter_groups.span(group_index)
        group_len = group_span[1] - group_span[0]
        paddings[group_index] = (group_str[0], group_len)

    def sum_fmt(year=0, month=0, day=0, hour=0, minute=0, second=0):
        offset = 0
        dt_sum = 0
        val_map = {
            "Y": year % 100 if year_mod_100 else year,
            "M": month,
            "D": day,
            "h": hour % 12 if time_12_h else hour,
            "m": minute,
            "s": second
        }
        for group_idx, (val_id, group_length) in paddings.items():
            group_val = val_map.get(val_id)
            dt_sum += group_val * 10 ** offset
            offset += 2 if group_length == 1 and group_val >= 10 else group_length
        return dt_sum

    return sum_fmt


def prime_second_of_day(year=0, month=0, day=0, hour=0, minute=0, second=0):
    return hour * 3600 + minute * 60 + second


FUNCTION_FORMATTERS = {
    filter_fmt: dt_fmt_to_func(filter_fmt)
    for filter_fmt in DATE_TIME_FILTER_LABELS + TIME_FILTER_LABELS + DATE_FILTER_LABELS
    if filter_fmt not in NON_FORMAT_FILTERS
}

FUNCTION_FORMATTERS[TIME_FILTER_SOD] = prime_second_of_day

