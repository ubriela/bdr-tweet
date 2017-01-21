'''
disaster_array = ["napa_earthquake", "michigan_storm", "california_fire", "washington_mudslide", "iowa_stf", "iowa_storm", "jersey_storm",
                  "oklahoma_storm", "iowa_stf_2", "vermont_storm", "virginia_storm", "texas_storm", "washington_storm",
                  "washington_wildfire", "newyork_storm"]
'''

disaster_array = ["napa_earthquake", "michigan_storm", "newyork_storm", "texas_storm", "iowa_stf", "iowa_stf_2", "iowa_storm", "washington_storm", "jersey_storm", "california_fire", "washington_mudslide"]

for ij in xrange(len(disaster_array)):

    print "\n\n", disaster_array[ij]

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_filtered_conv_hash.txt") as f:
        affect_filter = sum(1 for _ in f)
        print 'the number of affected hash filtered tweets', affect_filter

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_filtered_conv_hash.txt") as f:
        unaffect_filter = sum(1 for _ in f)
        print 'the number of unaffected hash filtered tweets', unaffect_filter


    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_filtered_classify.txt") as f:
        affect_filter_related = sum(1 for _ in f)
        print 'the number of affected_' + 'classification_related tweets', affect_filter_related

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_filtered_classify.txt") as f:
        unaffect_filter_related = sum(1 for _ in f)
        print 'the number of unaffected_' + 'classification_related tweets', unaffect_filter_related

        #print "Total tweets: ", disaster_array[ij], ": ", affect_unfilter + unaffect_unfilter

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_filtered_conv_hash.txt") as f:
        #affect_filter = sum(1 for _ in f)
        #print 'the number of affected_filtered tweets', affect_filter
        affected_filter_arr = []
        for line in f:
            a = [x.strip() for x in line.split(',')]
            #print len(a)
            if len(a) > 5:
                st = ""
                for i in xrange(0, len(a) - 4):
                    if i == len(a) - 5:
                        st += a[i]
                    else:
                        st += a[i] + ", "
                affected_filter_arr.append(st)
                #for i in xrange(len(a) - 4, len(a)):
                #    arr.append(a[i])
            else:
                affected_filter_arr.append(a[0])
        #print len(arr)


    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_filtered_conv_hash.txt") as f:
        #unaffect_filter = sum(1 for _ in f)
        #print 'the number of unaffected_filtered tweets', unaffect_filter
        unaffected_filter_arr = []
        for line in f:
            a = [x.strip() for x in line.split(',')]
            #print len(a)
            if len(a) > 5:
                st = ""
                for i in xrange(0, len(a) - 4):
                    if i == len(a) - 5:
                        st += a[i]
                    else:
                        st += a[i] + ", "
                unaffected_filter_arr.append(st)
                #for i in xrange(len(a) - 4, len(a)):
                #    arr.append(a[i])
            else:
                unaffected_filter_arr.append(a[0])
        #print len(arr)


    #print "Total tweets: ", disaster_array[ij], ": ", affect_unfilter + unaffect_unfilter



    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_filtered_classify.txt") as f:
        #affect_filter_related = sum(1 for _ in f)
        #print 'the number of affected_' + 'classification_related tweets', affect_filter_related
        affected_related_arr = []
        for line in f:
            a = [x.strip() for x in line.split(',')]
            # print len(a)
            if len(a) > 5:
                st = ""
                for i in xrange(0, len(a) - 4):
                    if i == len(a) - 5:
                        st += a[i]
                    else:
                        st += a[i] + ", "
                affected_related_arr.append(st)
                # for i in xrange(len(a) - 4, len(a)):
                #    arr.append(a[i])
            else:
                affected_related_arr.append(a[0])



    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_filtered_classify.txt") as f:
        #unaffect_filter_related = sum(1 for _ in f)
        #print 'the number of unaffected_' + 'classification_related tweets', unaffect_filter_related
        unaffected_related_arr = []
        for line in f:
            a = [x.strip() for x in line.split(',')]
            # print len(a)
            if len(a) > 5:
                st = ""
                for i in xrange(0, len(a) - 4):
                    if i == len(a) - 5:
                        st += a[i]
                    else:
                        st += a[i] + ", "
                unaffected_related_arr.append(st)
                # for i in xrange(len(a) - 4, len(a)):
                #    arr.append(a[i])
            else:
                unaffected_related_arr.append(a[0])
    affected_output = "./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_intersection.txt"
    unaffected_output = "./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_intersection.txt"

    affected_unrelated_output = "./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_unrelated_intersection.txt"
    unaffected_unrelated_output = "./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_unrelated_intersection.txt"
    count_filter = 0

    with open(affected_unrelated_output, "wb") as f3:
        with open(affected_output, "wb") as f2:
            for i in affected_filter_arr:
                #print i
                if i in affected_related_arr:
                    f2.write(i[1:] + "\n")
                    count_filter += 1
                else:
                    f3.write(i[1:] + "\n")
    print disaster_array[ij], " Affected Intersection: ", count_filter

    count_unfilter = 0

    with open(unaffected_unrelated_output, "wb") as f3:
        with open(unaffected_output, "wb") as f2:
            for i in unaffected_filter_arr:
                # print i
                if i in unaffected_related_arr:
                    f2.write(i[1:] + "\n")
                    count_unfilter += 1
                else:
                    f3.write(i[1:] + "\n")
    print disaster_array[ij], " Unaffected Intersection: ", count_unfilter

    '''
    for i in affected_related_arr:
        # print i
        if i in affected_filter_arr:
            continue
        else:
            print i
    '''
    print count_unfilter

    print "Recall hash affected :", (count_filter / (affect_filter * 1.0)) * 100
    print "Recall classify affected :", (count_filter / (affect_filter_related * 1.0)) * 100

    print "Recall hash unaffected :", (count_unfilter / (unaffect_filter * 1.0)) * 100
    print "Recall classify unaffected :", (count_unfilter / (unaffect_filter_related * 1.0)) * 100

        #print "Total tweets: ", disaster_array[ij], ": ", affect_unfilter + unaffect_unfilter
