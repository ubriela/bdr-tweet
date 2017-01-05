


disaster_array = ["napa_earthquake", "michigan_storm", "california_fire", "washington_mudslide", "iowa_stf", "iowa_storm", "jersey_storm",
                  "oklahoma_storm", "iowa_stf_2", "vermont_storm", "virginia_storm", "texas_storm", "washington_storm",
                  "washington_wildfire", "newyork_storm"]



for ij in xrange(len(disaster_array)):

    print "\n\n", disaster_array[ij]

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_unfiltered_non_spam.txt") as f:
        affect_unfilter = sum(1 for _ in f)
        print 'the number of affected_unfiltered tweets', affect_unfilter

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_unfiltered_non_spam.txt") as f:
        unaffect_unfilter = sum(1 for _ in f)
        print 'the number of unaffected_unfiltered tweets', unaffect_unfilter

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_filtered.txt") as f:
        affect_filter = sum(1 for _ in f)
        print 'the number of affected_filtered tweets', affect_filter

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_filtered.txt") as f:
        unaffect_filter = sum(1 for _ in f)
        print 'the number of unaffected_filtered tweets', unaffect_filter

    print "Total tweets: ", disaster_array[ij], ": ", affect_unfilter + unaffect_unfilter


    ratio_1 = (affect_filter / (affect_unfilter * 1.0)) * 100
    ratio_2 = (unaffect_filter / (unaffect_unfilter * 1.0)) * 100
    ratio_3 = (affect_filter / ((affect_filter + unaffect_filter) * 1.0)) * 100

    print ratio_1
    print ratio_2
    print ratio_3
