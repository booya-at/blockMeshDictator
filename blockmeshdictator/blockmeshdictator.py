from __future__ import division
import os
import jinja2

import scipy.optimize

defaults = {
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

class BlockmeshDictator(object):
    whole_mesh = False
    inner_size = 0.25
    bottom_cells = 15
    top_cells = 15
    side_cells = 10
    inlet_cells = 20
    outlet_cells = 30

    def __init__(self, inner_min, inner_max, outer_min, outer_max):
        self.inner_min = inner_min
        self.inner_max = inner_max
        self.outer_min = outer_min
        self.outer_max = outer_max

        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
        self.env.filters.update({
            "f": lambda f: "{:.4f}".format(f),
            "f2": lambda f: "{: 10.4f}".format(f),
            "fourtimes": lambda s: "{0} {0} {0} {0}".format(s)
        })

    def get_grading(self, num_blocks, length_total):
        length_center = self.inner_size
        # L=sum(x^i*d_0, {i, 1, num_blocks}) -> sum(x^i) - L/d_0 == 0
        f = lambda x: sum([x ** (i+1) for i in range(num_blocks)]) - length_total / length_center
        res = scipy.optimize.newton(f, 1, maxiter=50000)**num_blocks
        return res

    @staticmethod
    def get_length(num_blocks, length_center, grading):
        # L=sum(x^i*d_0, {i, 1, num_blocks})
        return sum([grading ** (i + 1) for i in range(num_blocks)]) * length_center

    def get_vertices(self):
        inner_max = self.inner_max
        inner_min = self.inner_min
        outer_max = self.outer_max
        outer_min = self.outer_min

        self.vertices = {#  CBD--DBD
            # Xmin -> max  /    /|
            # AAD--BAD--CAD--DAD DBC
            # |    |    |  / |  /|
            # AAC--BAC--CAC--DAC DBB
            # |    |    |  / |  /|
            # AAB--BAB--CAB--DAB DBA
            # |    |    |  / |  /
            # AAA--BAA--CAA--DAA

            "AAA": (outer_min[0], outer_min[1], outer_min[2]),
            "AAB": (outer_min[0], outer_min[1], inner_min[2]),
            "AAC": (outer_min[0], outer_min[1], inner_max[2]),
            "AAD": (outer_min[0], outer_min[1], outer_max[2]),

            "ABA": (outer_min[0], inner_min[1], outer_min[2]),
            "ABB": (outer_min[0], inner_min[1], inner_min[2]),
            "ABC": (outer_min[0], inner_min[1], inner_max[2]),
            "ABD": (outer_min[0], inner_min[1], outer_max[2]),

            "ACA": (outer_min[0], inner_max[1], outer_min[2]),
            "ACB": (outer_min[0], inner_max[1], inner_min[2]),
            "ACC": (outer_min[0], inner_max[1], inner_max[2]),
            "ACD": (outer_min[0], inner_max[1], outer_max[2]),

            "ADA": (outer_min[0], outer_max[1], outer_min[2]),
            "ADB": (outer_min[0], outer_max[1], inner_min[2]),
            "ADC": (outer_min[0], outer_max[1], inner_max[2]),
            "ADD": (outer_min[0], outer_max[1], outer_max[2]),

            "BAA": (inner_min[0], outer_min[1], outer_min[2]),
            "BAB": (inner_min[0], outer_min[1], inner_min[2]),
            "BAC": (inner_min[0], outer_min[1], inner_max[2]),
            "BAD": (inner_min[0], outer_min[1], outer_max[2]),

            "BBA": (inner_min[0], inner_min[1], outer_min[2]),
            "BBB": (inner_min[0], inner_min[1], inner_min[2]),
            "BBC": (inner_min[0], inner_min[1], inner_max[2]),
            "BBD": (inner_min[0], inner_min[1], outer_max[2]),

            "BCA": (inner_min[0], inner_max[1], outer_min[2]),
            "BCB": (inner_min[0], inner_max[1], inner_min[2]),
            "BCC": (inner_min[0], inner_max[1], inner_max[2]),
            "BCD": (inner_min[0], inner_max[1], outer_max[2]),

            "BDA": (inner_min[0], outer_max[1], outer_min[2]),
            "BDB": (inner_min[0], outer_max[1], inner_min[2]),
            "BDC": (inner_min[0], outer_max[1], inner_max[2]),
            "BDD": (inner_min[0], outer_max[1], outer_max[2]),

            "CAA": (inner_max[0], outer_min[1], outer_min[2]),
            "CAB": (inner_max[0], outer_min[1], inner_min[2]),
            "CAC": (inner_max[0], outer_min[1], inner_max[2]),
            "CAD": (inner_max[0], outer_min[1], outer_max[2]),

            "CBA": (inner_max[0], inner_min[1], outer_min[2]),
            "CBB": (inner_max[0], inner_min[1], inner_min[2]),
            "CBC": (inner_max[0], inner_min[1], inner_max[2]),
            "CBD": (inner_max[0], inner_min[1], outer_max[2]),

            "CCA": (inner_max[0], inner_max[1], outer_min[2]),
            "CCB": (inner_max[0], inner_max[1], inner_min[2]),
            "CCC": (inner_max[0], inner_max[1], inner_max[2]),
            "CCD": (inner_max[0], inner_max[1], outer_max[2]),

            "CDA": (inner_max[0], outer_max[1], outer_min[2]),
            "CDB": (inner_max[0], outer_max[1], inner_min[2]),
            "CDC": (inner_max[0], outer_max[1], inner_max[2]),
            "CDD": (inner_max[0], outer_max[1], outer_max[2]),

            "DAA": (outer_max[0], outer_min[1], outer_min[2]),
            "DAB": (outer_max[0], outer_min[1], inner_min[2]),
            "DAC": (outer_max[0], outer_min[1], inner_max[2]),
            "DAD": (outer_max[0], outer_min[1], outer_max[2]),

            "DBA": (outer_max[0], inner_min[1], outer_min[2]),
            "DBB": (outer_max[0], inner_min[1], inner_min[2]),
            "DBC": (outer_max[0], inner_min[1], inner_max[2]),
            "DBD": (outer_max[0], inner_min[1], outer_max[2]),

            "DCA": (outer_max[0], inner_max[1], outer_min[2]),
            "DCB": (outer_max[0], inner_max[1], inner_min[2]),
            "DCC": (outer_max[0], inner_max[1], inner_max[2]),
            "DCD": (outer_max[0], inner_max[1], outer_max[2]),

            "DDA": (outer_max[0], outer_max[1], outer_min[2]),
            "DDB": (outer_max[0], outer_max[1], inner_min[2]),
            "DDC": (outer_max[0], outer_max[1], inner_max[2]),
            "DDD": (outer_max[0], outer_max[1], outer_max[2]),
        }

        return self.vertices


    def get_blockmeshdict(self):
        context = {
            "inner_size": self.inner_size,
            "inner_min": self.inner_min,
            "inner_max": self.inner_max,
            "outer_min": self.outer_min,
            "outer_max": self.outer_max,
            "whole_mesh": self.whole_mesh,
            "bottom_cells": self.bottom_cells,
            "top_cells": self.top_cells,
            "side_cells": self.side_cells,
            "inlet_cells": self.inlet_cells,
            "outlet_cells": self.outlet_cells
        }

        if not self.whole_mesh:
            # TODO: Set inner_max and outer_max y 0
            context["inner_min"][1] = 0
            context["outer_min"][1] = 0


        # Vertice-koordinaten berechnen:
        def get_num(i):
            return int((self.inner_max[i] - self.inner_min[i]) // self.inner_size)

        context["inner_num_x"] = get_num(0)
        context["inner_num_y"] = get_num(1)
        context["inner_num_z"] = get_num(2)

        context["bottom_grading"] = 1/self.get_grading(context["bottom_cells"], self.inner_min[2] - self.outer_min[2])
        context["top_grading"] = self.get_grading(context["top_cells"], self.outer_max[2] - self.inner_max[2])

        context["inlet_grading"] = 1/self.get_grading(context["inlet_cells"], self.inner_min[0] - self.outer_min[0])
        context["outlet_grading"] = self.get_grading(context["outlet_cells"], self.outer_max[0] - self.inner_max[0])

        context["side_grading"] = self.get_grading(context["side_cells"], self.outer_max[1] - self.inner_max[1])

        if self.whole_mesh:
            context["side_grading_inv"] = 1/self.get_grading(context["side_cells"], self.inner_min[1] - self.outer_min[1])

        ids = {}
        vertices = []
        for i, (key, vertex) in enumerate(self.get_vertices().items()):
            ids[key] = i
            vertices.append(vertex)

        def get_vertex_ids(string: str):
            vertice_names = string.split(" ")
            vertice_ids = ["{: 2}".format(ids[key]) for key in vertice_names]
            return " ".join(vertice_ids)

        self.env.filters.update({
            "node_ids": get_vertex_ids
        })


        return self.env.get_template("new").render(vertices=vertices, **context)