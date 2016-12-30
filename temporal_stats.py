import os.path
import numpy as np
import time, datetime, calendar

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from Params import Params
import numpy as np

d_duration = Params.disaster_duration

for unit_bin in ['day', 'hour']:
    for graph_type in ['senti_both', 'senti_score']:
        for disaster_id in Params.disaster_ids:
            start_date, end_date = d_duration[disaster_id][0], d_duration[disaster_id][1]

            start_date = calendar.timegm(datetime.datetime.strptime(start_date, "%m-%d-%Y %H:%M:%S").timetuple())
            end_date = calendar.timegm(datetime.datetime.strptime(end_date, "%m-%d-%Y %H:%M:%S").timetuple())

            # conver from UTC time to PST time
            start_date, end_date = start_date - 3600*8, end_date - 3600*8

            for affect in ['_affected', '_unaffected']:
                for filt in ['_filtered', '_unfiltered']:
                    filename = disaster_id + affect + filt
                    file = Params.without_tweet_folder + filename + '.txt'
                    print file
                    if os.path.isfile(file):
                        data = np.loadtxt(file, dtype=int, delimiter='\t', usecols=(1,5))   # (time, sentiment)
                        # neg_rows = [i for i in range(len(data)) if data[i][1] == -1]
                        # pos_rows = [i for i in range(len(data)) if data[i][1] == 1]
                        # neg_data, pos_data, all_data = data[neg_rows][:,0], data[pos_rows][:,0], data[:,0]

                        all_data = data[:,0]
                        neg_data = np.array(filter(lambda x : x[1] == -1, data))[:,0]
                        pos_data = np.array(filter(lambda x : x[1] == 1, data))[:,0]


                        if unit_bin == 'hour':
                            bins = (end_date - start_date)/(3600)
                        elif unit_bin == 'day':
                            bins = (end_date - start_date) / (3600*24)
                        # bins = 10
                        neg_hist, neg_edges = np.histogram(neg_data, bins)
                        pos_hist, pos_edges = np.histogram(pos_data, bins)
                        all_hist, all_edges = np.histogram(all_data, bins)

                        neg_ratio = np.array(neg_hist, dtype=float)/ (all_hist + 0.001)

                        sentiment_score = pos_hist - neg_hist

                        values = sentiment_score

                        # plot graph
                        fig, ax = plt.subplots()

                        if graph_type == 'senti_score':
                            index = np.arange(len(values))
                            bar_width = 0.2
                            plt.bar(index, values, bar_width, alpha=0.4, color='g', label='Sentiment score')
                            ticks = [str(i + 1) for i in range(len(values))]
                            ax.set_xticks(index + bar_width/2)
                            ax.set_xticklabels(ticks)
                            ax.set_xlabel('Time (hour)')
                            ax.set_ylabel('Sentiment score')
                            ax.legend()
                            ax.set_title(filename)

                        if graph_type == 'senti_both':
                            index = np.arange(len(values))
                            bar_width = 0.2
                            rects1 = ax.bar(index, neg_hist, bar_width, alpha=0.4, color='r')
                            rects2 = ax.bar(index + bar_width, pos_hist, bar_width, alpha=0.4, color='y')
                            ticks = [str(i + 1) for i in range(len(pos_hist))]
                            ax.set_xticks(index + bar_width)
                            ax.set_xticklabels(ticks)
                            ax.set_xlabel('Time (' + unit_bin + ')')
                            ax.set_ylabel('Sentiment score')
                            ax.legend((rects1[0], rects2[0]), ('Negative', 'Positive'))
                            ax.set_title(filename)

                        # plt.show()
                        plt.savefig('./output/graph/' + graph_type + '_' + unit_bin + '_' + filename + '.png', format='png', dpi=400)