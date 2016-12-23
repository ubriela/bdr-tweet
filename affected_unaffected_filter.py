"""
generate affected/unaffected files

"""
import glob
import re


# disaster ids
disaster_array = ["california_fire", "washington_mudslide", "iowa_stf", "iowa_storm", "jersey_storm", "oklahoma_storm", "iowa_stf_2", "vermont_storm", "virginia_storm", "texas_storm", "washington_storm", "washington_wildfire", "newyork_storm"]
affected_county_array = [[33, 9],
                         [73, 47, 19, 65, 51, 43, 7, 77],
                         [119, 143, 59, 63, 189, 191, 5, 167, 41, 147, 109, 81, 37, 65, 19, 149, 35, 21, 151, 91, 197, 69, 23, 193, 93, 161],
                         [131, 89, 191, 5, 43, 197, 23, 77, 49, 181, 125, 117, 135, 101, 57, 185, 7, 51, 111],
                         [15, 7, 5, 1],
                         [151, 3, 53, 93, 45, 43, 11, 73, 83, 129, 39, 17, 109, 9, 149, 15, 75, 51],
                         [23, 93, 79, 83, 75, 13, 47, 171, 113, 105, 97, 165, 9, 99, 157, 95, 103, 31, 123, 107, 183, 139, 57, 111],
                         [1, 7],
                         [107, 35, 43, 45, 87, 15, 7, 67, 101],
                         [423, 349, 217, 35, 471, 453, 209, 91, 187, 493, 55, 351, 241, 199, 291, 201, 167, 39, 215, 489, 61, 21],
                         [73, 61, 29, 9, 31, 27],
                         [37, 47],
                         [89, 45, 49, 73, 37, 121, 29, 9, 13]]

#TWEET_PATH = "./data/washington_wildfire/out/"

#affected_arr = [89, 45, 49, 73, 37, 121, 29, 9, 13]


#affected_arr = [37, 47]

#os.chdir(TWEET_PATH)
#os.makedirs("out_2014-11-28")
#os.chdir("2014-11-28")




for ij in xrange(len(disaster_array)):
    affected_count = 0
    unaffected_count = 0
    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] +"_affected_unfiltered.txt", 'w') as f2:
        for file in glob.glob("./data/disasters/" + disaster_array[ij] + "/out/" + '*/*.txt'):

            textfile = re.findall('[^\\\\/]+', file)[-1]
            filename = re.findall('[^\\\\/]+', file)[-2]
            #print textfile

            if int(textfile[13:16]) in affected_county_array[ij]:
                with open(file, 'rU') as f:
                    for i in f:
                        f2.write( i )
                        affected_count += 1

    print "Total Affected related tweets: ", disaster_array[ij], ": ", affected_count

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_unfiltered.txt", 'w') as f2:
        for file in glob.glob("./data/disasters/" + disaster_array[ij] + "/out/" + '*/*.txt'):

            textfile = re.findall('[^\\\\/]+', file)[-1]
            filename = re.findall('[^\\\\/]+', file)[-2]
            #print textfile

            if int(textfile[13:16]) not in affected_county_array[ij]:
                with open(file, 'rU') as f:
                    for i in f:
                        f2.write( i )
                        unaffected_count += 1

    print "Total UnAffected related tweets: ", disaster_array[ij], ": ",unaffected_count

    print "Total tweets: ", disaster_array[ij], ": ",unaffected_count + affected_count