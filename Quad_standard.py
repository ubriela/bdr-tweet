import numpy as np

from Kd_pure import Kd_pure


class Quad_standard(Kd_pure):
    def __init__(self, data, param):
        Kd_pure.__init__(self, data, param)

    def getSplit(self, left, right):
        """If epsilon is zero, return middle point of lower/upper bound"""
        return (left + right) / 2

    def getCoordinates(self, curr):
        """ get corrdinates of the point which defines the four subnodes 
        same as in Kd_pure except explicitly deal with empty node in order to
        grow a full tree """
        dimP = curr.n_depth % self.param.NDIM  # ## primary split dimension
        dimS = 1 - dimP  # ## secondary split dimension, 2D use only
        _data = curr.n_data
        _box = curr.n_box

        if _data is None or _data.shape[1] == 0:
            splitP = (_box[0, dimP] + _box[1, dimP]) / 2
            splitS = (_box[0, dimS] + _box[1, dimS]) / 2
            if dimP == 0:
                x_nw, y_nw, x_se, y_se = splitP, splitS, splitP, splitS
            else:
                x_nw, y_nw, x_se, y_se = splitS, splitP, splitS, splitP
            return (x_nw, y_nw), (x_se, y_se), None, None, None, None

        _ndata = _data.shape[1]

        # ## Primary split
        _idx = np.argsort(_data[dimP, :], kind='mergesort')

        _data[:, :] = _data[:, _idx]
        splitP = self.getSplit(_box[0, dimP], _box[1, dimP])  # ## get split point for dim_1
        posP = np.searchsorted(_data[dimP, :], splitP)  # ## get split position for dimP

        # ## Secondary split - 1
        data_S1 = _data[:, :posP]
        S1_nonempty = True
        if data_S1 is None or data_S1.shape[1] == 0:
            split_S1 = self.getSplit(_box[0, dimS], _box[1, dimS])
            S1_nonempty = False
        else:
            _idx = np.argsort(data_S1[dimS, :], kind='mergesort')
            data_S1[:, :] = data_S1[:, _idx]
            split_S1 = self.getSplit(_box[0, dimS], _box[1, dimS])
            pos_S1 = np.searchsorted(data_S1[dimS, :], split_S1)

        # ## Secondary split - 2
        data_S2 = _data[:, posP:]
        S2_nonempty = True
        if data_S2 is None or data_S2.shape[1] == 0:
            split_S2 = self.getSplit(_box[0, dimS], _box[1, dimS])
            S2_nonempty = False
        else:
            _idx = np.argsort(data_S2[dimS, :], kind='mergesort')
            data_S2[:, :] = data_S2[:, _idx]
            split_S2 = self.getSplit(_box[0, dimS], _box[1, dimS])
            if split_S2 <= _box[0, dimS] or split_S2 >= _box[1, dimS]:
                split_S2 = self.getSplit(_box[0, dimS], _box[1, dimS])
            pos_S2 = np.searchsorted(data_S2[dimS, :], split_S2)

        if dimP == 0:
            x_nw, y_nw, x_se, y_se = splitP, split_S1, splitP, split_S2
            nw_data = data_S1[:, pos_S1:] if S1_nonempty else None
            ne_data = data_S2[:, pos_S2:] if S2_nonempty else None
            sw_data = data_S1[:, :pos_S1] if S1_nonempty else None
            se_data = data_S2[:, :pos_S2] if S2_nonempty else None

        else:
            x_nw, y_nw, x_se, y_se = split_S2, splitP, split_S1, splitP
            nw_data = data_S2[:, :pos_S2] if S2_nonempty else None
            ne_data = data_S2[:, pos_S2:] if S2_nonempty else None
            sw_data = data_S1[:, :pos_S1] if S1_nonempty else None
            se_data = data_S1[:, pos_S1:] if S1_nonempty else None

        return (x_nw, y_nw), (x_se, y_se), nw_data, ne_data, sw_data, se_data