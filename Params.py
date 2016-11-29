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

    #
    # GRID_SIZE = 1700
    # TIME_SNAPSHOT = 6

    def __init__(self, seed, x_min = None, y_min = None, x_max = None, y_max = None):
        self.Seed = seed
        self.minPartSize = 2 ** 4  # minimum number of data points in a leaf node
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