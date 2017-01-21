import os
import csv
import glob
import operator
import re

# with open("", 'rU') as f:
#    rd = csv.reader(f, delimiter=",")
# arr = [11,12,13]


disaster_array = ["napa_earthquake", "michigan_storm", "california_fire", "washington_mudslide", "iowa_stf", "iowa_storm", "jersey_storm",
                  "oklahoma_storm", "iowa_stf_2", "vermont_storm", "virginia_storm", "texas_storm", "washington_storm",
                  "washington_wildfire", "newyork_storm"]
state_code = [6, 26, 6, 53, 19, 19, 34, 40, 19, 50, 54, 48, 53, 53, 36]

hash_1 = [r"""napa earthqauke""",
          r"""storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding | detroitflood""",
          r"""fire | wildfire | wild fire | californiafire | burning""",
          r"""mudslide | slide | wild fire | fire | wildfire | earthfall | avalanche | landslide | mud""",
          r"""storm | windstorm | tempest | high wind | strong wind | tornado | cyclone | twister | typhoon | whirlwind | hurricane | flood | high water | flooding | wind | breeze""",
          r"""storm | windstorm | tempest | high wind | strong wind | tornado | cyclone | twister | typhoon | whirlwind | hurricane | flood | high water | flooding""",
          r"""storm | windstorm | tempest | high wind | strong wind""",
          r"""storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding""",
          r"""storm | windstorm | tempest | high wind | strong wind | tornado | cyclone | twister | typhoon | whirlwind | hurricane | flood | high water | flooding | wind | breeze""",
          r"""storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding""",
          r"""thunderstorm | earthfall | avalanche | mud | landslide | mudslide | storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding""",
          r"""storm | windstorm | tempest | high wind | strong wind | tornado | cyclone | twister | typhoon | whirlwind | hurricane | flood | high water | flooding | wind | breeze""",
          r"""wind | breeze | storm | windstorm""",  # wash storm
          r"""fire | burning | wildfire""",  # wash wildfire
          r"""storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding | snow | snowstorm | storm | blizzard"""]  # new york

all_flood_keywords = "mudslide | landslide | windstorm | storm | high wind | tornado | hurricane | thunderstorm | flood | typhoon | strong wind | high water | flooding | snowstorm | rain"  # keywords related to flood-related disaster

all_fire_keywords = "wildfire | wild fire | ablaze"  # keywords related to wildfire-related disaster

all_earthquake_keywords = "earthquake | aftershock | aftershocks | foreshock | eathquake | eartquake | earthquakes | quake | bigearthquake | earrhquake | majorearthquake | postearthquake | earthquakedamage | eathquakedamage | earthquakedamage | 3amearthquake | postearthquakeinspections | myfirstquake | myfirstearthquake | my1stquake | earthquakebelt | earthquakesucks | earthquaketoday | hateearthquakes | pissoffearthquake | fuckyouearthquake | nomoreearthquakes | EarthquakeAt3am | thatwasafuckinghugeearthquake | noearthquakehere | noearthquakes | ItWasAnEarthquake | fearoftheearthquake | terroirquake | earthquakesfiresfloodsetc | postearthquakepost | earthquakepreparedness | survivedtheearthquake | earthquakereadiness | earthquakekit | earthquakeprobs | earthquakeproblems | haterofearthquakes | earthquakesurviving | firstquakeinnewhouse | earthquakesurvivor | quakenoob | didntfeelanyearthquake | earthequakemode | isurvivedanearthquake | harvestearthquake | earthquakessuck | ihateearthquakes"  # keywords related to earthquake-related disaster


all_flood_keywords =r"\bmudslide\b|\blandslide\b|\bwindstorm\b|\bstorm\b|\bhigh wind\b|\btornado\b|\bhurricane\b|\bthunderstorm\b|\bflood\b|\btyphoon\b|\bstrong wind\b|\bhigh water\b|\bflooding\b|\bsnowstorm\b|\brain\b"

all_fire_keywords=r"\bwildfire\b|\bwild fire\b|\bablaze\b"

all_earthquake_keywords=r"\bearthquake\b|\baftershock\b|\baftershocks\b|\bforeshock\b|\beathquake\b|\beartquake\b|\bearthquakes\b|\bquake\b|\bbigearthquake\b|\bearrhquake\b|\bmajorearthquake\b|\bpostearthquake\b|\bearthquakedamage\b|\beathquakedamage\b|\bearthquakedamage\b|\b3amearthquake\b|\bpostearthquakeinspections\b|\bmyfirstquake\b|\bmyfirstearthquake\b|\bmy1stquake\b|\bearthquakebelt\b|\bearthquakesucks\b|\bearthquaketoday\b|\bhateearthquakes\b|\bpissoffearthquake\b|\bfuckyouearthquake\b|\bnomoreearthquakes\b|\bEarthquakeAt3am\b|\bthatwasafuckinghugeearthquake\b|\bnoearthquakehere\b|\bnoearthquakes\b|\bItWasAnEarthquake\b|\bfearoftheearthquake\b|\bterroirquake\b|\bearthquakesfiresfloodsetc\b|\bpostearthquakepost\b|\bearthquakepreparedness\b|\bsurvivedtheearthquake\b|\bearthquakereadiness\b|\bearthquakekit\b|\bearthquakeprobs\b|\bearthquakeproblems\b|\bhaterofearthquakes\b|\bearthquakesurviving\b|\bfirstquakeinnewhouse\b|\bearthquakesurvivor\b|\bquakenoob\b|\bdidntfeelanyearthquake\b|\bearthequakemode\b|\bisurvivedanearthquake\b|\bharvestearthquake\b|\bearthquakessuck\b|\bihateearthquakes\b"


# INPUT_FOLDER = "./data/washington_wildfire/hash"
for ij in xrange(len(disaster_array)):
    # if ij == 6 or ij == 8 or ij == 9 or ij == 12:   # skip some disasters due to not having enough data
    #     continue

    #

    if ij != 0:
        l = {}
        r = re.compile(
            hash_1[ij],
            flags=re.I | re.X)

        for file in glob.glob("./data/disasters/" + disaster_array[ij] + "/hash" + '*/*.txt'):
            # print file
            filename = re.findall('[^\\\\/]+', file)[-1]

            idfilepath = str(filename)

            if int(idfilepath[11:13]) == state_code[ij]:
                # print idfilepath

                with open("./data/disasters/" + disaster_array[ij] + "/hash" + "/" + idfilepath, 'rU') as f:
                    rd = csv.reader(f, delimiter="\t")
                    # print len(rd)

                    for i in rd:
                        if i[0] in l:
                            l[i[0]] += int(i[1])
                        else:
                            l[i[0]] = int(i[1])
                            # print len(l)

        hash_2 = []
        # print l

        for i in l:
            if re.search(r, str(i)):
                hash_2.append(i)
        print "original hash: " ,len(hash_2)
        # print (hash_2)

        s = ''
        for i in hash_2:
            s += i + " | "

        s = s[:-3]
        # s += " | dff"
        s += ''
        # print s

    # disaster_array = [
    #     "michigan_storm",
    #     "california_fire",
    #     "washington_mudslide",
    #     "iowa_stf",
    #     "iowa_storm",
    #     "jersey_storm",
    #     "oklahoma_storm",
    #     "iowa_stf_2",
    #     "vermont_storm",
    #     "virginia_storm",
    #     "texas_storm",
    #     "washington_storm",
    #     "washington_wildfire",
    #     "newyork_storm"
    # ]



    manually_verified_hashtags = [


        all_earthquake_keywords + r" |\bearthquake\b|\baftershock\b|\baftershocks\b|\bforeshock\b|\beathquake\b|\beartquake\b|\bearthquakes\b|\bquake\b|\bbigearthquake\b|\bbayquake\b|\bearrhquake\b|\bmajorearthquake\b|\bpostearthquake\b|\bearthquakedamage\b|\beathquakedamage\b|\bearthquakedamage2014\b|\b3amearthquake\b|\bearthquake2014\b|\bearthquake14\b|\bpostearthquakeinspections\b|\bcaearthquake\b|\bcaliforniaearthquake\b|\bcaliforniaearthquakes\b|\bCAearthquake\b|\bCAearthquakes\b|\bearthquakeCA\b|\bnorcalearthquake\b|\bsfoearthquake\b|\bbayareaearthquake\b|\bnorcaquake\b|\bnapaquake\b|\bnapaquakes\b|\bnapaearthquake\b|\bsouthnapaquake\b|\bnapashake\b|\bearthquakeinnapa\b|\bsouthnapaearthquake\b|\beartquakenapa\b|\bsonomaquake\b|\bsouthnapearthquake\b|\bearthquakenapa\b|\bnapaquake14\b|\bnapaquake2014\b|\bwestnapafault\b|\bearthquakeruinednapaplans\b|\bnapastrong\b|\bprayfornapa\b|\brebuildnapa\b|\bstaysafenapa\b|\bstaystrongnapa\b|\brecovernapa\b|\bNapaEarthquake6\b|\bSanFranciscoearthquake\b|\bsfearthquake\b|\bbayareaquake\b|\bsfquake\b|\bearthquakesf\b|\bearthquakesanfrancisco\b|\bearthquakessf\b|\bsfeathquake\b|\bearthquakesf2014\b|\bearthquakebayarea\b|\bsanfranquake2014\b|\bamericancanyonquake\b|\bamericancanyonearthquake\b|\bearthquakeamericancanyon\b|\bearthquakeamericancanyon\b|\bearthquakeinamericancanyon\b|\bprayforamericancanyon\b|\bmyfirstquake\b|\bmyfirstearthquake\b|\bmy1stquake\b|\bearthquakebelt\b|\bearthquakesucks\b|\bearthquaketoday\b|\bhateearthquakes\b|\bpissoffearthquake\b|\bfuckyouearthquake\b|\bnomoreearthquakes\b|\bEarthquakeAt3am\b|\bthatwasafuckinghugeearthquake\b|\bnoearthquakehere\b|\bnoearthquakes\b|\bItWasAnEarthquake\b|\bfearoftheearthquake\b|\bterroirquake\b|\bearthquakesfiresfloodsetc\b|\bcaloforniaearthquake\b|\bpostearthquakepost\b|\bearthquakepreparedness\b|\bsurvivedtheearthquake\b|\bearthquakereadiness\b|\bearthquakekit\b|\bearthquakeprobs\b|\bearthquakeproblems\b|\bhaterofearthquakes\b|\bearthquakesurviving\b|\bfirstquakeinnewhouse\b|\bearthquakesurvivor\b|\bAugust24EarthquakeSurvivor\b|\bsfearthquakewelcome\b|\bquakenoob\b|\bdidntfeelanyearthquake\b|\bearthequakemode\b|\bisurvivedanearthquake\b|\bharvestearthquake\b|\bearthquakessuck\b|\bihateearthquakes\b",

        all_flood_keywords + r" |\bfloodageddon\b|\bstupidfloods\b|\bfloodmageddon\b|\bthegreatflood\b|\bflooding\b|\bFloodsAren\b|\bfloodzilla2014\b|\bflood\b|\bnonstopstorms\b|\bmajorflooding\b|\bfloodssuck\b|\bDetroitflood\b|\bzomgfloods\b|\bbasementflood\b|\bitsstormingthough\b|\bfloodingintaylor\b|\bmichiganflood2k14\b|\bIntoTheStorm\b|\bFloodDay\b|\bflooded\b|\bFloodageddon\b|\bafterthestorm\b|\bDetroitFlood2014\b|\bfloodedbasement\b|\bdearbornflood\b|\bfloodingindetroit\b|\bNoFloodZone\b|\bFlooded\b|\bStupidFlood\b|\bFloodedinDetroit\b|\bschoolsflooded\b|\bdetroitflood2014\b|\bfloods\b|\bMIFlood\b|\btheflood\b|\bdetroitfloods\b|\bLocal4stormpicks\b|\bStormvsEdgerton\b|\bTheFlood\b|\bstorm\b|\bbasementisflooded\b|\bfloodedroads\b|\bFloodsEverywhere\b|\bfloodmagedon\b|\bfloodingindearborn\b|\bthunderstorm\b|\bfloodrecovery\b|\bdetroitisflooded\b|\bFlood\b|\bgreatfloodof2014\b|\bbeastisflooded\b|\bmetrodetroitflooding\b|\bFlooding\b|\bstupidflood\b|\bonlyroutenotflooded\b|\bFLOODZONE\b|\bfloodsfordays\b|\baramfloodlive\b|\bfloodymess\b|\bflood2014\b|\bsummerstorm\b|\bFloodgate\b|\bdetroitflooding\b|\btaylorflood\b|\bfloodedout\b|\bthunderstorms\b|\bmiflood\b|\bFloodingProblems\b|\bthegreatflood2k14\b|\bFlood2014\b|\bfloodpocalypse2014\b|\bDetroitFloodOf2014\b|\bfloodseverywhere\b|\bGreatFlood\b|\bDetroitFloods\b|\bflashflood\b|\bdetroitFlood\b|\bcelebritystorms\b|\bFloodWarnings\b|\bDetroitFlood\b|\bdetroitflood\b|\bnofloods\b|\bmidweststorm\b|\blivefromtheflood2014\b|\bfloodingproblems\b|\bFloodpocolypse\b|\bstorms\b",

        all_fire_keywords + r" |\bcafire\b|\bStreetsOnFire\b|\bcaliforniafire\b|\bcalfires\b|\bwillfire540\b|\bfirefight\b|\bFirecrackersElderts\b|\bwegotthatfire\b|\bhabanerohellfire\b|\bLakeCountyFires\b|\bTassajaraFire\b|\bsummitfire\b|\bKesterFire\b|\b1yearsincefireproof\b|\boxnardfire\b|\bcalfire\b|\bnorcalonfire2015\b|\bFireAndTheFlood\b|\bFireHotMami\b|\bwoodburninggrill\b|\bfireescape\b|\bFirefighters\b|\bTenayaFire\b|\bbuffalofiredepartment\b|\bfireengine\b|\b1YearSinceFireproof\b|\baliottasviafirenze\b|\bFireTrucks\b|\bfiremen\b|\blegsbeonfire\b|\bvalleyfire\b|\bwestcovinafiredepartment\b|\bcawildfirerelief\b|\bfirehazard\b|\bfirefire\b|\bArcadeFire\b|\bFiremen\b|\bsunnyvalefire\b|\blacountyfire\b|\bwoodburning\b|\bwoodfire\b|\bputoutthefires\b|\bcarfire\b|\bthefirewentwild\b|\bFullertonFire\b|\bfirefighters\b|\bbrushfire\b|\bHouseOnFire\b|\bfirehouse\b|\bSanJoseFire\b|\bCAFires\b|\barcadefire\b|\bCampfire\b|\blaurelesfire\b|\bRoughfire\b|\bFireTruck\b|\bjunctionfire\b|\bLaurelesFire\b|\bkingscountyfiredepartment|\bValleyfire\b|\bfirefightercostume\b|\bWeGotThatFire\b|\bsundancefire\b|\bfirethecannons\b|\bfirewood\b|\bfullertonisonfire\b|\bRisnerFire\b|\bDonationsForTheFireVictims\b|\bwildfire\b|\bhummerfire\b|\blakecountyfire\b|\blimofire\b|\bthefirewatchersdaughter\b|\bcobbfire\b|\bfiresuppression\b|\bthearcadefire\b|\byosemitefire\b|\broughfire2015\b|\bLaHabraFire\b|\bthesmelloffirewood\b|\bEarthWindandFire\b|\bfiredancing\b|\bRockAfireExplosion\b|\bventuracountyfiredepartment\b|\bLAOnFire\b|\barcadefireinmyears\b|\bPachecoFire\b|\btassajarafire\b|\bfirestone805\b|\bbuttefire\b|\bfireshurtredcrosshelps\b|\bfirefighterbrotherhood\b|\bValleyFire\b|\bfirefighting\b|\bstreetsonfire|\broughfire\b|\bbreathoffire\b|\bfireman\b|\bThankYouFirefighters\b|\bonfire2015\b|\bliveyourfiretv\b|\bfiredancers\b|\bglazefire\b|\bWildfireSmoke\b|\bfirefighter\b|\bmoralesfire\b|\bvalleyFire\b|\bcawildfires\b|\bpitfirewestlake\b|\bWhenTheresAFire\b|\blosangelesfiredepartment\b|\bFuckinFire\b|\bfiretruck\b|\bfireinthesky\b|\bquadsonfire\b|\bButteFire\b|\bwildfiresmoke\b|\bforestfire\b|\bfirecontrol\b|\bfiremenarehot\b|\bFiremenAreHot\b|\bButteCountyFire\b|\blakevillefire\b|\bbutteandvallyfires\b|\bLakeFire\b|\bRoughFire\b|\bitlooksliketheskyisonfire\b|\bButteMountainFire\b|\bOldFire\b|\bbuttefire2015\b|\bCalFire\b|\bCaliforniaFireSeason\b|\bfiredepartment\b|\bTenyafire\b|\bValleyFires\b|\bwildfires\b|\bfuturefirefighter\b|\brimfire01\b|\bHumboldtFireDepartment\b|\byosemitefires\b|\bheritagefire\b|\bCalfire\b|\bcaliforniaisburning\b|\bHellfire\b|\bskyonfire\b|\bOnFireNorCal\b|\bCawilfires\b|\bcaliforniafires\b|\bcaliforniaisonfire\b",

        all_fire_keywords + " | " + all_flood_keywords + r" |\bpreventwildfires\b|\bWAWILDFIRE\b|\bwildfires\b|\bWAWildfires\b|\bmorefires\b|\bWAWildFire\b|\bwildfiresunrise\b|\bfirehelmets\b|\bwafire\b|\bbaldyfire\b|\bWAWildFires\b|\bfireseason2015\b|\bwashingtonfires2015\b|\bTacomaFire\b|\bwashingtononfire\b|\bWildfire\b|\bchelanfires\b|\bforestfire\b|\bWAwildfire\b|\bWashingtonOnFire\b|\bgrizzlybearfire\b|\bfirehaze\b|\bwawildfire\b|\bnomorefiresplease\b|\bforrestfire\b|\bFireSmog\b|\bpnwfires\b|\bwashingtonStateFires\b|\bfirefighters\b|\bWaWILDFIRE\b|\bwashingtonfires\b|\burbancampfire\b|\bworldonfire\b|\bWildfires\b|\bNotSureIfChelanFireCanReachMe\b|\bThankYouFirefighters\b|\bwildfirefundraiser\b|\bchelancomplexfire\b|\bfiremen\b|\bfirepocalypse2k15\b|\bprayforFirefighters\b|\bforestfires\b|\bthankufirefighters\b|\bfirstcreekfire\b|\bWAWildfireRelief\b|\bwildfire\b|\bokanaganfire\b|\bfirefighter\b|\bfireseason\b|\bprayersforfirefighters\b|\bthewestcoastisonfire\b|\bwildfirefilter\b|\bchelanfire\b|\bwildfiresunset\b|\bthankafirefighter\b|\bwawildfires\b|\bWashingtonFires\b|\bTacomaFireDepartment\b|\bWAwildfires\b|\bfirefighting\b|\brennerfire\b|\bwafires\b|\bWAWildfire\b|\bthankyoufirefighters\b",

        all_flood_keywords + r" |\bfaketornado\b|\bstrobelightstorm\b|\bNextStormChaser\b|\bfloodprobs\b|\bstormpanos\b|\bTornadoOutbreak\b|\bHateStorms\b|\bstormyweather\b|\bFlashFloodAlarm\b|\bpleasedontstorm\b|\bFloodWaters\b|\bprayingfortornado\b|\bTwisterChasers\b|\bthunderstorm\b|\bFloodStage\b|\bonlyinstormlake\b|\baccidentalstormchasers\b|\bstormwatching\b|\bTornadoBaseball\b|\bFlooding\b|\bdamnstorm\b|\bstormy\b|\bstorms\b|\bStorminSiouxCity\b|\bStorminMcNorman\b|\bTornadoWarning\b|\bstormdamage\b|\bIaflood\b|\bStormChasers\b|\blovestorms\b|\bstorm\b|\bwindy\b|\bNebraskaTornadoes\b|\bILoveStorms\b|\bflooded\b|\biaflood\b|\bstormchasers\b|\bStormCrazy\b|\bRockValleyflood\b|\bStormChaser\b|\bstrongwinds\b|\bStupidThunderstorm\b|\bStormy\b|\bStorms\b|\bPilgertornado\b|\btornadobelt\b|\byaywind\b|\bFlood\b|\bstormupdates\b|\bTornado\b|\bdualtornadoes\b|\bastormiscoming\b|\bdustinthewind\b|\bIowaflooding\b|\bfloodingeverywhere\b|\bnightstorms\b|\bFloodedStreets\b|\bstormseason\b|\btornadosafety\b|\bHurricaneKony2014\b|\bfloods\b|\blovetornadoes\b|\banotherstorm\b|\bhumidstormcells\b|\bstupidtornadoes\b|\bteamwind\b|\btornadosamiright\b|\bStormOver\b|\bHalestorm\b|\bStormcon\b|\bstormABrewing\b|\bflashflood\b|\bfloodof2014\b|\bHaveyflood2014\b|\bmissouririverflood\b|\bfreakinstorm\b|\btornadoes\b|\bTornadoCantStopMe\b|\btornadowatchsucks\b|\bthunderstormsongs\b|\bweatherthestorm\b|\bCycloneWarning\b|\bIHateStorms\b|\bstormday2014\b|\bstormchaser\b|\btornadowatch\b|\bihatestorms\b|\bFuckTheStorm\b|\bwindswept\b|\bflood2k14\b|\bSoulStorm\b|\bFlood2014\b|\bTwoTornadoes\b|\bstrongstorms\b|\bStorming\b|\bnostorm\b|\bhatetornados\b|\bflooding\b|\bwindfactor\b|\bflood\b|\bstormkyaking\b|\bthewindbegantoswitch\b|\bThunderstorm\b|\bsummerstorms\b|\btornadoesgotnothin\b|\bdamnstorms\b|\bsocialmediaisflooded\b|\bdramaticstormpic\b|\bwindevent\b|\bhalestorm\b|\bwindinmyhair\b|\bfeelthebreeze\b|\bwinding\b|\bhatestorms\b|\bTornados\b|\bflood2014\b|\bthunderstorms\b|\btornadowarning\b|\bflashfloods\b|\bWindsor\b|\btornado\b|\btwintornados\b|\bStormWatchin\b",

        all_flood_keywords + r" |\btornadowarning\b|\bTornadoWarning\b|\bstorm\b|\btornadowatch\b|\biwantstorms\b|\bflood\b|\bstormynight\b|\btornadoes\b|\bstormchasers\b|\bstormsoverbachelorette\b|\brainstorms\b|\bthunderstorm\b|\bsolarstorm\b",

        all_flood_keywords + r" |\bstormyweather\b|\bthunderstorm\b|\bstorms\b|\bcalmafterthestorm\b|\bstorm\b|\bafterthestorm\b|\bcalmbeforethestorm\b|\bstormchaser\b|\bstorm2015\b|\binbeforethestorm\b|\bTheStorm\b|\bThunderstorm\b|\bstormsabrewin\b|\bdarkandstormy\b|\bStorm\b|\bsummerstorm\b|\bthunderstorms\b|\bthecalmbeforethestorm\b",

        all_flood_keywords,

        all_flood_keywords + r" |\bfloodageddon\b|\btornadoweather\b|\bHailStorm\b|\bStormsAreFun\b|\bflooded\b|\bfloodedbasement\b|\bstormchasemedia\b|\bWind\b|\bstormysummer\b|\bHelloFloods\b|\bstupidstorm\b|\bseverestorms\b|\bTonadoWarningsOnTornadoWarnings\b|\bthunderstorm\b|\bstormchasin\b|\bopenyourwindows\b|\bThanksStorms\b|\bTornadoAlley\b|\bbravetheflood\b|\bstormcon\b|\bFlooding\b|\bstormy\b|\bstorms\b|\bStorms\b|\btornadoseason\b|\bstorm2k14\b|\bfloodprobs\b|\bfloodprobz\b|\bStormWatch\b|\bstormdamage\b|\btornadowarnings\b|\bflood14\b|\bStormChasers\b|\bJoCoflooding\b|\bwindy\b|\bhashtagtornadolifeyoloswag\b|\bstopflashfloodsinIowa\b|\bCRflood14\b|\bafterthestorm\b|\bfloodsafety\b|\bgoawaystorms\b|\bstormpics\b|\bDamnStorms\b|\b2014floods\b|\bsrryforthestormtweet\b|\bstorming\b|\bStormChaser\b|\bdownwindstruggle\b|\bfloodwatch\b|\bstorm\b|\bcrazystorm\b|\bAmesFlood14\b|\bLoveStorms\b|\bFlood\b|\bTornado\b|\bTORNADO\b|\bTornadoOrNah\b|\bfloodwatergalore\b|\bcalmbeforethestorm\b|\bseverethunderstorm\b|\biowastorms\b|\bfloodcity\b|\bHurricaneGoodbyeIowa\b|\bFloodsof2014\b|\bIowastorms\b|\bilovefallingasleeptostorms\b|\bflashflood\b|\btornados\b|\bridingthestormout\b|\bfloodof2014\b|\bTyphoonNeoguri\b|\b2014flooding\b|\bstormpocalypse\b|\btornadoes\b|\bStormChasing\b|\bstormbycandlelight\b|\bFloodWaterFun\b|\bFloodOf14\b|\bfloodof14\b|\bstormchaser\b|\bstormchasing\b|\btornadowatch\b|\biowafloods\b|\bihatestorms\b|\bwindowsrattling\b|\bflooddanger\b|\bfuckstorms\b|\bthestormhaspassed\b|\bCalmAfterTheStorm\b|\bstormaggaden\b|\bStormchasers\b|\bflooding\b|\bflood\b|\bFlashFlood\b|\biowaflooding\b|\ballglasswindows\b|\bStorm\b|\bDarkandStormy\b|\bstormofthecentury\b|\bscaredofstorms\b|\bcoleswindell\b|\bhatestorms\b|\b2014Floods\b|\bQCFlood2014\b|\bflood2014\b|\bsummerstorm\b|\bthunderstorms\b|\bfloodedriver\b|\btornadowarning\b|\bstupidstormreports\b|\bIowaStorms2014\b|\btornado\b|\bJoCoFlooding\b|\bwindyaf\b|\bThunderstorms\b|\bhighwater\b",

        all_flood_keywords,

        all_flood_keywords,

        all_flood_keywords + r" |\bTexasFlood\b|\bStormcon\b|\bstrongsunsetandstorm\b|\bdfwflooding\b|\bHurricanePatriciaonablunt\b|\bsanantonioflood2015\b|\btexasflood\b|\bsummerstorms\b|\bpraisegodthroughthestorm\b|\bHighWaters\b|\bthunderstorm\b|\bflooded\b|\bTornadoWarning\b|\bFlooding\b|\bstormy\b|\bstorms\b|\bhurricaneproblems\b|\bfloodmageddon2015\b|\bHurricaneParty\b|\brainstorm\b|\baustinfloods\b|\btornadocActivity\b|\bhurricane\b|\bfloodingfail\b|\bstormdelays\b|\bhurricanewedding\b|\bfloodwaters\b|\bstorm\b|\bhurricaneseason2015\b|\bwindy\b|\bfloodwatching\b|\bTornadoWhile\b|\bTexasFloods\b|\bhalloweenfloods\b|\btropicalstormpatricia2015\b|\b2015flood\b|\belectricalstorm\b|\bflashfloodwarning\b|\bcentexfloods\b|\batxfloods\b|\bhurricanepatricia\b|\bWindingRoadRacing\b|\bTornadoWatch\b|\bstorming\b|\bglorywind\b|\bTORNADO\b|\bHurricanePatricia\b|\bFloodedEveryWhere\b|\bonioncreekflood\b|\blovefloods\b|\bStormfood\b|\bTrinityFlooded\b|\bstormfood\b|\bstormyweather\b|\bWickedStorms\b|\bHurricanePatriciaRain\b|\bfloods\b|\bFlooded\b|\bfloodwatchandchill\b|\bitswindy\b|\bsmtxflood\b|\bseriousstorm\b|\bfloodlife\b|\bsanmarcosflood\b|\bhalloweenflood2015\b|\bflashflood\b|\bfireandtheflood\b|\bbrushycreekfloods\b|\bStormOfTheCentury\b|\bsanmarcosflood2k15\b|\bhightowerhurricanes\b|\bHurricaneSeason\b|\bHoustonFlood\b|\bFLOOD\b|\bblancoriverflood\b|\bthestormafterthestorm\b|\bflashfloods\b|\batxflood2015\b|\bfloodpuns\b|\bstormiscoming\b|\bStormComing\b|\bStormageddon\b|\bcalmbeforethestorm\b|\bstormsthatgoboom\b|\bFlashFlood\b|\bhurricanepatricia2015\b|\bflooding\b|\btornado\b|\bflood\b|\bfloodindownintexas\b|\bUnionCreekFlood\b|\bOutRunningTheHurricane\b|\bTexasflood\b|\bfloodpacolypse2015\b|\btexasstorms\b|\bviewfrommywindow\b|\bHoustonflood\b|\bmonsoonflooding\b|\bStorm\b|\bthxstorm\b|\bwindydays\b|\bHurricaneHeat\b|\bhalloweenfloods2015\b|\bhoustonflood\b|\bFlashFloods\b|\bfloodwarning\b|\btxflood\b|\bHurricane\b|\bhurricaneweather\b|\bstrongeststormever\b|\bitsflooding\b|\bitsJUSTatropicalstorm\b|\bhurricanes\b|\bthunderstorms\b|\btornadowarning\b|\bstormcoming\b|\bflashfloodwarnings\b|\bHoustonFloodWatch\b|\bATXFlooding\b|\bThunderstorms\b|\bfloodingintexas\b|\bwhathurricane\b|\bFloodOfHalloweenEve\b|\bThanksStorm\b|\bTornado\b",

        all_flood_keywords + r" |\bpwnwstorm\b|\bitssortawindy\b|\bthestorm\b|\bduststorm\b|\bwawind\b|\bstorme\b|\bwindblowsmyfaceoff\b|\bcalmafterthestorm\b|\bwindschief\b|\bstorm\b|\bwindy\b|\bbringonthestorm\b|\bmorningstorm\b|\bwindyinseattle\b|\bwindfarm\b|\bwindenergy\b|\bwawindstorm\b|\bSummerstormproblems\b|\bwindrainorshine\b|\bcalmbeforethestorm\b|\bstormyweather\b|\bquietstorm\b|\bunwind\b|\bSeattleStormageddon\b|\bstorm2015\b|\bdirtstorm\b|\bwindstorm\b|\bThunderstorm\b|\bholywindbatman\b|\bnameourstorms\b|\bwindydays\b|\bstormynights\b|\bstormwatch\b",

        all_fire_keywords,

        all_flood_keywords + r" |\bstormaintstoppingus\b|\bStormcon\b|\bLakeEffectSnow\b|\bSnowpocalypse\b|\bfirstdayofsnow\b|\bnosnowdaysNovember\b|\bilikeSnow\b|\bbringonthesnow\b|\bSnowLover\b|\bSnowmedoggy\b|\bLetItSnow\b|\bsnowstop\b|\bSNOWBOWL\b|\bSnowband\b|\bnosnow\b|\bBuffaloSnow\b|\bdoublesnowday\b|\bwinterstorm\b|\blakeeffectsnowwarning\b|\bsnowpacalypse2k14part3\b|\bSnowEmergency\b|\bBuffalosnow\b|\bSNOWevember\b|\bBlizzardOf2014\b|\bsnowvembertoremrmber\b|\bletitsnowletitsnowletitsnow\b|\biwantasnowday\b|\bTsnownami\b|\bFirestorm\b|\bSnowmagedon\b|\bSnowAngels\b|\bAtLeastWeHaveNoSnow\b|\bBuffaSNOW\b|\bBuffaloBlizzard2014\b|\bnovembersnowday2k14\b|\bstupidstorm\b|\bnovemberstorm2k14\b|\bTHUNDERSNOW\b|\bshitstorm\b|\bgiantsnowflakes\b|\bsnowpocalypse2k14\b|\bFIRSTSNOW\b|\bSnowcopalypse\b|\bbuffasnow\b|\b3rdSnowDay\b|\blakesnoweffect\b|\bcnystorm\b|\bSnowStormActivties\b|\bsnowday4\b|\bsnowday3\b|\bsnowday1\b|\bsnowdays\b|\bstormywednesday\b|\bBuffaloblizzard2014\b|\bwtfsnow\b|\bsnowocalypse2k14\b|\bsnowcantcatchme\b|\bsnowtime\b|\bgoawaysnow\b|\bsnowpleasestayinsouthtowns\b|\bThanksgivingSnow\b|\bfloodgates\b|\bsnowmageddon\b|\bWGEZSNOW\b|\bBNstormready\b|\bsnowshoecatsofinstagram\b|\bBuffalsnow\b|\bfuckthesnow\b|\bBuffalostorm\b|\bsnowvemberbender\b|\bwinterstormGodzilla\b|\bNYCsnow\b|\bkhoopsnow\b|\bprayforasnowday\b|\bSydneyStorm\b|\bstorm\b|\bturnupinsnow\b|\bPerfectStorm\b|\bsnowstormofthecentury\b|\bwheresthesnow\b|\bsnowshmo\b|\bsnowdaysfordays\b|\bHappySnowDayNYC\b|\bsnowremovalproblems\b|\bhalfblizzard\b|\bsnowinNewYork\b|\bLetItGoSnow\b|\blakeeffectsnowstorm\b|\bSnowBeltprobs\b|\bSnowFallo\b|\bIWantSnow\b|\bverylittlesnownorth\b|\bSnownami\b|\bSNOWpocalypse\b|\bsnowneonta\b|\bsnowbound\b|\bknifestorm2014\b|\bstormcasualty\b|\bBuffaloNewYorkSnow\b|\bShovelThatSnow\b|\bSnowDay2014\b|\bstormkingmoments\b|\bsnownado\b|\bStormHowie\b|\bSnow\b|\bsnowdayfromwork\b|\bsnowday2014\b|\bsnowpocoplyse\b|\bsnowfordays\b|\bILoveSnow\b|\bwaposnow\b|\bsnowynights\b|\bTheSnowNews\b|\bsnowrun\b|\bsnoweater\b|\bsnowround2\b|\bPurfekStormGroup\b|\bWinterstorm\b|\bnomorefloodedengines\b|\b3INCHESOFSNOW\b|\bFirstSnow\b|\bsnowpocalypseBuffalo\b|\bSnowshoes\b|\bsnowthunder\b|\bThundersnow\b|\bsnowmakeseverythingfun\b|\btwosnowdaysinarow\b|\bclearingsnow\b|\bBuffaloblizzardbeers\b|\b4feetofsnow\b|\bBlizzard2014\b|\bsnowingoutside\b|\bsnowdayhappiness\b|\bSnowWhite\b|\btriplesnowday\b|\bSnowchat\b|\bsnowflakes\b|\bINTHEKNOWFORSNOW\b|\bHALESTORM\b|\bFlood\b|\bstupidsnow\b|\bitshellasnowing\b|\bsnowshoveler\b|\bblizzardballin\b|\bRidingOutTheStorm\b|\blovesnowdays\b|\bsnowdaydecisions\b|\bitsgonnasnowagain\b|\bsnowdaypart2\b|\bsnowdaypart3\b|\bbuffalostorm\b|\bWhyIsntThisSnow\b|\bbuffaSNOW\b|\bSOUTHTOWNBLIZZARD\b|\bwinterstormcato\b|\bSnowAlley\b|\bSnovemberStorm\b|\bNewYorkSnowDay\b|\bWGRZsnow\b|\bnomoresnow\b|\blakeeffectstorm\b|\bleavingbeforethesnowstorm\b|\bredstorm\b|\bcomeonsnow\b|\bSnowing\b|\bsnowmountain\b|\bItsSnowing\b|\bfunsleddinginrhesnow\b|\bquietstorm\b|\bSnowCoveredTDI\b|\bTheSnow\b|\bWinterStormKnife\b|\bsNOwINbuffalo\b|\bsnowshoeing\b|\bSnowThankYou\b|\bsnowpocalyps\b|\bsnow2014\b|\bONstorm\b|\bBlizzard\b|\bsnowmaggedon\b|\bfirstsnow\b|\bSNOWvember\b|\bSnowmageddonMyButt\b|\bFuckTheSnow\b|\bihatesnow\b|\bstormking\b|\bSnowvber\b|\bandyourBumAssSnow\b|\bsnowdaysshavery\b|\bseniorsskipsnowday\b|\blovesnow\b|\bnosnowyet\b|\bthingsyoudoonasnowday\b|\bsnowsucks\b|\bswallowedbysnow\b|\bhighwaters\b|\bbecauseSnow\b|\bSnowShovelWorkout\b|\bgoredstorm\b|\bStillSnowingHere\b|\bNovSnow2014\b|\bblizzardprobs\b|\bsnowflake\b|\bSnowday\b|\bhappysnowday\b|\bWallOfSnow\b|\bSnowdoginBuffalo\b|\bnomoresnowplease\b|\babc7snow\b|\bsnowdayfunday\b|\bDownofthesnow\b|\bsnowbreak\b|\bsnowlovers\b|\bQuietBeforeTheStorm\b|\bstormvember\b|\bnonamestorm\b|\bNoSnow\b|\bhaulingsnow\b|\bsmellslikesnow\b|\bdothesnowshovel\b|\btooearlyforsnowflakes\b|\bwhollysnowbatman\b|\bsickofsnow\b|\bstormiscoming\b|\bfamoussnowstorm\b|\bwedontneednofrickinsnow\b|\bFunOnTheSnow\b|\bmiraclesnow\b|\bitsjustsnow\b|\beyeonthestorm\b|\bupstateLakeeffectsnow\b|\bWinterStormCato\b|\bsnowdayround4\b|\bhidingfromthesnow\b|\bbuffalosnowmiracle\b|\bWhatBlizzard\b|\bpapersnowflakes\b|\btalliastorm\b|\bSuccessfulStudentsDontGetSnowDays\b|\bSnowbash2014\b|\bperfectstorm\b|\bLESSnow\b|\bwheresallthesnowiwaspromised\b|\bblizzard14\b|\bnewyorksnowstorm\b|\bWinterStorm\b|\bsnowmachines\b|\bsnowfallselfie\b|\bsnowpacalypse\b|\bSnowvembertoremember\b|\bnotreadyforsnow\b|\bSnowJoy\b|\bsnowmen\b|\bsnownedin\b|\bstormnecessity\b|\bHappySnowDays\b|\bsnowmagedon\b|\bSnowy\b|\bSnowSurvivalPlan\b|\bStupidSnow\b|\bSnowvember2014\b|\bblizzard\b|\bKNIFEstorm\b|\bsnowvembertoremember\b|\bsnowstorm2014\b|\b2SnowDays\b|\biactuallyhatesnow\b|\bsnowpocalypse\b|\bevenblizzards\b|\bsnowpocolypse\b|\bsnowshovel\b|\biblamethesnow\b|\bSNOWMAGGEDON\b|\bthecalmbeforethesnow\b|\bFirstSnowStormOf2014\b|\bWgrzsnow\b|\bsnowityourway\b|\bThanksgivingsnow\b|\bblizzardparty\b|\bsnowdayround3\b|\bBlizzard14\b|\bHighWinds\b|\bIHateSnow\b|\bBlizzardBoredom\b|\bstormdamage\b|\bNoSnowPLZ\b|\bsnowwheretoputit\b|\biheartsnow\b|\bturkeystorm\b|\brunninginsnow\b|\bihatesnowdays\b|\bgokissanIndiansassnow\b|\bsnowpacolypse2k14\b|\bsnowdog\b|\bSnowmobilerProblems\b|\bsnowedourwayintoprimetime\b|\bsnowhailrain\b|\bLetsGoSnowffalo\b|\bSnowvember\b|\bbuffaloblizzard\b|\bhopewedontgetsnowedin\b|\bsnowfie\b|\bwetsnowrainmix\b|\bhalestorm\b|\badultsnowday\b|\bsnowwhite\b|\bsnownami\b|\bsnowdayround2\b|\bSNOWVEMBER14\b|\bnotthankfulforsnow\b|\bbyebyesnow\b|\bRainSleetSnowDay\b|\bBuffaloStorm\b|\bthroughthestorm\b|\bSnowOnFOX\b|\bstormnames\b|\bWinterStormAdvisory\b|\bSnowvemberDrunkvember\b|\bsnowmageddon14\b|\bSnowmobiling\b|\bsabresfansnowday\b|\bastormisbrewing\b|\bIwantasnowday\b|\bSnowstormBuffalo\b|\bsnowdayalldayerrrrday\b|\bSnowfallOnTheWay\b|\bcalmbeforestorm\b|\bcanisiussnowdaypt2\b|\bsnowvemberbearit\b|\bwinterstorms\b|\bmyniggaknowsnowsoicanpostthis\b|\bfloodingProbs\b|\bBuffaloSnowday\b|\bstrugglesofblizzard2k14\b|\bNewYorkSnow\b|\bwishingitwasasnowday\b|\bPersonalSnowDay\b|\bnysnow\b|\bblacksnow\b|\bthanksgivingsnow\b|\bsnowmagedonwhat\b|\bPastorMikeSays\b|\brainsnow\b|\bsnowblowing\b|\bstilllovesnow\b|\bsouthbuffalosnowday\b|\bSnowForDays\b|\bfreesnowwhite\b|\babc7NYsnow\b|\bNotChristmasTimeUnlessItsSnowing\b|\bblizzardcravings\b|\bfloodwarning\b|\bsuckitwinterstormCato\b|\bsnowvemberstorm\b|\bsnowmobile\b|\bfuckyousnow\b|\bNovemberStorm2014\b|\bflooded\b|\bblizzardhacks\b|\bABC7NYSnow\b|\bFuckthesnow\b|\bSnowFall\b|\bSnowVember\b|\bSnowIsComing\b|\bsnowoutside\b|\bitssnowing\b|\bpjsnow\b|\bScavinoStormCenter\b|\bLakeEffectSnowStorm\b|\bsnowstormdelay\b|\bsnowbaby\b|\bDontSnortTheSnow\b|\bSnowDayStreak\b|\bfirstworldblizzardgamerproblems\b|\bsnowlightening\b|\bthankssnow\b|\bSnoWvember\b|\bprankwarstartsnow\b|\bTurnUpDelayedForSnow\b|\bOlihavingfuninthesnow\b|\bSnowIntoWater\b|\bSnowdayIII\b|\bsnowed\b|\bbuffalostorm2014\b|\bfrickyousnow\b|\bFirstsnow\b|\bwheresmysnow\b|\bBuffaloSnowstorm\b|\bsnowmobiling\b|\barticsnowbelt\b|\bWinterStormWatch\b|\bThunderSnow\b|\btwerkforjoessnowday\b|\bBuffaloSnowStorm2014\b|\bSnowPretty\b|\bsnowhaboob\b|\bBuffasnow\b|\bBringOnThatSnow\b|\bSuperstormSandy\b|\bStormSixPack\b|\btomuchsnow\b|\bsnowday\b|\bstormin\b|\bteamnosnow\b|\btsnownami2014\b|\bsnowflakeonfifth\b|\bsnowproblems\b|\bpurfekstorm\b|\bSnowFlake\b|\bHateTheSnow\b|\bsnowmygoodness\b|\bsnowvember2remember\b|\bitssnow\b|\bsnowwite\b|\bsnowfodays\b|\bIHATESNOW\b|\bneedasnowday\b|\bSnowbember\b|\bWGRZSnow\b|\basIf60InchesOfSnowIsntEnough\b|\bSNOWVEMBER\b|\bSaveStorm\b|\bsnowdaybordem\b|\bsnowsgone\b|\bsnowneverstoppedme\b|\bSnowflake\b|\bquietbeforethestorm\b|\bwhothefuckiscadistorm\b|\bBronxSnow\b|\bFirstStorm2014\b|\bSnowbound\b|\btoomuchsnow\b|\bLOOKATTHE4FEETOFSNOWINTHESTREET\b|\bsnowbuffalo\b|\bThruTheStorm\b|\bFunInTheSnow\b|\bSnowBelt\b|\bSnowedInThoughts\b|\bRainySnowyDay\b|\bSnovember2014Storm\b|\bsnowshoes\b|\bILikeSnowButShoveling\b|\b2014blizzard\b|\bItsTheSnowsFault\b|\bsnowytrees\b|\btwcnewssnow\b|\bsnowdonia\b|\bilovesnowdays\b|\b1stSnow\b|\bSnowAintNoJoke\b|\bBringOnTheStorm\b|\bBuffaloflood\b|\bsnowboundzombies\b|\bLakeEffectSnowSTORM\b|\bDarkandstormy\b|\bSnowvemberSucks\b|\bsnowstormhopping\b|\bblizzardconditions\b|\bsnowboots\b|\bWGRZSNOW\b|\bbuffaloflood\b|\bSnowStorm\b|\bSnowsgiving\b|\bbringmethesnow\b|\bItsSnowsHere\b|\bIPlowSnow\b|\bSnowDayNumber3\b|\bstillsnowing\b|\bsomuchforabigsnowstorm\b|\battackoftheiceandsnow\b|\bSnowEDin\b|\bsyracusesnow\b|\bholysnow\b|\bsnowpocalypse2014\b|\bpray4snow\b|\bSnowvemberSavesOurGrades\b|\bfloodwatch\b|\bGoHomeSnow\b|\bcrazystorm\b|\bubsnowday\b|\bFuckTheSnowDay\b|\bIWantASnowDay\b|\bsnowstorm\b|\bStormville\b|\bWarmSnow\b|\bdamnsnow\b|\bSnowCaps\b|\bsnowscomin\b|\bfirstsnowfun\b|\bsnowerrywhere\b|\bTheFallingSnow\b|\bblizzardof77\b|\bSnowvembver\b|\bTHUNDERSNOWFOOTBALL2014\b|\bsnowvember\b|\boffseasonstartsnow\b|\bStormKing\b|\bsnowsouttitsout\b|\bNovemberSnow\b|\bsnowtown\b|\bsnowinmymouth\b|\bSnowpocalypse2K14\b|\bwgrzsnow\b|\bBuffaloStorm14\b|\bWhoNeedsSnowBoots\b|\bsnowpacolypse\b|\bblizzardcomingsoon\b|\bSabresFanSnowDay\b|\bsnowridge\b|\bsnowslomo\b|\bSnowHappens\b|\bbuffalosnowchallege\b|\bcalmbeforethestorm\b|\bReportedSnowAlready\b|\byaysnow\b|\bsnowvemberprobs\b|\bsnowsessions\b|\bnovemberstorm\b|\bNovemberStorm\b|\bSnowdayTurnup\b|\bsnowdayplz\b|\bSnowChesterNy\b|\bsnownyc\b|\bRedStormFridays\b|\bYellowsnowhadtogo\b|\bsnowheart\b|\bLESnow\b|\bOurSnowMachine\b|\bnosnowfornyc\b|\bsnowscoming\b|\bdfsnow\b|\bstormkingartcenter\b|\bHalestorm\b|\bsnowdaytuesday\b|\bSnowBaby\b|\bSnowDays\b|\bSnowDay4\b|\bsnowedinandhungry\b|\bsnowbank\b|\bsnowband\b|\bNW2Wsnow\b|\bsnowblower\b|\bwhat_snow\b|\bstormpreparedness\b|\bhatesnow\b|\bweinablizzardman\b|\bhailstombetterthanwinterstorm\b|\bsnowember\b|\bicysnow\b|\b2snowdays\b|\bstormknife\b|\bstormprobs\b|\bFyahStorm\b|\bhavetheynamedthisstormyet\b|\bsomuchsnow\b|\bfloodinsurance\b|\blakeeffectsnow\b|\bsnowfall\b|\bsnowdayforMomma\b|\bbuffalosnow\b|\bCanisiusSnowDayPt2\b|\bCanisiusSnowDayPt3\b|\bbuffalosnowstorm\b|\blohudsnow\b|\bwinterstormKNIFE\b|\bSnowDay\b|\bsnowedin2014\b|\bbringsnowblowers\b|\bPraysForAlotOfSnow\b|\blotsofsnow\b|\bsnowbrush\b|\bletitsnow\b|\bneedmoresnow\b|\bwgrztvsnow\b|\bsnowbowl\b|\bgiantsnowflake\b|\bSnowToForehead\b|\bsnowmaking\b|\bidloveasnowstormlikethat\b|\bbirthdayweekendbeginsnow\b|\bwnysnow\b|\bblizzardmyass\b|\bhatingsnow\b|\bsnowpants\b|\bthankyousnow\b|\bsnowbowl2014\b|\bsnowpocalyspe2014\b|\bWhatWouldSnowDo\b|\bsnowremoval\b|\bstopthesnow2014\b|\bFirstSnowOfTheSeason\b|\bSnowBuffalo\b|\bSnowstorm\b|\bWinterStormWarning\b|\bsnowdogs\b|\bilovesnow\b|\bihatethesnow\b|\bsnow\b|\bclarencesnowday\b|\bwolsnowcamp\b|\bGetStormATwitter\b|\blovethesnow\b|\bLovinThoseConcentratedSnowStorms\b|\bTooMuchSnow\b|\btcnewssnow\b|\bSnowblowerElbow\b|\bsnowedinstruggles\b|\bBuffalOsnow\b|\banothersnowday\b|\bblizzard2014\b|\bknifestorm\b|\bsnowedinstruggle\b|\bSnowember\b|\bsnowing\b|\bhatethesnow\b|\bscaredofsnow\b|\bsnowdayproblems\b|\bbestsnowdayever\b|\bflooding\b|\bFuckSnow\b|\bsnowday2\b|\bbuffsnowday\b|\bNotSnowboardingWeather\b|\bBuffaloSnowedIn\b|\bFLOODWATCH\b|\bmrsnowmizer\b|\bitsnowed\b|\bBuffaloBlizzard\b|\bsnowdaythoughts\b|\bsnowblowerless\b|\bsnowtsunami\b|\bsnowstrong\b|\bFourDaySnowDay\b|\bStormKnife\b|\bsnowtine\b|\bilovethesnow\b|\bItstartsnow\b|\bsnowalldayeveryday\b|\bsnowbandproblems\b|\bSnowStorm14\b|\bSnowpocalypseproblems\b|\bpushingsnowdrinkinbeerwithconzi\b|\bfuckthissnow\b|\bblizzardworkout\b|\bTWCNewsSnow\b|\bsnowy\b|\bsnoww\b|\bfirstsnowoftheseason\b|\bwinterstormknife\b|\bsupersnowdog\b|\bthundersnow\b|\bhamburgblizzard11\b|\bfuckingsnow\b|\bStorm\b|\bFristSnow2014\b|\bitwasalsosnowing\b|\bsnowydusk\b|\bsnowny\b|\bfirstsnowfall\b|\bStorm2014\b|\boksnowpolice\b|\bSnowweeks\b|\bbuffalsnow\b|\beveryonessnowedinbutme\b|\bTheCalmBeforeTheStorm\b|\bStorm4Arturo\b|\btsnownami\b|\bsnowrnado\b|\bthecalmbeforethestorm\b|\bSNOWDAYBITCHESSSS\b|\bBuffaloSnowStorm\b|\bmediastorm\b|\bMeltTheSnow\b|\bsnowrain\b|\bsnowwalk\b|\bbffsnow\b|\bImMadAtYouSnow\b|\bfthissnow\b|\bsnowwhatsnow\b|\bbuffaloblizzard2014\b|\bWGRZStorm\b|\bSNOW\b|\bBeforeTheSnow\b|\bSnowveber\b|\bWhatIsSnow\b|\bfucksnow\b|\bsnowingrightnow\b|\bFirstSnowFall\b|\bCalmBeforeTheStorm\b|\bFireStorm\b|\bgetyoursnow\b|\bsnowgeese\b|\bthesnowisreallypilingupoutside\b|\biblendinwiththesnow\b|\bNotSoSnowvember\b|\bBuffBlizzard\b|\b2014SnowStorm\b|\bSnowDogs\b|\bPurfekStorm\b|\bnovembersnow\b|\bSnowmageddon\b|\bSnowyRideHome\b|\bsnowbash2014\b|\bSnowcalypse\b|\bblizzardof2014\b"

    ]

    # sorted_x = sorted(l.items(), key=operator.itemgetter(1))
    # for i in xrange(len(sorted_x)):
    #   print sorted_x[-1-i]


    import re
    import csv


    # do not include general words, e.g., napa, naturaldisaster

    def hash_filter(input_file, s):

        output_file = input_file[:-23] + "filtered_hash.txt"

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
        l = manually_verified_hashtags[ij].split('|')
        print "manually hash :", len(l)
        hash_filter(i, manually_verified_hashtags[ij])

    print '\n', disaster_array[ij]

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_affected_filtered_hash.txt") as f:
        print 'the number of affected hash filtered tweets', sum(1 for _ in f)

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] + "_unaffected_filtered_hash.txt") as f:
        print 'the number of unaffected hash filtered tweets', sum(1 for _ in f)

