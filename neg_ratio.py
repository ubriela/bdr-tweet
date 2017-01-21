import glob
from Params import Params

disaster_array = ["napa_earthquake", "michigan_storm", "california_fire", "washington_mudslide", "iowa_stf", "iowa_storm", "jersey_storm",
                  "oklahoma_storm", "iowa_stf_2", "vermont_storm", "virginia_storm", "texas_storm", "washington_storm",
                  "washington_wildfire", "newyork_storm"]

area = ["affected_filtered", "unaffected_filtered"]
type = ["hash", "classify"]

# extract tweet_only

for ij in disaster_array:
    for i in area:
        for j in type:
            for file in glob.glob(Params.with_sentiment_folder + ij + "_" + i + "_" + j + ".txt"):
                neg = 0
                pos = 0
                with open(file, 'rU') as f:
                    for a in f:
                        a = a.split(',')
                        if int(a[-1]) < 0:
                            neg += 1
                        else:
                            pos += 1

                print ij
                print i , j ,"Neg ratio : ", ((neg * 1.0) / (neg + pos)) * 100





