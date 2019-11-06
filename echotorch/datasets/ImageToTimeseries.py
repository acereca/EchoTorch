# -*- coding: utf-8 -*-
#
# File : echotorch/datasets/ImageToTimeseries.py
# Description : Transform a dataset of images into timeseries.
# Date : 6th of November, 2019
#
# This file is part of EchoTorch.  EchoTorch is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Nils Schaetti <nils.schaetti@unine.ch>


# Imports
import math
import torch
from torch.utils.data import Dataset


# Image to timeseries dataset
class ImageToTimeseries(Dataset):
    """
    Image to timeseries dataset
    """

    # Constructor
    def __init__(self, image_dataset, timeseries_length, time_axis=-1):
        """
        Constructor
        :param image_dataset: A Dataset object to transform
        :param timeseries_length: How many images to join to compose a timeserie ?
        :param time_axis: Time dimension
        """
        # Params
        self._image_dataset = image_dataset
        self._timeseries_length = timeseries_length
        self._time_axis = time_axis
    # end __init__

    #################
    # OVERRIDE
    #################

    # Length
    def __len__(self):
        """
        Length
        :return: How many samples
        """
        return int(math.ceil(len(self._image_dataset) / self._timeseries_length))
    # end __len__

    # Get item
    def __getitem__(self, item):
        """
        Get item
        :param item: Item index
        :return: (sample, target)
        """
        # Data and target
        timeseries_data = None
        timeseries_target = None

        # Get samples
        for i in range(self._timeseries_length):
            # Get sample
            sample_data, sample_target = next(self._image_dataset)

            # Concat
            if i == 0:
                timeseries_data = sample_data
                timeseries_target = sample_target
            else:
                timeseries_data = torch.cat((timeseries_data, sample_data), axis=self._time_axis)
                timeseries_target = torch.cat((timeseries_target, sample_data), axis=self._time_axis)
            # end for
        # end for

        return (timeseries_data, timeseries_target)
    # end __getitem__

# end ImageToTimeseries

