"""
Cron format from man 5 crontab:

  field          allowed values
  -----          --------------
  minute         0-59
  hour           0-23
  day of month   1-31
  month          1-12 (or names, see below)
  day of week    0-7 (0 or 7 is Sun, or use names)
"""

import re

NUMBER_RE = re.compile('\d+')
ITEM_RE = re.compile(r'(\d+-\d+/\d+)|(\d+-\d+)|(\d+)')
RANGES = ('0-59', '0-23', '1-31', '1-12', '0-7')

# Names are allowed for months and weekdays
MONTHS = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')
WEEKDAYS = ('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
NAME_MAP = (
    {},
    {},
    {},
    dict(zip(MONTHS, range(1, 13))),
    dict(zip(WEEKDAYS, range(0, 8))),
)
NAME_REPLACE_RE = [re.compile('({})'.format('|'.join(x))) for x in NAME_MAP]

def resolve_names(spec):
    """
    Resolves things like @start, @hourly, etc.
    into a numerical representation that can be
    parsed with parse_spec.
    * gets replaced with the appropriate range
    """
    spec = spec.lower()
    parts = spec.split()
    assert len(parts) == 5, "Invalid spec. Need 5 white-space separated items"

    # Replace '*' with the appropriate ranges.
    parts = [p.replace('*', r) for p, r in zip(parts, RANGES)]

    # Replace named values. Could be prettier.
    parts = [
        name_replace_re.sub(lambda x: str(name_map.get(x.group(1), '')), p)
        for p, name_replace_re, name_map in zip(parts, NAME_REPLACE_RE, NAME_MAP)
    ]
    return ' '.join(parts)

def _numbers(s):
    return tuple(int(x) for x in NUMBER_RE.findall(s))

def parse_spec(spec):
    """
    Parses a specs like
    '* * * * *' or '1 0 0 0 0'
    into a set that can be evaluated
    """
    parts = spec.split()
    sets = [set() for x in range(5)]
    for p, out_set in zip(parts, sets):

        for range_step, range_, number in ITEM_RE.findall(p):
            if range_step:
                b, e, s = _numbers(range_step)
                out_set |= set(range(b, e+1, s))
            if range_:
                b, e = _numbers(range_)
                out_set |= set(range(b, e+1))
            if number:
                b, = _numbers(number)
                out_set.add(b)

    return sets
