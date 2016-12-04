import time
import logging
from collections import deque
from pylab import *
import numpy as np

from Params import Params
from Quad_standard import Quad_standard
from social_urgency_map import data_readin
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

def getPathData(data, param):
    path_data = []


    start = time.time()

    tree = Quad_standard(data, param)

    tree.buildIndex()

    print "time ", time.time() - start
    print "data points: ", tree.checkCorrectness(tree.root)



    leaf_boxes = getLeafNode(tree, 2)

    for data in leaf_boxes:
        # [[x_min,y_min],[x_max,y_max]]
        # if data[1] > 10:
        #     print (data[0][0][0]+data[0][1][0])/2 , "\t" , (data[0][0][1]+data[0][1][1])/2 , "\t" , data[1]
        path = []
        box = data[0]
        # (x_min, y_min) --> (x_min, y_max) --> (x_max, y_max) --> (x_max, y_min) --> (x_min, y_min)
        # print box[0][0], ',', box[0][1]
        # print box[0][0], ',', box[1][1]
        # print box[1][0], ',', box[1][1]
        # print box[1][0], ',', box[0][1]
        path.append((mpath.Path.MOVETO, (box[0][1], box[0][0])))
        path.append((mpath.Path.LINETO, (box[1][1], box[0][0])))
        path.append((mpath.Path.LINETO, (box[1][1], box[1][0])))
        path.append((mpath.Path.LINETO, (box[0][1], box[1][0])))
        path.append((mpath.Path.CLOSEPOLY, (box[0][1], box[0][0])))

        path_data.append((path, data[1]))

    return path_data

def getLeafNode(tree, type):
    leaf_boxes = []
    if type == 1:
        for l1_child in tree.root.children:
            if not l1_child.n_isLeaf and l1_child.children is not None:
                for l2_child in l1_child.children:  # child1 is a first-level cell
                    leaf_boxes.append((l2_child.n_box, l2_child.n_count))
            leaf_boxes.append((l1_child.n_box, l1_child.n_count))
    elif type == 2:
        queue = deque()
        queue.append(tree.root)
        while len(queue) > 0:
            curr = queue.popleft()
            if curr.n_isLeaf is False:
                queue.append(curr.nw)
                queue.append(curr.ne)
                queue.append(curr.sw)
                queue.append(curr.se)
            else:
                leaf_boxes.append((curr.n_box, curr.n_count))

    return leaf_boxes


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, filename='./log/debug.log')

    # dataset_list = ['yelp', 'foursquare', 'gowallasf', 'gowallala']
    # dataset_list = ['mediaq']


    param = Params(1000, 37.382166, -123.561700, 39.048834, -121.061700)
    data = data_readin(param)

    param.debug()
    path_data = getPathData(data, param)

    fig, ax = plt.subplots()
    # img = imread("background.png")
    for data in path_data:
        path = data[0]
        codes, verts = zip(*path)
        path = mpath.Path(verts, codes)
        # weight = min(1, (data[1] + 0.0) / 500)
        weight = 1
        patch = mpatches.PathPatch(path, facecolor='white', alpha=weight)
        ax.add_patch(patch)

        ax.xaxis.set_visible(True)
        ax.yaxis.set_visible(True)
        ax.axis('off')

        # plot control points and connecting lines
        x, y = zip(*path.vertices)
        # ax.imshow(img)
        line, = ax.plot(x, y, 'k-', linewidth=0.1)

    ax.grid()
    # ax.axis('equal')
    savefig('./graph/graph.png', format='png', dpi=400)