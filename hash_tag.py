import os
import csv
import glob
import operator
import re

#with open("", 'rU') as f:
#    rd = csv.reader(f, delimiter=",")
#arr = [11,12,13]


disaster_array = ["california_fire", "washington_mudslide", "iowa_stf", "iowa_storm", "jersey_storm", "oklahoma_storm", "iowa_stf_2", "vermont_storm", "virginia_storm", "texas_storm", "washington_storm", "washington_wildfire", "newyork_storm"]
state_code = [6, 53, 19, 19, 34, 40, 19, 50, 54, 48, 53, 53, 36]

hash_1 = [r"""fire | wildfire | wild fire | californiafire | burning | bonfire""",
          r"""mudslide | slide | wild fire | fire | wildfire | earthfall | avalanche | landslide""",
          r"""storm | windstorm | tempest | high wind | strong wind | tornado | cyclone | twister | typhoon | whirlwind | hurricane | flood | high water | flooding | wind | breeze""",
          r"""storm | windstorm | tempest | high wind | strong wind | tornado | cyclone | twister | typhoon | whirlwind | hurricane | flood | high water | flooding""",
          r"""storm | windstorm | tempest | high wind | strong wind""",
          r"""storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding""",
          r"""storm | windstorm | tempest | high wind | strong wind | tornado | cyclone | twister | typhoon | whirlwind | hurricane | flood | high water | flooding | wind | breeze""",
          r"""storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding""",
          r"""earthfall | avalanche | landslide | mudslide | storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding""",
          r"""storm | windstorm | tempest | high wind | strong wind | tornado | cyclone | twister | typhoon | whirlwind | hurricane | flood | high water | flooding | wind | breeze""",
          r"""wind | breeze | storm | windstorm""", #wash storm
          r"""fire | burning | wildfire""", #wash wildfire
          r"""storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding | snow | snowstorm | storm | blizzard"""] #new york


#INPUT_FOLDER = "./data/washington_wildfire/hash"
for ij in xrange(len(disaster_array)):
    l = {}
    r = re.compile(
            hash_1[ij],
            flags=re.I | re.X)

    for file in glob.glob("./data/" + disaster_array[ij] + "/hash" + '*/*.txt'):
        #print file
        filename = re.findall('[^\\\\/]+', file)[-1]

        idfilepath = str(filename)

        if int(idfilepath[11:13]) == state_code[ij]:
            #print idfilepath
            with open("./data/" + disaster_array[ij] + "/hash" + "/" + idfilepath, 'rU') as f:
                rd = csv.reader(f, delimiter="\t")
                #print len(rd)

                for i in rd:
                    if i[0] in l:
                        l[i[0]] += int(i[1])
                    else:
                        l[i[0]] = int(i[1])
        #print len(l)


    hash_2 = []
    #print l
    for i in l:
        if re.search(r, str(i)):
            hash_2.append(i)
    print len(hash_2)
    print (hash_2)

    s = 'r"""'
    for i in hash_2:
        s += i + " | "

    s = s[:-3]
    s += '"""'
    print s

    #sorted_x = sorted(l.items(), key=operator.itemgetter(1))
    #for i in xrange(len(sorted_x)):
    #   print sorted_x[-1-i]


    import re
    import csv

            # do not include general words, e.g., napa, naturaldisaster

    def hash_filter(input_file, s):

        output_file = input_file[:-14] + "filtered.txt"

        r = re.compile(
            s,
            flags=re.I | re.X)
        disaster_tweets_count = 0
        with open(input_file, 'rU') as f:
            rd = csv.reader(f, delimiter=",")
            with open(output_file, "wb") as f2:
                for a in rd:
                    arr = []
                    #a = [x.strip() for x in line.split(',')]

                    if len(a) > 5:
                        st = ""
                        for i in xrange(0, len(a) - 4):
                            if i == len(a) - 5:
                                st += a[i]
                            else:
                                st += a[i] + ", "
                        arr.append(st)
                        for i in xrange(len(a) - 4, len(a)):
                            arr.append(a[i])
                        a = []
                        a = arr
                    if re.search(r, a[0]):
                        #print disaster_tweets_count
                        disaster_tweets_count += 1
                        f2.write(', '.join(a) + '\n')

                #print "Disaster related tweets: ", disaster_tweets_count


    f = ["./data/" + disaster_array[ij] + "/" + disaster_array[ij] +"_affected_unfiltered.txt", "./data/" + disaster_array[ij] + "/" + disaster_array[ij] +"_unaffected_unfiltered.txt"]

    for i in f:
        hash_filter(i, s)


    print disaster_array[ij]

    with open("./data/" + disaster_array[ij] + "/" + disaster_array[ij] +"_affected_filtered.txt") as f:
        print sum(1 for _ in f)

    with open("./data/" + disaster_array[ij] + "/" + disaster_array[ij] +"_unaffected_filtered.txt") as f:
        print sum(1 for _ in f)