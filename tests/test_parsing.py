import datetime
from nose.tools import eq_
from ctab import ctab

def test_parse_spec():
    eq_(ctab.parse_spec('0-59/2 0-23 1-32 1-12 0-7'), 
        ctab.ParsedSpec(minute=set([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58]), hour=set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]), dom=set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]), month=set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]), dow=set([0, 1, 2, 3, 4, 5, 6, 7]))
    )
    eq_(ctab.parse_spec('7 0-23 1-32 1-12 0-7'),
        ctab.ParsedSpec(minute=set([7]), hour=set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]), dom=set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]), month=set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]), dow=set([0, 1, 2, 3, 4, 5, 6, 7]))
    )
    eq_(ctab.parse_spec('0-20/3,40-59/3 0 1 1  0-7'),
        ctab.ParsedSpec(minute=set([0, 3, 6, 40, 9, 43, 12, 46, 15, 49, 18, 52, 55, 58]), hour=set([0]), dom=set([1]), month=set([1]), dow=set([0, 1, 2, 3, 4, 5, 6, 7]))
        )

def test_resolve_names():
    eq_(ctab.resolve_names('* * * * *'), '0-59 0-23 1-31 1-12 0-7')
    eq_(ctab.resolve_names('* * * Oct suN'), '0-59 0-23 1-31 10 7')

def test_match():
    now = datetime.datetime.utcnow()
    sunday = datetime.datetime(2012, 4, 29)
    monday = datetime.datetime(2012, 4, 30)

    # Now
    spec = ctab.parse_spec(ctab.resolve_names('* * * * *'))
    eq_(ctab.match(spec, now), True)

    # Day of week
    spec = ctab.parse_spec(ctab.resolve_names('* * * * 0'))
    eq_(ctab.match(spec, sunday), True)
    eq_(ctab.match(spec, monday), False)

    spec = ctab.parse_spec(ctab.resolve_names('* * * * 7'))
    eq_(ctab.match(spec, sunday), True)
    eq_(ctab.match(spec, monday), False)
