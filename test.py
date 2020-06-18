# TEST time window
from datetime import datetime
from datetime import timedelta

dep = '2020-06-19 12:00'
departure = datetime.strptime(dep, "%Y-%m-%d %H:%M")
initial = departure

departures = [initial]
for i in range(5):
    departure += timedelta(minutes=5)
    departures.append(departure)


