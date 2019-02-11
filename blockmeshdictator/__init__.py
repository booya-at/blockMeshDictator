#!/bin/python
import os
import json
from optparse import OptionParser

from blockmeshdictator.blockmeshdictator import BlockmeshDictator

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