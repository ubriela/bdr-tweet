
def plot_ratio(neg_ratio):

    """
       Daily plot
       """
    import matplotlib.pyplot as plt

    # plt.plot([0.43, 0.39, 0.42, 0.23, 0.17, 0.13, 0.17, 0.24])
    plt.plot(neg_ratio)
    plt.ylabel('neg_ratio')
    plt.xlabel('day')
    plt.show()

    """
    Hourly plot
    """
    import time
    import datetime

    s = "2014-08-24 06:00:00"
    s_time = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple())
    arr = []
    for k in xrange(1, 8):
        pos = 0
        neg = 0
        total = 0
        set_time = s_time + k * 10800
        with open("./data/state_id_2014-08-24/output/2014-08-24_sent.txt") as f2:
            for i in f2:
                a = [x.strip() for x in i.split(',')]
                t = time.mktime(datetime.datetime.strptime(a[1], "%Y-%m-%d %H:%M:%S").timetuple())
                if set_time > int(t) and int(t) > set_time - 10800:
                    if int(a[5]) == -1:
                        neg += 1
                    elif int(a[5]) == 1:
                        pos += 1
                    total += 1
            if pos == 0:
                arr.append(0)
            else:
                arr.append(neg / ((pos + neg) * 1.0))

            print neg, pos, total
    import matplotlib.pyplot as plt

    plt.plot(arr)
    plt.ylabel('neg_ratio')
    plt.xlabel('hour')
    plt.show()