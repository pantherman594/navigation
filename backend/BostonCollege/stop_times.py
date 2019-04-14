from datetime import datetime, timedelta
import csv
import requests


def input_times(default=""):
    allTimes = []
    times = []
    time = input("Paste times: ")
    while time != "":
        if (time == "|"):
            allTimes.append(times)
            times = []
        else:
            times.append(datetime.strptime(time, "%I:%M:%S %p"))
        time = input("")

    allTimes.append(times)
    return allTimes


stops = dict()

commAllStops = [
    4068910,
    4068914,
    4068918,
    4068902,
    4068922,
    4068930,
    4068938,
    4068942,
    4068946,
    4068950,
    4068934,
    4068926,
    4068906
]

commDirStops = [
    4068910,
    4068922,
    4068930,
    4068938,
    4068942,
    4068946,
    4068950,
    4068934,
    4068926,
    4068906
]

commExpStops = [
    4068910,
    4068922,
    4068930,
    4068938,
    4068942,
    4068946,
    4068950,
    4068934,
    4068926
]

newtonAllStops = [
    4160230,
    4068278,
    4068902,
    4068906,
    4068910,
    4068914,
    4068918,
    4160234
]

newtonLtdStops = [
    4160230,
    4068278,
    4068902,
    4068914,
    4068918,
    4160234
]

newtonDirStops = [
    4160230,
    4068278,
    4068902
]

newtonWkdStops = [
    4160230,
    4068910
]

with open('stops.txt', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        stops[int(row['stop_id'])] = [row['stop_lat'], row['stop_lon']]

schedules = [
    [commDirStops, 'comm_dir'],
    [commExpStops, 'comm_exp'],
    [commAllStops, 'comm_all_mtw'],
    [commAllStops, 'comm_all_thu'],
    [commAllStops, 'comm_all_fri'],
    [commAllStops, 'comm_all_sat'],
    [commAllStops, 'comm_all_sun'],
    [newtonDirStops, 'newt_dir'],
    [newtonLtdStops, 'newt_ltd'],
    [newtonAllStops, 'newt_all_mtw'],
    [newtonAllStops, 'newt_all_thf'],
    [newtonWkdStops, 'newt_wkd_sat'],
    [newtonWkdStops, 'newt_wkd_sun'],
]

toPrint = ""
outFmt = "%H:%M:%S"

allTimes = input_times()
num = 0
for schedule in schedules:
    # times = allTimes[num]
    num += 1

    currStops = schedule[0]

    print(schedule[1])
    # print('/'.join([','.join(stops[stop]) for stop in currStops + [currStops[0]]]))

    start = ','.join(stops[currStops[0]])
    end = start
    waypoints = '|'.join([','.join(stops[stop]) for stop in currStops[1:]])
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = dict(
        origin=start,
        destination=end,
        waypoints=waypoints,
        key='AIzaSyBAWAq1xYm7c8dlb3Z1vWAwffL5YHrvUEM'
    )

    resp = requests.get(url=url, params=params)
    print(resp.url)
    continue
    print(resp.json())
    print(resp.json()['routes'][0]['overview_polyline']['points'])
    continue

    i = 0
    for startTime in times:
        time = startTime
        j = 0
        name = schedule[1] + "_" + str(i)
        for stop in currStops[0:-1]:
            arrive = time
            time += timedelta(minutes=1)
            depart = time
            toPrint += "{}\t{}\t{}\t{}\t{}\n".format(name, stop, datetime.strftime(arrive, outFmt), datetime.strftime(depart, outFmt), str(j))
            time += timedelta(seconds=legs[j]['duration']['value'])
            j += 1
        toPrint += "{}\t{}\t{}\t{}\t{}\n".format(name, currStops[-1], datetime.strftime(time, outFmt), datetime.strftime(time + timedelta(minutes=1), outFmt), str(j))
        i += 1
print(toPrint)
