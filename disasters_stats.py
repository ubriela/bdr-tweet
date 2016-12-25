import os.path
import numpy as np
import time, datetime, calendar

import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches

from Params import Params


d_duration = Params.disaster_duration

for disaster_id in Params.disaster_ids:
    start_date, end_date = d_duration[disaster_id], end_date

    start_date = calendar.timegm(datetime.datetime.strptime(start_date, "%m-%Y-%d %H:%M:%S").timetuple())
    end_date = calendar.timegm(datetime.datetime.strptime(end_date, "%m-%Y-%d %H:%M:%S").timetuple())

    for affect in ['_affected', '_unaffected']:
        for filter in ['_filtered', '_unfiltered']:
            filename = disaster_id + affect + filter
            file = Params.without_tweet_folder + filename
            if os.path.isfile(file):
                data = np.loadtxt(file, dtype=int, delimiter='\t', usecols=(1,5))   # (time, sentiment)
                neg_rows = [i for i in range(len(data)) if data[i][1] == -1]
                neg_data, all_data = data[neg_rows][:,0], data[:,0]

                bins = (end_date - start_date)/3600000
                neg_hist, neg_edges = np.histogram(neg_data, bins)
                all_hist, all_edges = np.histogram(all_data, bins)

                neg_ratio = neg_hist/all_hist

                # plot graph
                index = np.arange(len(neg_ratio))
                bar_width = 0.2
                plt.bar(index, neg_ratio, bar_width, alpha=0.4, color='g', label='Negative ratio')
                ticks = [str(i + 1) for i in range(len(neg_ratio))]
                plt.xticks(index + bar_width/2, ticks)
                plt.xlabel('Time (hour)')
                plt.ylabel('Negative ratio')
                plt.legend()
                plt.show()
                # savefig('./output/graph/' + filename + '.png', format='png', dpi=400)