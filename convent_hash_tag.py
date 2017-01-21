import csv
import glob
import operator
import re

'''
with open("./data/disasters/newyork_storm/newyork_storm_affected_unfiltered.txt", 'rU') as fg:
    with open("./data/disasters/newyork_storm/newyork_storm_affected_unfiltered_user1.txt", "wb") as f2:
        for g in fg:
            a = (g.split(','))

            if int(a[-3]) == 1674592068:
                f2.write(",".join(a))
'''


disaster_array = ["napa_earthquake", "michigan_storm", "newyork_storm", "texas_storm", "iowa_stf", "iowa_stf_2", "iowa_storm", "washington_storm", "jersey_storm", "california_fire", "washington_mudslide"]

all_flood_keywords =r"\bmudslide\b|\blandslide\b|\bwindstorm\b|\bstorm\b|\bhigh wind\b|\btornado\b|\bhurricane\b|\bthunderstorm\b|\bflood\b|\btyphoon\b|\bstrong wind\b|\bhigh water\b|\bflooding\b|\bsnowstorm\b|\brain\b"

all_fire_keywords=r"\bwildfire\b|\bwild fire\b|\bablaze\b"

all_earthquake_keywords=r"\bearthquake\b|\baftershock\b|\baftershocks\b|\bforeshock\b|\beathquake\b|\beartquake\b|\bearthquakes\b|\bquake\b|\bbigearthquake\b|\bearrhquake\b|\bmajorearthquake\b|\bpostearthquake\b|\bearthquakedamage\b|\beathquakedamage\b|\bearthquakedamage\b|\b3amearthquake\b|\bpostearthquakeinspections\b|\bmyfirstquake\b|\bmyfirstearthquake\b|\bmy1stquake\b|\bearthquakebelt\b|\bearthquakesucks\b|\bearthquaketoday\b|\bhateearthquakes\b|\bpissoffearthquake\b|\bfuckyouearthquake\b|\bnomoreearthquakes\b|\bEarthquakeAt3am\b|\bthatwasafuckinghugeearthquake\b|\bnoearthquakehere\b|\bnoearthquakes\b|\bItWasAnEarthquake\b|\bfearoftheearthquake\b|\bterroirquake\b|\bearthquakesfiresfloodsetc\b|\bpostearthquakepost\b|\bearthquakepreparedness\b|\bsurvivedtheearthquake\b|\bearthquakereadiness\b|\bearthquakekit\b|\bearthquakeprobs\b|\bearthquakeproblems\b|\bhaterofearthquakes\b|\bearthquakesurviving\b|\bfirstquakeinnewhouse\b|\bearthquakesurvivor\b|\bquakenoob\b|\bdidntfeelanyearthquake\b|\bearthequakemode\b|\bisurvivedanearthquake\b|\bharvestearthquake\b|\bearthquakessuck\b|\bihateearthquakes\b"

conventional_word = [

all_earthquake_keywords + r" |\bnapaquake\b|\bnapaquakes\b|\bnapaearthquake\b|\bsouthnapaquake\b|\bnapashake\b|\bearthquakeinnapa\b|\bsouthnapaearthquake\b|\beartquakenapa\b|\bsouthnapearthquake\b|\bearthquakenapa\b|\bnapaquake14\b|\bnapaquake2014\b|\brebuildnapa\b|\bstaysafenapa\b|\bstaystrongnapa\b|\brecovernapa\b|\bNapaEarthquake6\b",

all_flood_keywords + r" |\bmichiganflood\b|\bfloodmichigan\b|\bDetroitflood\b|\bdetroitfloods\b",

all_flood_keywords + r" |\bBuffaloSnow\b|\bBuffaloNewYorkSnow\b|\bBuffaloStorm\b|\bSnowstormBuffalo\b|\bbuffalostorm2014\b|\bBuffaloSnowstorm\b|\bbuffaloflood\b|\bnewyorksnowstorm\b",

all_flood_keywords + r" |\bTexasFlood\b|\baustinfloods\b|\btexasstorms\b",

all_flood_keywords + r" |\bIowaflooding\b|\bHurricaneKony2014\b",

all_flood_keywords + r" |\biowastorms\b|\bTyphoonNeoguri\b|\biowafloods\b|\biowaflooding\b|\bIowaStorms2014\b",

all_flood_keywords +r" |\biowastorm\b|\biowaflood\b",

all_flood_keywords + r" |\bwastorm\b|\bwaflood\b|\bwashingtonflood\b|\bwashingtonstorm\b",

all_flood_keywords + r" |\bjerseystorm\b|\bjerseyflood\b|\bjerseyflooding\b",

all_fire_keywords + r" |\bcafire\b|\bcaliforniafire\b|\bcalfires\b|\bLakeCountyFires\b|\bTassajaraFire\b|\bsummitfire\b|\bKesterFire\b|\bTenayaFire\b|\bsunnyvalefire\b|\blacountyfire\b|\bFullertonFire\b|\bSanJoseFire\b|\blaurelesfire\b|\byosemitefire\b|\btassajarafire\b|\bButteFire\b",

all_fire_keywords + " | " + all_flood_keywords + r" |\bWAWILDFIRE\b|\bwafire\b|\bwashingtonfires2015\b|\bTacomaFire\b|\bwashingtononfire\b|\bokanaganfire\b|\bchelanfire\b|\bWashingtonFires\b"
]

import re

for ij in xrange(len(disaster_array)):
    # do not include general words, e.g., napa, naturaldisaster

    def hash_filter(input_file, s):

        output_file = input_file[:-23] + "filtered_conv_hash.txt"

        r = re.compile(
            s,
            flags=re.I | re.X)

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
                        # print "Disaster related tweets: ", disaster_tweets_count


    f = ["./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_unfiltered_non_spam.txt",
         "./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_unfiltered_non_spam.txt"]

    for i in f:
        l = conventional_word[ij].split('|')
        print "manually hash :", len(l)
        hash_filter(i, conventional_word[ij])

    print '\n', disaster_array[ij]

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_filtered_conv_hash.txt") as f:
        print 'the number of affected hash filtered tweets', sum(1 for _ in f)

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_filtered_conv_hash.txt") as f:
        print 'the number of unaffected hash filtered tweets', sum(1 for _ in f)

    print '\n'








