#!/bin/python
import os
import json
from optparse import OptionParser

from blockmeshdictator.blockmeshdictator import return_blockmeshdict

__all__ = ['return_blockmeshdict', 'default_mesh_params']

default_mesh_params = {
    "whole_mesh": False,
    "inner_min": [-3, -2.5, -3],
    "inner_max": [3, 2.5, 3],
    "inner_size": 0.25,
    "outer_min": [-30, -10, -10],
    "outer_max": [15, 10, 10],
    "bottom_cells": 15,
    "bottom_grading": None,
    "top_cells": 15,
    "top_grading": None,
    "side_cells": 20,
    "side_grading": None,
    "inlet_cells": 20,
    "inlet_grading": None,
    "outlet_cells": 45,
    "outlet_grading": None
}

if __name__ == "__main__":
    parser = OptionParser()
    from optparse import OptionParser
    parser.add_option("-f", "--file", dest="filename",
                      help="the input file to user", metavar="FILE")
    parser.add_option("-o", "--out", dest="target",
                      help="")

    options, args = parser.parse_args()
    file_name = options.filename
    if file_name:
        if not os.path.isfile(file_name):
            raise IOError("file not found: {}".format(file_name))
        with open(file_name, 'r') as paramfile:
            mesh_params = json.load(paramfile)
    else:
        mesh_params = default_mesh_params
    print(blockmeshdictator.return_blockmeshdict(mesh_params))