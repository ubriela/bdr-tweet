# Basic parameters
class Params(object):
    input_filename = "./data/CL_raw_training.csv"
    output_filename = "./data/CL_refined_training.csv"
    vocab_filename = "./data/Tweets.vocab"

    # DATASET = "napa"
    #
    # NDATA = None
    # NDIM = None
    LOW = None
    HIGH = None
    # nQuery = 2  # number of queries
    # unitGrid = 0.01  # cell unit in kd-cell
    # ONE_KM = 0.0089982311916  # convert km to degree
    #
    # ZIPFIAN_SKEW = 2
    # URGENCY_RANDOM = True
    #
    # POPULATION_FILE = '../../dataset/gowalla_CA.dat'
    #
    # # for grid standard
    # # maxHeight = 2
    # # part_size = 6
    # # ANALYST_COUNT = 36
    #
    # part_size = 8
    ANALYST_COUNT = 2**10

    big_disaster_ids = ["napa_earthquake", "michigan_storm", "iowa_stf",
                    "iowa_stf_2", "texas_storm", "newyork_storm"]
    disaster_ids = ["napa_earthquake", "michigan_storm", "california_fire", "washington_mudslide", "iowa_stf",
                    "iowa_storm", "jersey_storm", "iowa_stf_2", "texas_storm", "washington_storm", "newyork_storm"]

    disaster_duration = {
        "napa_earthquake" : ('08-23-2014 00:00:00', '08-31-2014 23:59:59'),
        "michigan_storm" : ('08-10-2014 00:00:00', '08-16-2014 23:59:59'),
        "california_fire" : ('09-08-2015 00:00:00', '09-21-2015 23:59:59'),
        "washington_mudslide" : ('08-08-2015 00:00:00', '08-23-2015 23:59:59'),
        "iowa_stf" : ('06-13-2014 00:00:00', '06-25-2014 23:59:59'),
        "iowa_storm" : ('06-19-2015 00:00:00', '06-26-2015 23:59:59'),
        "jersey_storm" : ('06-22-2015 00:00:00', '06-24-2015 23:59:59'),
        "iowa_stf_2" : ('06-25-2014 00:00:00', '07-09-2014 23:59:59'),
        "texas_storm" : ('10-21-2015 00:00:00', '10-31-2015 23:59:59'),
        "washington_storm" : ('08-28-2015 00:00:00', '08-30-2015 23:59:59'),
        "newyork_storm" : ('11-16-2014 00:00:00', '11-28-2014 23:59:59')
    }

    peak_day = {
        "napa_earthquake" : 0,
        "michigan_storm" : 2,
        "california_fire" : 2,
        "washington_mudslide" : 13,
        "iowa_stf" : 2,
        "iowa_storm" : 5,
        "jersey_storm" : 0,
        "iowa_stf_2" : 5,
        "texas_storm" : 8,
        "washington_storm" : 0,
        "newyork_storm" : 2
    }



    gesis_disaster_folder = './data/disasters/'
    with_sentiment_folder = './data/disasters/with_sentiment/'
    with_informative_folder = './data/disasters/with_informative/'
    without_tweet_folder = './data/disasters/without_tweet/'

    tweet_folder = './model/word2vec-sentiments-master/tweets/'
    label_folder = './model/word2vec-sentiments-master/labels/'


    #
    # GRID_SIZE = 1700
    # TIME_SNAPSHOT = 6

    def __init__(self, seed, x_min = None, y_min = None, x_max = None, y_max = None):
        self.Seed = seed
        self.minPartSize = 2 ** 5  # minimum number of data points in a leaf node
        #
        # self.resdir = ""
        self.x_min, self.y_min, self.x_max, self.y_max = x_min, y_min, x_max, y_max
        self.epicenter = [38.2414392,-122.3128157]
        # self.NDATA = None
        # self.NDIM = None
        # self.LOW = None
        # self.HIGH = None

    def set_data(self, dyfi_data, tweet_data):
        self.dyfi_data, self.tweet_data = dyfi_data, tweet_data

    def debug(self):
        print self.x_min, self.y_min, self.x_max, self.y_max
        print self.NDATA, self.NDIM, self.LOW, self.HIGH