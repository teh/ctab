# Simple cron parsing tools

These tools help with parsing the time specs in cron files. Time specs look like '* * * * Sun' or '1-30/5 * * * *'.
These tools do _not_ parse entire cron files.

A simple example:

```python
import datetime
from ctab.ctab import parse, match, cron_iter

spec = parse('* * * * *')
print match(spec, datetime.datetime.utcnow())
# Prints True

i = cron_iter(spec)
print i.next()
print i.next()
# Prints something like:
# 2012-04-27 13:58:09.152578
# 2012-04-27 13:59:09.152578
```


# Testing

Install nose test, then run:

```
nosetests
```