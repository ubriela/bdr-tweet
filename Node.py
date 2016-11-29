from Params import Params

""" generic node class """

from UtilsBDR import distance_km
class Node(object):
    """ generic tree node class """

    def __init__(self):
        self.n_data = None  # list of data points
        self.n_box = None  # 2 by 2 matrix [[x_min,y_min],[x_max,y_max]]
        self.nw = self.ne = self.sw = self.se = None
        self.n_count = 0  # count of this node
        self.n_depth = 0
        self.n_failSplit = False
        self.n_isLeaf = False

        self.urgency = 3
        self.children = []  # list of its children

    def center(self):
        return [(self.n_box[0][0] + self.n_box[1][0])/2, (self.n_box[0][1] + self.n_box[1][1])/2]

    def area(self):
        a = distance_km(self.n_box[0,0],self.n_box[0,1],self.n_box[0,0],self.n_box[1,1]) * distance_km(self.n_box[0,0],self.n_box[0,1],self.n_box[1,0],self.n_box[0,1]);
        return a

    def update_count(self):
        if self.n_isLeaf is False:
            self.nw.update_count()
            self.ne.update_count()
            self.sw.update_count()
            self.se.update_count()
            self.n_count = self.nw.n_count + self.ne.n_count + self.sw.n_count + self.se.n_count


    def find_subnode(self, ptx, pty):
        if self.n_isLeaf is True:
            return self
        elif ptx <= self.nw.n_box[1, 0] and pty >= self.nw.n_box[0, 1]:
            return self.nw.find_subnode(ptx, pty)
        elif ptx >= self.ne.n_box[0, 0] and pty >= self.ne.n_box[0, 1]:
            return self.ne.find_subnode(ptx, pty)
        elif ptx <= self.sw.n_box[1, 0] and pty <= self.sw.n_box[1, 1]:
            return self.sw.find_subnode(ptx, pty)
        elif ptx >= self.se.n_box[0, 0] and pty <= self.se.n_box[1, 1]:
            return self.se.find_subnode(ptx, pty)
