'''

def filter(min_lat, min_lon, max_lat, max_lon):
    county_array = [6075, 6055, 6041, 6033, 6097, 6113, 6095, 6011, 6013, 6001, 6081]
    county_array.sort()
    day = [25,26,27,28,29,30,31]
    for j in day:
        with open("./data/state_id_2014-08-24/output/2014-08-" + str(j) + ".txt", "wb") as f2:
            for i in county_array:
                with open("./data/state_id_2014-08-25/output/2014-08-"+str(j)+"_0" + str(i) + "_ID.txt") as f:
                    for line in f:
                        arr = []
                        a = [x.strip() for x in line.split(',')]

                        if len(a) > 5:

                            st = ""
                            for i in xrange(0, len(a) - 4):
                                if i != len(a) - 5:
                                    st += a[i]
                                else:
                                    st += a[i]
                            arr.append(st)
                            for i in xrange(len(a) - 4, len(a)):
                                arr.append(a[i])
                            a = []
                            a = arr
                        lat, lon = float(a[len(a) - 2]), float(a[len(a) - 1])
                        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                            f2.write(', '.join(a) + '\n')

filter(37.382166, -123.561700, 39.048834, -121.061700)



county_array = [6075, 6055, 6041, 6033, 6097, 6113, 6095, 6011, 6013, 6001, 6081]
a = []
with open("./data/state_id_2014-08-24/output/2014-08-24.txt", "wb") as f2:
    for i in county_array:
        with open("./data/state_id_2014-08-24/output/2014-08-24_0" + str(i) + ".txt") as f:
            for line in f:
                f2.write(line)



def filter_tweets(min_lat, min_lon, max_lat, max_lon, file, file_out):
    with open(file) as f:
        with open(file_out, "w") as f2:
            for line in f:
                a = [x.strip() for x in line.split(',')]
                lat, lon = float(a[len(a) - 2]), float(a[len(a) - 1])
                if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                    f2.write(', '.join(a) + '\n')

filter_tweets(37.382166, -123.561700, 39.048834, -121.061700, "./data/state_id_2014-08-24/output/2014-08-24.txt", "./data/state_id_2014-08-24/output/2014-08-24_geo_filter.txt")




import matplotlib.pyplot as plt
#plt.plot([0.43, 0.39, 0.42, 0.23, 0.17, 0.13, 0.17, 0.24])
plt.plot([0.22, 0.14, 0.15, 0.078, 0.065, 0.054, 0.057, 0.086])
my_xticks = ['John','Arnold','Mavis','Matt']
plt.xticks(x, my_xticks)
plt.ylabel('neg_ratio')
plt.xlabel('day')
plt.show()

'''

import time
import datetime

s = "2014-08-24 06:00:00"
s_time = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple())
arr = []
for k in xrange(1,23):
    pos = 0
    neg = 0
    total = 0
    set_time = s_time + k*3600
    with open("./data/state_id_2014-08-24/output/2014-08-24_sent.txt") as f2:
        for i in f2:
            a = [x.strip() for x in i.split(',')]
            t = time.mktime(datetime.datetime.strptime(a[1], "%Y-%m-%d %H:%M:%S").timetuple())
            if set_time > int(t) and int(t) > set_time - 3600:
                if int(a[5]) == -1:
                    neg += 1
                elif int(a[5]) == 1:
                    pos += 1
                total += 1
        if pos == 0:
            arr.append(0)
        else:
            arr.append(neg / ((pos) * 1.0))

        print neg, pos, total
import matplotlib.pyplot as plt
#plt.plot([0.43, 0.39, 0.42, 0.23, 0.17, 0.13, 0.17, 0.24])
plt.plot(arr)
plt.ylabel('neg_ratio')
plt.xlabel('hour')
plt.show()

