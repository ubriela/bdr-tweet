import os
import csv
import glob
import operator
import re

#with open("", 'rU') as f:
#    rd = csv.reader(f, delimiter=",")
#arr = [11,12,13]


disaster_array = ["michigan_storm", "california_fire", "washington_mudslide", "iowa_stf", "iowa_storm", "jersey_storm", "oklahoma_storm", "iowa_stf_2", "vermont_storm", "virginia_storm", "texas_storm", "washington_storm", "washington_wildfire", "newyork_storm"]
state_code = [26, 6, 53, 19, 19, 34, 40, 19, 50, 54, 48, 53, 53, 36]

hash_1 = [r"""storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding | detroitflood""",
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
          r"""wind | breeze | storm | windstorm""", #wash storm
          r"""fire | burning | wildfire""", #wash wildfire
          r"""storm | windstorm | tempest | high wind | strong wind | flood | high water | flooding | snow | snowstorm | storm | blizzard"""] #new york

keywords = [
    r"""storm | windstorm | high wind | strong wind | flood | high water | flooding""",
    r"""mudslide | wild fire | wildfire | landslide""",
    r"""storm | windstorm | high wind | strong wind | tornado | typhoon | hurricane | flood | high water | flooding""",
    r"""storm | windstorm | high wind | strong wind | tornado | typhoon | hurricane | flood | high water | flooding""",
    r"""storm | windstorm | high wind | strong wind """,
    r"""storm | windstorm | high wind | strong wind | flood | high water | flooding""",
    r"""storm | windstorm | high wind | strong wind | tornado | typhoon | hurricane | flood | high water | flooding""",
    r"""storm | windstorm | high wind | strong wind | flood | high water | flooding""",
    r"""thunderstorm | landslide | mudslide | storm | windstorm | high wind | strong wind | flood | high water | flooding""",
    r"""storm | windstorm | high wind | strong wind | tornado | typhoon | hurricane | flood | high water | flooding""",
    r"""storm | windstorm""",  # wash storm
    r"""storm | windstorm | high wind | strong wind | flood | high water | flooding | snowstorm"""]  # new york

keywords_for_all_disasters = set();
for key in keywords:
    parts = key.split('|')
    for part in parts:
        keywords_for_all_disasters.add(part.strip())

all_flood_keywords = ' | '.join(keywords_for_all_disasters)     # keywords related to flood-related disaster

all_fire_keywords = "wildfire | wild fire"                      # keywords related to wildfire-related disaster

#INPUT_FOLDER = "./data/washington_wildfire/hash"
for ij in xrange(len(disaster_array)):
    # if ij == 6 or ij == 8 or ij == 9 or ij == 12:   # skip some disasters due to not having enough data
    #     continue
    l = {}
    r = re.compile(
            hash_1[ij],
            flags=re.I | re.X)

    for file in glob.glob("./data/disasters/" + disaster_array[ij] + "/hash" + '*/*.txt'):
        #print file
        filename = re.findall('[^\\\\/]+', file)[-1]

        idfilepath = str(filename)

        if int(idfilepath[11:13]) == state_code[ij]:
            #print idfilepath

            with open("./data/disasters/" + disaster_array[ij] + "/hash" + "/" + idfilepath, 'rU') as f:
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
    # print len(hash_2)
    #print (hash_2)

    s = ''
    for i in hash_2:
        s += i + " | "

    s = s[:-3]
    #s += " | dff"
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
        all_flood_keywords + " | floodageddon | stupidfloods | floodmageddon | thegreatflood | flooding | FloodsAren | floodzilla2014 | flood | nonstopstorms | majorflooding | floodssuck | Detroitflood | zomgfloods | basementflood | itsstormingthough | floodingintaylor | michiganflood2k14 | IntoTheStorm | FloodDay | flooded | Floodageddon | afterthestorm | DetroitFlood2014 | floodedbasement | dearbornflood | floodingindetroit | NoFloodZone | Flooded | StupidFlood | FloodedinDetroit | schoolsflooded | detroitflood2014 | floods | MIFlood | theflood | detroitfloods | Local4stormpicks | StormvsEdgerton | TheFlood | storm | basementisflooded | floodedroads | FloodsEverywhere | floodmagedon | floodingindearborn | thunderstorm | floodrecovery | detroitisflooded | Flood | greatfloodof2014 | beastisflooded | metrodetroitflooding | Flooding | stupidflood | onlyroutenotflooded | FLOODZONE | floodsfordays | aramfloodlive | floodymess | flood2014 | summerstorm | Floodgate | detroitflooding | taylorflood | floodedout | thunderstorms | miflood | FloodingProblems | thegreatflood2k14 | Flood2014 | floodpocalypse2014 | DetroitFloodOf2014 | floodseverywhere | GreatFlood | DetroitFloods | flashflood | detroitFlood | celebritystorms | FloodWarnings | DetroitFlood | detroitflood | nofloods | midweststorm | livefromtheflood2014 | floodingproblems | Floodpocolypse | storms",
        all_fire_keywords + " | cafire | StreetsOnFire | californiafire | calfires | willfire540 | firefight | FirecrackersElderts | wegotthatfire | habanerohellfire | LakeCountyFires | TassajaraFire | summitfire | KesterFire | 1yearsincefireproof | oxnardfire | calfire | norcalonfire2015 | FireAndTheFlood | FireHotMami | woodburninggrill | fireescape | Firefighters | TenayaFire | buffalofiredepartment | fireengine | 1YearSinceFireproof | aliottasviafirenze | FireTrucks | firemen | legsbeonfire | valleyfire | westcovinafiredepartment | cawildfirerelief | firehazard | firefire | ArcadeFire | Firemen | sunnyvalefire | lacountyfire | woodburning | woodfire | putoutthefires | carfire | thefirewentwild | FullertonFire | firefighters | brushfire | HouseOnFire | firehouse | SanJoseFire | CAFires | arcadefire | Campfire | laurelesfire | Roughfire | FireTruck | junctionfire | LaurelesFire | kingscountyfiredepartment| Valleyfire | firefightercostume | WeGotThatFire | sundancefire | firethecannons | firewood | fullertonisonfire | RisnerFire | DonationsForTheFireVictims | wildfire | hummerfire | lakecountyfire | limofire | thefirewatchersdaughter | cobbfire | firesuppression | thearcadefire | yosemitefire | roughfire2015 | LaHabraFire | thesmelloffirewood | EarthWindandFire | firedancing | RockAfireExplosion | venturacountyfiredepartment | LAOnFire | arcadefireinmyears | PachecoFire | tassajarafire | firestone805 | buttefire | fireshurtredcrosshelps | firefighterbrotherhood | ValleyFire | firefighting | streetsonfire| roughfire | breathoffire | fireman | ThankYouFirefighters | onfire2015 | liveyourfiretv | firedancers | glazefire | WildfireSmoke | firefighter | moralesfire | valleyFire | cawildfires | pitfirewestlake | WhenTheresAFire | losangelesfiredepartment | FuckinFire | firetruck | fireinthesky | quadsonfire | ButteFire | wildfiresmoke | forestfire | firecontrol | firemenarehot | FiremenAreHot | ButteCountyFire | lakevillefire | butteandvallyfires | LakeFire | RoughFire | itlooksliketheskyisonfire | ButteMountainFire | OldFire | buttefire2015 | CalFire | CaliforniaFireSeason | firedepartment | Tenyafire | ValleyFires | wildfires | futurefirefighter | rimfire01 | HumboldtFireDepartment | yosemitefires | heritagefire | Calfire | californiaisburning | Hellfire | skyonfire | OnFireNorCal | Cawilfires | californiafires | californiaisonfire",
        all_flood_keywords + " | preventwildfires | WAWILDFIRE | wildfires | WAWildfires | morefires | WAWildFire | wildfiresunrise | firetrail | firehelmets | wafire | baldyfire | WAWildFires | fireseason2015 | washingtonfires2015 | TacomaFire | washingtononfire | Wildfire | chelanfires | forestfire | WAwildfire | WashingtonOnFire | grizzlybearfire | firehaze | wawildfire | nomorefiresplease | forrestfire | FireSmog | pnwfires | washingtonStateFires | firefighters | WaWILDFIRE | washingtonfires | urbancampfire | worldonfire | Wildfires | NotSureIfChelanFireCanReachMe | ThankYouFirefighters | wildfirefundraiser | chelancomplexfire | firemen | firepocalypse2k15 | prayforFirefighters | forestfires | thankufirefighters | firstcreekfire | WAWildfireRelief | wildfire | Fireworks | okanaganfire | firefighter | fireseason | prayersforfirefighters | thewestcoastisonfire | wildfirefilter | chelanfire | wildfiresunset | thankafirefighter | wawildfires | WashingtonFires | TacomaFireDepartment | WAwildfires | firefighting | rennerfire | wafires | WAWildfire | thankyoufirefighters",
        all_flood_keywords + " | faketornado | strobelightstorm | NextStormChaser | floodprobs | stormpanos | TornadoOutbreak | HateStorms | stormyweather | FlashFloodAlarm | pleasedontstorm | FloodWaters | prayingfortornado | TwisterChasers | thunderstorm | FloodStage | onlyinstormlake | accidentalstormchasers | stormwatching | TornadoBaseball | Flooding | damnstorm | stormy | storms | StorminSiouxCity | StorminMcNorman | TornadoWarning | stormdamage | Iaflood | StormChasers | lovestorms | storm | windy | NebraskaTornadoes | ILoveStorms | flooded | iaflood | stormchasers | StormCrazy | RockValleyflood | StormChaser | strongwinds | StupidThunderstorm | Stormy | Storms | Pilgertornado | tornadobelt | yaywind | Flood | stormupdates | Tornado | dualtornadoes | astormiscoming | dustinthewind | Iowaflooding | floodingeverywhere | nightstorms | FloodedStreets | stormseason | tornadosafety | HurricaneKony2014 | floods | lovetornadoes | anotherstorm | humidstormcells | stupidtornadoes | teamwind | tornadosamiright | StormOver | Halestorm | Stormcon | stormABrewing | flashflood | floodof2014 | Haveyflood2014 | missouririverflood | freakinstorm | tornadoes | TornadoCantStopMe | tornadowatchsucks | thunderstormsongs | weatherthestorm | CycloneWarning | IHateStorms | stormday2014 | stormchaser | tornadowatch | ihatestorms | FuckTheStorm | windswept | flood2k14 | SoulStorm | Flood2014 | TwoTornadoes | strongstorms | Storming | nostorm | hatetornados | flooding | windfactor | flood | stormkyaking | thewindbegantoswitch | Thunderstorm | rewind | summerstorms | tornadoesgotnothin | damnstorms | socialmediaisflooded | dramaticstormpic | windevent | halestorm | windinmyhair | feelthebreeze | winding | hatestorms | Tornados | flood2014 | thunderstorms | tornadowarning | flashfloods | Windsor | tornado | twintornados | StormWatchin",
        all_flood_keywords + " | tornadowarning | TornadoWarning | storm | tornadowatch | iwantstorms | flood | stormynight | tornadoes | stormchasers | stormsoverbachelorette | rainstorms | thunderstorm | solarstorm",
        all_flood_keywords + " | stormyweather | thunderstorm | storms | calmafterthestorm | storm | afterthestorm | calmbeforethestorm | stormchaser | storm2015 | inbeforethestorm | TheStorm | Thunderstorm | stormsabrewin | darkandstormy | Storm | summerstorm | thunderstorms | thecalmbeforethestorm",
        all_flood_keywords,
        all_flood_keywords + " | floodageddon | tornadoweather | HailStorm | StormsAreFun | flooded | floodedbasement | stormchasemedia | Wind | stormysummer | HelloFloods | stupidstorm | severestorms | TonadoWarningsOnTornadoWarnings | thunderstorm | stormchasin | openyourwindows | ThanksStorms | TornadoAlley | bravetheflood | stormcon | Flooding | stormy | storms | Storms | tornadoseason | storm2k14 | floodprobs | floodprobz | StormWatch | stormdamage | tornadowarnings | flood14 | StormChasers | JoCoflooding | windy | hashtagtornadolifeyoloswag | stopflashfloodsinIowa | wind | CRflood14 | afterthestorm | floodsafety | goawaystorms | stormpics | DamnStorms | 2014floods | srryforthestormtweet | storming | StormChaser | downwindstruggle | floodwatch | storm | crazystorm | AmesFlood14 | LoveStorms | Flood | Tornado | TORNADO | TornadoOrNah | floodwatergalore | calmbeforethestorm | severethunderstorm | iowastorms | floodcity | HurricaneGoodbyeIowa | Floodsof2014 | Iowastorms | ilovefallingasleeptostorms | flashflood | tornados | ridingthestormout | floodof2014 | TyphoonNeoguri | 2014flooding | stormpocalypse | tornadoes | StormChasing | stormbycandlelight | FloodWaterFun | FloodOf14 | floodof14 | stormchaser | stormchasing | tornadowatch | iowafloods | ihatestorms | windowsrattling | flooddanger | fuckstorms | thestormhaspassed | CalmAfterTheStorm | stormaggaden | Stormchasers | flooding | flood | FlashFlood | iowaflooding | allglasswindows | Storm | DarkandStormy | stormofthecentury | scaredofstorms | coleswindell | hatestorms | 2014Floods | QCFlood2014 | flood2014 | summerstorm | thunderstorms | floodedriver | tornadowarning | stupidstormreports | IowaStorms2014 | tornado | JoCoFlooding | windyaf | Thunderstorms | highwater",
        all_flood_keywords,
        all_flood_keywords,
        all_flood_keywords + " | TexasFlood | Stormcon | strongsunsetandstorm | dfwflooding | HurricanePatriciaonablunt | sanantonioflood2015 | texasflood | summerstorms | praisegodthroughthestorm | HighWaters | thunderstorm | flooded | TornadoWarning | Flooding | stormy | storms | hurricaneproblems | floodmageddon2015 | HurricaneParty | rainstorm | austinfloods | tornadocActivity | hurricane | floodingfail | stormdelays | hurricanewedding | floodwaters | storm | hurricaneseason2015 | windy | floodwatching | TornadoWhile | TexasFloods | wind | halloweenfloods | tropicalstormpatricia2015 | 2015flood | electricalstorm | flashfloodwarning | centexfloods | atxfloods | hurricanepatricia | WindingRoadRacing | TornadoWatch | storming | glorywind | TORNADO | HurricanePatricia | FloodedEveryWhere | onioncreekflood | lovefloods | Stormfood | TrinityFlooded | stormfood | stormyweather | WickedStorms | HurricanePatriciaRain | floods | Flooded | floodwatchandchill | itswindy | smtxflood | seriousstorm | floodlife | sanmarcosflood | halloweenflood2015 | flashflood | fireandtheflood | brushycreekfloods | StormOfTheCentury | sanmarcosflood2k15 | hightowerhurricanes | HurricaneSeason | HoustonFlood | FLOOD | blancoriverflood | thestormafterthestorm | flashfloods | atxflood2015 | floodpuns | stormiscoming | StormComing | Stormageddon | calmbeforethestorm | stormsthatgoboom | FlashFlood | hurricanepatricia2015 | flooding | coolbreeze | tornado | flood | floodindownintexas | UnionCreekFlood | OutRunningTheHurricane | Texasflood | floodpacolypse2015 | texasstorms | viewfrommywindow | Houstonflood | monsoonflooding | Storm | thxstorm | windydays | HurricaneHeat | halloweenfloods2015 | houstonflood | FlashFloods | floodwarning | txflood | Hurricane | hurricaneweather | strongeststormever | itsflooding | itsJUSTatropicalstorm | hurricanes | thunderstorms | tornadowarning | stormcoming | flashfloodwarnings | HoustonFloodWatch | ATXFlooding | Thunderstorms | floodingintexas | whathurricane | FloodOfHalloweenEve | ThanksStorm | Tornado",
        all_flood_keywords + " | pwnwstorm | itssortawindy | thestorm | duststorm | wawind | storme | windblowsmyfaceoff | calmafterthestorm | windschief | storm | windy | bringonthestorm | morningstorm | wind | windyinseattle | windfarm | windenergy | windycity | wawindstorm | Summerstormproblems | windrainorshine | calmbeforethestorm | stormyweather | quietstorm | unwind | SeattleStormageddon | storm2015 | dirtstorm | windstorm | Thunderstorm | holywindbatman | nameourstorms | windydays | stormynights | stormwatch | windsurfing",
        all_fire_keywords,
        all_flood_keywords + " | stormaintstoppingus | Stormcon | LakeEffectSnow | Snowpocalypse | firstdayofsnow | nosnowdaysNovember | ilikeSnow | bringonthesnow | SnowLover | Snowmedoggy | LetItSnow | snowstop | SNOWBOWL | Snowband | nosnow | BuffaloSnow | doublesnowday | winterstorm | lakeeffectsnowwarning | snowpacalypse2k14part3 | SnowEmergency | Buffalosnow | SNOWevember | BlizzardOf2014 | snowvembertoremrmber | letitsnowletitsnowletitsnow | iwantasnowday | Tsnownami | Firestorm | Snowmagedon | SnowAngels | AtLeastWeHaveNoSnow | BuffaSNOW | BuffaloBlizzard2014 | novembersnowday2k14 | stupidstorm | novemberstorm2k14 | THUNDERSNOW | shitstorm | giantsnowflakes | snowpocalypse2k14 | FIRSTSNOW | Snowcopalypse | buffasnow | 3rdSnowDay | lakesnoweffect | cnystorm | SnowStormActivties | snowday4 | snowday3 | snowday1 | snowdays | stormywednesday | Buffaloblizzard2014 | wtfsnow | snowocalypse2k14 | snowcantcatchme | snowtime | goawaysnow | snowpleasestayinsouthtowns | ThanksgivingSnow | floodgates | snowmageddon | WGEZSNOW | BNstormready | snowshoecatsofinstagram | Buffalsnow | fuckthesnow | Buffalostorm | snowvemberbender | winterstormGodzilla | NYCsnow | khoopsnow | prayforasnowday | SydneyStorm | storm | turnupinsnow | PerfectStorm | snowstormofthecentury | wheresthesnow | snowshmo | snowdaysfordays | HappySnowDayNYC | snowremovalproblems | halfblizzard | snowinNewYork | LetItGoSnow | lakeeffectsnowstorm | SnowBeltprobs | SnowFallo | IWantSnow | verylittlesnownorth | Snownami | SNOWpocalypse | snowneonta | snowbound | knifestorm2014 | stormcasualty | BuffaloNewYorkSnow | ShovelThatSnow | SnowDay2014 | stormkingmoments | snownado | StormHowie | Snow | snowdayfromwork | snowday2014 | snowpocoplyse | snowfordays | ILoveSnow | waposnow | snowynights | TheSnowNews | snowrun | snoweater | snowround2 | PurfekStormGroup | Winterstorm | nomorefloodedengines | 3INCHESOFSNOW | FirstSnow | snowpocalypseBuffalo | Snowshoes | snowthunder | Thundersnow | snowmakeseverythingfun | twosnowdaysinarow | clearingsnow | Buffaloblizzardbeers | 4feetofsnow | Blizzard2014 | snowingoutside | snowdayhappiness | SnowWhite | triplesnowday | Snowchat | snowflakes | INTHEKNOWFORSNOW | HALESTORM | Flood | stupidsnow | itshellasnowing | snowshoveler | blizzardballin | RidingOutTheStorm | lovesnowdays | snowdaydecisions | itsgonnasnowagain | snowdaypart2 | snowdaypart3 | buffalostorm | WhyIsntThisSnow | buffaSNOW | SOUTHTOWNBLIZZARD | winterstormcato | SnowAlley | SnovemberStorm | NewYorkSnowDay | WGRZsnow | nomoresnow | lakeeffectstorm | leavingbeforethesnowstorm | redstorm | comeonsnow | Snowing | snowmountain | ItsSnowing | funsleddinginrhesnow | quietstorm | SnowCoveredTDI | TheSnow | WinterStormKnife | sNOwINbuffalo | snowshoeing | SnowThankYou | snowpocalyps | snow2014 | ONstorm | Blizzard | snowmaggedon | firstsnow | SNOWvember | SnowmageddonMyButt | FuckTheSnow | ihatesnow | stormking | Snowvber | andyourBumAssSnow | snowdaysshavery | seniorsskipsnowday | lovesnow | nosnowyet | thingsyoudoonasnowday | snowsucks | swallowedbysnow | highwaters | becauseSnow | SnowShovelWorkout | goredstorm | StillSnowingHere | NovSnow2014 | blizzardprobs | snowflake | Snowday | happysnowday | WallOfSnow | SnowdoginBuffalo | nomoresnowplease | abc7snow | snowdayfunday | Downofthesnow | snowbreak | snowlovers | QuietBeforeTheStorm | stormvember | nonamestorm | NoSnow | haulingsnow | smellslikesnow | dothesnowshovel | tooearlyforsnowflakes | whollysnowbatman | sickofsnow | stormiscoming | famoussnowstorm | wedontneednofrickinsnow | FunOnTheSnow | miraclesnow | itsjustsnow | eyeonthestorm | upstateLakeeffectsnow | WinterStormCato | snowdayround4 | hidingfromthesnow | buffalosnowmiracle | WhatBlizzard | papersnowflakes | talliastorm | SuccessfulStudentsDontGetSnowDays | Snowbash2014 | perfectstorm | LESSnow | wheresallthesnowiwaspromised | blizzard14 | newyorksnowstorm | WinterStorm | snowmachines | snowfallselfie | snowpacalypse | Snowvembertoremember | notreadyforsnow | SnowJoy | snowmen | snownedin | stormnecessity | HappySnowDays | snowmagedon | Snowy | SnowSurvivalPlan | StupidSnow | Snowvember2014 | blizzard | KNIFEstorm | snowvembertoremember | snowstorm2014 | 2SnowDays | iactuallyhatesnow | snowpocalypse | evenblizzards | snowpocolypse | snowshovel | iblamethesnow | SNOWMAGGEDON | thecalmbeforethesnow | FirstSnowStormOf2014 | Wgrzsnow | snowityourway | Thanksgivingsnow | blizzardparty | snowdayround3 | Blizzard14 | HighWinds | IHateSnow | BlizzardBoredom | stormdamage | NoSnowPLZ | snowwheretoputit | iheartsnow | turkeystorm | runninginsnow | ihatesnowdays | gokissanIndiansassnow | snowpacolypse2k14 | snowdog | SnowmobilerProblems | snowedourwayintoprimetime | snowhailrain | LetsGoSnowffalo | Snowvember | buffaloblizzard | hopewedontgetsnowedin | snowfie | wetsnowrainmix | halestorm | adultsnowday | snowwhite | snownami | snowdayround2 | SNOWVEMBER14 | notthankfulforsnow | byebyesnow | RainSleetSnowDay | BuffaloStorm | throughthestorm | SnowOnFOX | stormnames | WinterStormAdvisory | SnowvemberDrunkvember | snowmageddon14 | Snowmobiling | sabresfansnowday | astormisbrewing | Iwantasnowday | SnowstormBuffalo | snowdayalldayerrrrday | SnowfallOnTheWay | calmbeforestorm | canisiussnowdaypt2 | snowvemberbearit | winterstorms | myniggaknowsnowsoicanpostthis | floodingProbs | BuffaloSnowday | strugglesofblizzard2k14 | NewYorkSnow | wishingitwasasnowday | PersonalSnowDay | nysnow | blacksnow | thanksgivingsnow | snowmagedonwhat | PastorMikeSays | rainsnow | snowblowing | stilllovesnow | southbuffalosnowday | SnowForDays | freesnowwhite | abc7NYsnow | NotChristmasTimeUnlessItsSnowing | blizzardcravings | floodwarning | suckitwinterstormCato | snowvemberstorm | snowmobile | fuckyousnow | NovemberStorm2014 | flooded | blizzardhacks | ABC7NYSnow | Fuckthesnow | SnowFall | SnowVember | SnowIsComing | snowoutside | itssnowing | pjsnow | ScavinoStormCenter | LakeEffectSnowStorm | snowstormdelay | snowbaby | DontSnortTheSnow | SnowDayStreak | firstworldblizzardgamerproblems | snowlightening | thankssnow | SnoWvember | prankwarstartsnow | TurnUpDelayedForSnow | Olihavingfuninthesnow | SnowIntoWater | SnowdayIII | snowed | buffalostorm2014 | frickyousnow | Firstsnow | wheresmysnow | BuffaloSnowstorm | snowmobiling | articsnowbelt | WinterStormWatch | ThunderSnow | twerkforjoessnowday | BuffaloSnowStorm2014 | SnowPretty | snowhaboob | Buffasnow | BringOnThatSnow | SuperstormSandy | StormSixPack | tomuchsnow | snowday | stormin | teamnosnow | tsnownami2014 | snowflakeonfifth | snowproblems | purfekstorm | SnowFlake | HateTheSnow | snowmygoodness | snowvember2remember | itssnow | snowwite | snowfodays | IHATESNOW | needasnowday | Snowbember | WGRZSnow | asIf60InchesOfSnowIsntEnough | SNOWVEMBER | SaveStorm | snowdaybordem | snowsgone | snowneverstoppedme | Snowflake | quietbeforethestorm | whothefuckiscadistorm | BronxSnow | FirstStorm2014 | Snowbound | toomuchsnow | LOOKATTHE4FEETOFSNOWINTHESTREET | snowbuffalo | ThruTheStorm | FunInTheSnow | SnowBelt | SnowedInThoughts | RainySnowyDay | Snovember2014Storm | snowshoes | ILikeSnowButShoveling | 2014blizzard | ItsTheSnowsFault | snowytrees | twcnewssnow | snowdonia | ilovesnowdays | 1stSnow | SnowAintNoJoke | BringOnTheStorm | Buffaloflood | snowboundzombies | LakeEffectSnowSTORM | Darkandstormy | SnowvemberSucks | snowstormhopping | blizzardconditions | snowboots | WGRZSNOW | buffaloflood | SnowStorm | Snowsgiving | bringmethesnow | ItsSnowsHere | IPlowSnow | SnowDayNumber3 | stillsnowing | somuchforabigsnowstorm | attackoftheiceandsnow | SnowEDin | syracusesnow | holysnow | snowpocalypse2014 | pray4snow | SnowvemberSavesOurGrades | floodwatch | GoHomeSnow | crazystorm | ubsnowday | FuckTheSnowDay | IWantASnowDay | snowstorm | Stormville | WarmSnow | damnsnow | SnowCaps | snowscomin | firstsnowfun | snowerrywhere | TheFallingSnow | blizzardof77 | Snowvembver | THUNDERSNOWFOOTBALL2014 | snowvember | offseasonstartsnow | StormKing | snowsouttitsout | NovemberSnow | snowtown | snowinmymouth | Snowpocalypse2K14 | wgrzsnow | BuffaloStorm14 | WhoNeedsSnowBoots | snowpacolypse | blizzardcomingsoon | SabresFanSnowDay | snowridge | snowslomo | SnowHappens | buffalosnowchallege | calmbeforethestorm | ReportedSnowAlready | yaysnow | snowvemberprobs | snowsessions | novemberstorm | NovemberStorm | SnowdayTurnup | snowdayplz | SnowChesterNy | snownyc | RedStormFridays | Yellowsnowhadtogo | snowheart | LESnow | OurSnowMachine | nosnowfornyc | snowscoming | dfsnow | stormkingartcenter | Halestorm | snowdaytuesday | SnowBaby | SnowDays | SnowDay4 | snowedinandhungry | snowbank | snowband | NW2Wsnow | snowblower | what_snow | stormpreparedness | hatesnow | weinablizzardman | hailstombetterthanwinterstorm | snowember | icysnow | 2snowdays | stormknife | stormprobs | FyahStorm | havetheynamedthisstormyet | somuchsnow | floodinsurance | lakeeffectsnow | snowfall | snowdayforMomma | buffalosnow | CanisiusSnowDayPt2 | CanisiusSnowDayPt3 | buffalosnowstorm | lohudsnow | winterstormKNIFE | SnowDay | snowedin2014 | bringsnowblowers | PraysForAlotOfSnow | lotsofsnow | snowbrush | letitsnow | needmoresnow | wgrztvsnow | snowbowl | giantsnowflake | SnowToForehead | snowmaking | idloveasnowstormlikethat | birthdayweekendbeginsnow | wnysnow | blizzardmyass | hatingsnow | snowpants | thankyousnow | snowbowl2014 | snowpocalyspe2014 | WhatWouldSnowDo | snowremoval | stopthesnow2014 | FirstSnowOfTheSeason | SnowBuffalo | Snowstorm | WinterStormWarning | snowdogs | ilovesnow | ihatethesnow | snow | clarencesnowday | wolsnowcamp | GetStormATwitter | lovethesnow | LovinThoseConcentratedSnowStorms | TooMuchSnow | tcnewssnow | SnowblowerElbow | snowedinstruggles | BuffalOsnow | anothersnowday | blizzard2014 | knifestorm | snowedinstruggle | Snowember | snowing | hatethesnow | scaredofsnow | snowdayproblems | bestsnowdayever | flooding | FuckSnow | snowday2 | buffsnowday | NotSnowboardingWeather | BuffaloSnowedIn | FLOODWATCH | mrsnowmizer | itsnowed | BuffaloBlizzard | snowdaythoughts | snowblowerless | snowtsunami | snowstrong | FourDaySnowDay | StormKnife | snowtine | ilovethesnow | Itstartsnow | snowalldayeveryday | snowbandproblems | SnowStorm14 | Snowpocalypseproblems | pushingsnowdrinkinbeerwithconzi | fuckthissnow | blizzardworkout | TWCNewsSnow | snowy | snoww | firstsnowoftheseason | winterstormknife | supersnowdog | thundersnow | hamburgblizzard11 | fuckingsnow | Storm | FristSnow2014 | itwasalsosnowing | snowydusk | snowny | firstsnowfall | Storm2014 | oksnowpolice | Snowweeks | buffalsnow | everyonessnowedinbutme | TheCalmBeforeTheStorm | Storm4Arturo | tsnownami | snowrnado | thecalmbeforethestorm | SNOWDAYBITCHESSSS | BuffaloSnowStorm | mediastorm | MeltTheSnow | snowrain | snowwalk | bffsnow | ImMadAtYouSnow | fthissnow | snowwhatsnow | buffaloblizzard2014 | WGRZStorm | SNOW | BeforeTheSnow | Snowveber | WhatIsSnow | fucksnow | snowingrightnow | FirstSnowFall | CalmBeforeTheStorm | FireStorm | getyoursnow | snowgeese | thesnowisreallypilingupoutside | iblendinwiththesnow | NotSoSnowvember | BuffBlizzard | 2014SnowStorm | SnowDogs | PurfekStorm | novembersnow | Snowmageddon | SnowyRideHome | snowbash2014 | Snowcalypse | blizzardof2014"
    ]

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
                        #print a[0]
                    if re.search(r, a[0]):
                        #print disaster_tweets_count
                        disaster_tweets_count += 1
                        f2.write(', '.join(a) + '\n')

                #print "Disaster related tweets: ", disaster_tweets_count


    f = ["./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] +"_affected_unfiltered.txt", "./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] +"_unaffected_unfiltered.txt"]

    for i in f:
        hash_filter(i, manually_verified_hashtags[ij])


    print '\n', disaster_array[ij]

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] +"_affected_filtered.txt") as f:
        print 'the number of affected_filtered tweets', sum(1 for _ in f)

    with open("./data/disasters/" + disaster_array[ij] + "/" + disaster_array[ij] +"_unaffected_filtered.txt") as f:
        print 'the number of unaffected_filtered tweets', sum(1 for _ in f)