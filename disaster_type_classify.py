import re
import glob
all_flood_keywords = "mudslide | landslide | windstorm | storm | high wind | tornado | hurricane | thunderstorm | flood | typhoon | strong wind | high water | flooding | snowstorm | rain"  # keywords related to flood-related disaster

all_fire_keywords = "wildfire | wild fire | ablaze"  # keywords related to wildfire-related disaster

all_earthquake_keywords = "earthquake | aftershock | aftershocks | foreshock | eathquake | eartquake | earthquakes | quake | bigearthquake | earrhquake | majorearthquake | postearthquake | earthquakedamage | eathquakedamage | earthquakedamage | 3amearthquake | postearthquakeinspections | myfirstquake | myfirstearthquake | my1stquake | earthquakebelt | earthquakesucks | earthquaketoday | hateearthquakes | pissoffearthquake | fuckyouearthquake | nomoreearthquakes | EarthquakeAt3am | thatwasafuckinghugeearthquake | noearthquakehere | noearthquakes | ItWasAnEarthquake | fearoftheearthquake | terroirquake | earthquakesfiresfloodsetc | postearthquakepost | earthquakepreparedness | survivedtheearthquake | earthquakereadiness | earthquakekit | earthquakeprobs | earthquakeproblems | haterofearthquakes | earthquakesurviving | firstquakeinnewhouse | earthquakesurvivor | quakenoob | didntfeelanyearthquake | earthequakemode | isurvivedanearthquake | harvestearthquake | earthquakessuck | ihateearthquakes"  # keywords related to earthquake-related disaster

all_fire_flood_keywords = "ablaze | wildfire | mudslide | landslide | windstorm | storm | high wind | tornado | hurricane | thunderstorm | flood | typhoon | strong wind | wild fire | high water | flooding | snowstorm | rain"  # keywords related to flood-related disaster


flood = re.compile(
        all_flood_keywords,
        flags=re.I | re.X)

fire = re.compile(
        all_fire_keywords,
        flags=re.I | re.X)

earthquake = re.compile(
        all_earthquake_keywords,
        flags=re.I | re.X)

fire_flood = re.compile(
        all_fire_flood_keywords,
        flags=re.I | re.X)


'''

fire_c = 0

with open("./data/_CL_training.csv") as f:
    crisis = []
    for line in f:
        a = [x.strip() for x in line.split('\t')]
        if re.search(fire, a[4]):
            fire_c += 1
        if a[3] == "Related and informative" or a[3] == "Related - but not informative":
            a[3] = "Relevant"
        else:
            a[3] = "Not Relevant"
        crisis.append(a[3] + "\t" + a[4])
print fire_c

fire_c = 0
#print crisis[16]

with open("./data/Ryan/10KLabeledTweets_formatted.txt") as f:
    ryan = []
    for line in f:
        a = [x.strip() for x in line.split('\t')]
        if re.search(fire, a[4]):
            fire_c += 1
        ryan.append(a[3] + "\t" + a[4])
print fire_c
combine_data = crisis + ryan
print len(combine_data)



flood_c = 0
fire_c = 0
earth_c = 0

for i in combine_data:
    a = [x.strip() for x in i.split('\t')]
    if re.search(flood, a[1]):
        flood_c += 1

    if re.search(fire, a[1]):
        fire_c += 1

    if re.search(earthquake, a[1]):
        earth_c += 1

print flood_c, fire_c, earth_c

with open("./data/Ryan/10KLabeledTweets_formatted.txt") as f:
    ryan = []
    for line in f:
        a = [x.strip() for x in line.split('\t')]
        if re.search(fire, a[4]):
            fire_c += 1
        ryan.append(a[3] + "\t" + a[4])
'''



disaster_type = ["flood", "earthquake", "fire", "fire_flood"]
for i in disaster_type:
    nr = 0
    r = 0
    output = "./data/disasters/classify/" + i + '.csv'
    with open(output, "wb") as f2:
        for file in glob.glob("./data/disasters/" + i + '/*.csv'):
            with open(file) as f:
                for line in f:
                    a = [x.strip() for x in line.split(',')]
                    if a[4] == "Related and informative" or a[4] == "Related - but not informative":
                        a[4] = "Relevant"
                        r += 1
                    else:
                        a[4] = "Not Relevant"
                        nr += 1
                    f2.write(a[4] + "," + a[1] + "\n")

        print "Relevant: ", r
        print "nr: ", nr

        f_r = 0
        f_nr = 0
        e_r = 0
        e_nr = 0
        fir_r = 0
        fir_nr = 0
        with open("./data/Ryan/10KLabeledTweets_formatted.txt") as f:
            ryan = []
            for line in f:
                a = [x.strip() for x in line.split('\t')]
                if i == "flood":
                    if re.search(flood, a[4]):
                        if a[3] == "Relevant":
                            f_r += 1
                        elif a[3] == "Not Relevant":
                            f_nr += 1
                        f2.write(a[3] + "," + a[4] + "\n")
                elif i == "earthquake":
                    if re.search(earthquake, a[4]):
                        if a[3] == "Relevant":
                            e_r += 1
                        elif a[3] == "Not Relevant":
                            e_nr += 1
                        f2.write(a[3] + "," + a[4] + "\n")
                elif i == "fire":
                    if re.search(fire, a[4]):
                        if a[3] == "Relevant":
                            fir_r += 1
                        elif a[3] == "Not Relevant":
                            fir_nr += 1
                        f2.write(a[3] + "," + a[4] + "\n")
                elif i == "fire_flood":
                    if re.search(fire_flood, a[4]):
                        f2.write(a[3] + "," + a[4] + "\n")
    print "fr: ", f_r
    print "fnr: ", f_nr
    print "er: ", e_r
    print "enr: ", e_nr
    print "firr: ", fir_r
    print "firnr: ", fir_nr





