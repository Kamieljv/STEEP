c = []
a = 0
for i in range(4):
    a += 5
    c.append(a)

from datetime import datetime
from datetime import timedelta

now = datetime.now()
aDay = timedelta(days=1)
now = now + aDay
print(now.strftime('%Y-%m-%d'))
