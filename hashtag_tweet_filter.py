import re
import csv
import numpy as np
import sys
import json
import os.path
import glob
import csv
import re
import os

        # do not include general words, e.g., napa, naturaldisaster

def hash_filter(input_file, output_file):
    r = re.compile(
        r"""
        earthquake | aftershock | aftershocks | foreshock | eathquake | eartquake | earthquakes | quake | bigearthquake | bayquake | earrhquake | majorearthquake | postearthquake | earthquakedamage | eathquakedamage | earthquakedamage2014 | 3amearthquake | earthquake2014 | earthquake14 | postearthquakeinspections
        | caearthquake | californiaearthquake | californiaearthquakes | CAearthquake | CAearthquakes | earthquakeCA | norcalearthquake | sfoearthquake | bayareaearthquake | norcaquake
        | napaquake | napaquakes | napaearthquake | southnapaquake | napashake | earthquakeinnapa | southnapaearthquake | eartquakenapa | sonomaquake | southnapearthquake | earthquakenapa | napaquake14 | napaquake2014 | westnapafault | earthquakeruinednapaplans | napastrong
        | prayfornapa | rebuildnapa  | staysafenapa | staystrongnapa | recovernapa | NapaEarthquake6
        | SanFranciscoearthquake | sfearthquake | bayareaquake | sfquake | earthquakesf | earthquakesanfrancisco | earthquakessf | sfeathquake | earthquakesf2014 | earthquakebayarea | sanfranquake2014
        | americancanyonquake | americancanyonearthquake | earthquakeamericancanyon | earthquakeamericancanyon | earthquakeinamericancanyon | prayforamericancanyon
        | myfirstquake | myfirstearthquake | my1stquake | earthquakebelt | earthquakesucks | earthquaketoday | hateearthquakes | pissoffearthquake | fuckyouearthquake | nomoreearthquakes | EarthquakeAt3am | thatwasafuckinghugeearthquake | noearthquakehere | noearthquakes | ItWasAnEarthquake | fearoftheearthquake | terroirquake | earthquakesfiresfloodsetc | caloforniaearthquake | postearthquakepost| earthquakepreparedness | survivedtheearthquake | earthquakereadiness | earthquakekit | earthquakeprobs | earthquakeproblems | haterofearthquakes | earthquakesurviving | firstquakeinnewhouse| earthquakesurvivor | August24EarthquakeSurvivor| sfearthquakewelcome | quakenoob | didntfeelanyearthquake | earthequakemode | isurvivedanearthquake |harvestearthquake | earthquakessuck | ihateearthquakes
        """,
        flags=re.I | re.X)

    # r = re.compile(
    #     r"""
    #     detroitflood | BadNatureShows |storm | DetroitFlood | flood | flooding | DetroitWater | floodageddon | BadNatureShows | weather } Flood | flooded | flood2014 | floods | DetroitFlood2014 | Floodageddon | thegreatflood | floods | Floods | floodedbasement | flood | floodseverywhere | miflood | floodmagedon | detroitfloods | FloodedinDetroit | Detroitflood | Floodpocolypsefloodageddon | stupidfloods | floodmageddon | thegreatflood | flooding | FloodsAren | floodzilla2014 | flood | majorflooding | floodssuck | Detroitflood | zomgfloods | basementflood | floodingintaylor | michiganflood2k14 | FloodDay | flooded | Floodageddon | DetroitFlood2014 | floodedbasement | dearbornflood | floodingindetroit | NoFloodZone | Flooded | StupidFlood | JumangiFlood | FloodedinDetroit | schoolsflooded | detroitflood2014 | floods | MIFlood | theflood | detroitfloods | TheFlood | basementisflooded | floodedroads | FloodsEverywhere | floodmagedon | floodingindearborn | floodrecovery | detroitisflooded | Flood | greatfloodof2014 | beastisflooded | metrodetroitflooding | Flooding | stupidflood | onlyroutenotflooded | FLOODZONE | floodsfordays | aramfloodlive | floodymess | flood2014 | Floodgate | detroitflooding | taylorflood | floodedout | miflood | FloodingProblems | thegreatflood2k14 | Flood2014 | floodpocalypse2014 | DetroitFloodOf2014 | floodseverywhere | GreatFlood | DetroitFloods | flashflood | detroitFlood | FloodWarnings | DetroitFlood | detroitflood | nofloods | livefromtheflood2014 | floodingproblems | Floodpocolypse
    #     """,
    #     flags=re.I | re.X)

    disaster_tweets_count = 0
    with open(input_file, 'rU') as f:
        with open(output_file, "wb") as f2:
            for i in f:
                a = [x for x in i.split(',')]
                tweet = ""
                if len(a) > 5:
                    for i in xrange(0, len(a) - 4):
                        tweet += a[i]
                else:
                    tweet = a[0]
                if re.search(r, tweet):
                    # print disaster_tweets_count
                    disaster_tweets_count += 1
                    f2.write(', '.join(a))
                    disaster_tweets_count += 1

    print "Disaster related tweets: ", disaster_tweets_count

INPUT_FOLDER = './data/gesis/2014-08/state/'

# INPUT_FOLDER = './data/michigian_flood/unaffected_output_tweet/'
# OUTPUT_FOLDER = './data/michigian_flood/unaffected_hash_filtered/'
for file in glob.glob(INPUT_FOLDER + '*/2014*06.txt'):
    filename = re.findall('[^\\\\/]+', file)[-1]

    basepath, filename = os.path.split(file)
    output_file = basepath + '/unfiltered_' + filename

    print output_file

    hash_filter(file, output_file)