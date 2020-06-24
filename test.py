# TEST time window
from datetime import datetime, timedelta

dep = '2020-06-23 20:10'
departure = datetime.strptime(dep, "%Y-%m-%d %H:%M")
initial = departure

departures = []
if departure-timedelta(minutes=11) >= datetime.now():
    departure -= timedelta(minutes=10)

departures.append(initial)
for i in range(4):
    departure += timedelta(minutes=(5*i))
    departures.append(departure)

########################################################################3
def calculate_route():
    """Gets route configuration; calculates route; returns route to view as JSON."""
    # Check if time is not in past, otherwise change to present
    departure = datetime.strptime(request.form['departure'], '%Y-%m-%d %H:%M')
    if departure < datetime.now():
        departure = datetime.now() + timedelta(minutes=1)

    initial = departure
    # Adding 4 more departure times
    departures = []
    if departure - timedelta(minutes=11) >= datetime.now():
        departure -= timedelta(minutes=10)

    departures.append(initial)
    # Create time window
    for i in range(4):
        departure += timedelta(minutes=(5*1))
        departures.append(datetime.strftime(departure, '%Y-%m-%d %H:%M'))
