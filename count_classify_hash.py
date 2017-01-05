disaster_array = ["napa_earthquake", "michigan_storm", "california_fire", "washington_mudslide", "iowa_stf", "iowa_storm", "jersey_storm",
                  "oklahoma_storm", "iowa_stf_2", "vermont_storm", "virginia_storm", "texas_storm", "washington_storm",
                  "washington_wildfire", "newyork_storm"]


#type = ["filtered", "unfiltered"]

for ij in xrange(1, len(disaster_array)):

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



    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_" + "classification_related.txt") as f:
        affect_filter_related = sum(1 for _ in f)
        print 'the number of affected_' + 'classification_related tweets', affect_filter_related

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_" + "classification_unrelated.txt") as f:
        affect_filter_unrelated = sum(1 for _ in f)
        print 'the number of affected_' + 'classification_unrelated tweets', affect_filter_unrelated

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_" + "classification_related.txt") as f:
        unaffect_filter_related = sum(1 for _ in f)
        print 'the number of unaffected_' + 'classification_related tweets', unaffect_filter_related

        #print "Total tweets: ", disaster_array[ij], ": ", affect_unfilter + unaffect_unfilter

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_" + "classification_unrelated.txt") as f:
        unaffect_filter_unrelated = sum(1 for _ in f)
        print 'the number of unaffected_' + 'classification_unrelated tweets', unaffect_filter_unrelated


    new_affected = affect_filter_related + affect_filter_unrelated

    new_unaffected = unaffect_filter_related + unaffect_filter_unrelated

    '''
    print "\n % of duplicates\n"
    print "Affected : ", str(((affect_filter - new_affected) / (affect_filter * 1.0) * 100))
    print "\n UnAffected : ", str(((unaffect_filter - new_unaffected) / (unaffect_filter * 1.0)) * 100)
    '''

    print "classify related ratio: ", (affect_filter_related / (affect_unfilter * 1.0) ) * 100
    print "classify unrelated ratio: ", (unaffect_filter_related / (unaffect_unfilter * 1.0)) * 100
    print "hash related ratio: ", (affect_filter / (affect_unfilter * 1.0)) * 100
    print "classify related ratio: ", (unaffect_filter / (unaffect_unfilter * 1.0)) * 100
