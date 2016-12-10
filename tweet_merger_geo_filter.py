"""
This function merger all the tweet data day wise into one single folder
It also removes the extra comma within the tweet data and makes a

"""


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