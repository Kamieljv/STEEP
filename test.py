# TEST time window
from datetime import datetime
from datetime import timedelta

dep = '2020-06-19 12:00'
departure = datetime.strptime(dep, "%Y-%m-%d %H:%M")
initial = departure

departures = [initial]
for i in range(4):
    departure += timedelta(minutes=5)
    departures.append(departure)

#make a emissions list
em_list = [32.32, 46.54, 34.38, 67, 54]
def diff_emission(list):
    diff_list = []
    for i in range(len(list)):
        if i <= len(list)-2:
            diff = round((list[i+1] - list[0]),2)
            i = i + 1
            diff_list.append(diff)
    return diff_list





