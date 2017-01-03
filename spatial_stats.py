import os.path
import numpy as np
import time, datetime, calendar
from Params import Params

d_duration = Params.disaster_duration

for disaster_id in Params.big_disaster_ids:

    start_date, end_date = d_duration[disaster_id][0], d_duration[disaster_id][1]

    start_date = calendar.timegm(datetime.datetime.strptime(start_date, "%m-%d-%Y %H:%M:%S").timetuple())
    end_date = calendar.timegm(datetime.datetime.strptime(end_date, "%m-%d-%Y %H:%M:%S").timetuple())

    # conver from UTC time to PST time
    start_date, end_date = start_date - 3600 * 8, end_date - 3600 * 8

    # only consider period when disasters happen
    # affected_start_date, affected_end_date = start_date + 3600 * 24, end_date - 3600 * 24     # all time
    affected_start_date, affected_end_date = start_date + 3600 * 24 * Params.peak_day[disaster_id], start_date + 3600 * 24 * (1 + Params.peak_day[disaster_id])

    neg_dict = {}
    for affect in ['_affected', '_unaffected']:
        for filter in ['_filtered']:
            filename = disaster_id + affect + filter
            file = Params.without_tweet_folder + filename + '.txt'
            if os.path.isfile(file):
                data = np.loadtxt(file, dtype=int, delimiter='\t', usecols=(1, 5))  # (time, sentiment)
                neg_rows = [i for i in range(len(data)) if data[i][1] == -1 and affected_start_date < data[i][0] < affected_end_date]
                all_affected_rows = [i for i in range(len(data)) if affected_start_date < data[i][0] < affected_end_date]
                # neg_data, all_data = data[neg_rows][:, 0], data[:, 0]
                neg_dict[affect] = float(len(neg_rows)) / (0.01 + len(all_affected_rows))
                print len(neg_rows), len(all_affected_rows)

    if neg_dict.has_key('_affected') and neg_dict.has_key('_unaffected'):
        print disaster_id, '\t', round(neg_dict['_affected']-neg_dict['_unaffected'], 2), '\t', neg_dict['_affected'], neg_dict['_unaffected']