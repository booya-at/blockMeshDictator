from __future__ import division
import os
import jinja2

import scipy.optimize

env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
env.filters.update({
    "floatformat": lambda f: "{: 19.4f}".format(f),
    "fourtimes": lambda s: "{0} {0} {0} {0}".format(s)
})


class BlockmeshDictator(object):
    whole_mesh = False
    inner_size = 0.1

    def __init__(self, inner_min, inner_max, outer_min, outer_max):
        self.inner_min = inner_min
        self.inner_max = inner_max
        self.outer_min = outer_min
        self.outer_max = outer_max

    def get_grading(self, num_blocks, length_total):
        length_center = self.inner_size
        # L=sum(x^i*d_0, {i, 1, num_blocks}) -> sum(x^i) - L/d_0 == 0
        f = lambda x: sum([x ** (i+1) for i in range(num_blocks)]) - length_total / length_center
        return scipy.optimize.newton(f, 1, maxiter=5000)**num_blocks

    @staticmethod
    def get_length(num_blocks, length_center, grading):
        # L=sum(x^i*d_0, {i, 1, num_blocks})
        return sum([grading ** (i + 1) for i in range(num_blocks)]) * length_center

    def get_vertices(self):
        inner_max = self.inner_max
        inner_min = self.inner_min
        outer_max = self.outer_max
        outer_min = self.outer_min

        self.vertices = {
            # min -> max
            # AA--BA--CA
            # |   |   |
            # AB--BB--CB
            # |   |   |
            # AC--BC--CC
            # |   |   |
            # AD--BD--CD

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
        if not self.whole_mesh:
            # TODO: Set inner_max and outer_max y 0
            #mesh_params["inner_max"][1] = 0
            #mesh_params["outer_max"][1] = 0
            pass

        context = {}

        # Vertice-koordinaten berechnen:
        def get_num(i):
            return int((self.inner_max[i] - self.inner_min[i]) // self.inner_size)

        context["inner_num_x"] = get_num(0)
        context["inner_num_y"] = get_num(1)
        context["inner_num_z"] = get_num(2)

        inner_size = context["inner_size"]

        context["bottom_grading"] = self.get_grading(context["bottom_cells"], self.inner_min[2] - self.outer_min[2])
        context["top_grading"] = 1/self.get_grading(context["top_cells"], self.outer_max[2] - self.inner_max[2])

        context["inlet_grading"] = self.get_grading(context["inlet_cells"], self.inner_min[0] - self.outer_min[0])
        context["outlet_grading"] = 1/self.get_grading(context["outlet_cells"], self.outer_max[0] - self.inner_max[0])

        context["side_grading"] = self.get_grading(context["side_cells"], self.outer_max[1] - self.inner_max[1])
        if self.whole_mesh:
            context["side_grading_inv"] = 1/self.get_grading(context["side_cells"], self.inner_min[1] - self.outer_min[1])



        return env.get_template("blockMeshDict").render(vertices=vertices, **mesh_params)



def get_vertices(mesh_params):
    inner_max = mesh_params["inner_max"]
    inner_min = mesh_params["inner_min"]
    outer_max = mesh_params["outer_max"]
    outer_min = mesh_params["outer_min"]


    vertices2 = [
        # Center block
        [inner_max[0], inner_min[1], inner_max[2]],  # V_0
        [inner_min[0], inner_min[1], inner_max[2]],  # V_1
        [inner_min[0], inner_max[1], inner_max[2]],  # V_2
        inner_max,  # V_3
        [inner_max[0], inner_min[1], inner_min[2]],  # V_4
        inner_min,  # V_5
        [inner_min[0], inner_max[1], inner_min[2]],  # V_6
        [inner_max[0], inner_max[1], inner_min[2]],  # V_7

        # center Bottom (+z richtung)
        [inner_max[0], inner_min[1], outer_max[2]],  # V_8
        [inner_min[0], inner_min[1], outer_max[2]],  # V_9
        [inner_min[0], inner_max[1], outer_max[2]],  # V_10
        [inner_max[0], inner_max[1], outer_max[2]],  # V_11

        # center Top (-z richtung)
        [inner_max[0], inner_min[1], outer_min[2]],  # V_12
        [inner_min[0], inner_min[1], outer_min[2]],  # V_13
        [inner_min[0], inner_max[1], outer_min[2]],  # V_14
        [inner_max[0], inner_max[1], outer_min[2]],  # V_15

        # center left (-y richtung)
        [inner_max[0], outer_min[1], inner_max[2]],  # V_16
        [inner_min[0], outer_min[1], inner_max[2]],  # V_17
        [inner_min[0], outer_min[1], inner_min[2]],  # V_18
        [inner_max[0], outer_min[1], inner_min[2]],  # V_19

        # center edge left bottom:
        [inner_max[0], outer_min[1], outer_max[2]],  # V_20
        [inner_min[0], outer_min[1], outer_max[2]],  # V_21

        # center edge left top:
        [inner_max[0], outer_min[1], outer_min[2]],  # V_22
        [inner_min[0], outer_min[1], outer_min[2]],  # V_23

        # center right block (+y richtung)
        [inner_max[0], outer_max[1], inner_max[2]],  # V_24
        [inner_min[0], outer_max[1], inner_max[2]],  # V_25
        [inner_max[0], outer_max[1], inner_min[2]],  # V_26
        [inner_min[0], outer_max[1], inner_min[2]],  # V_27

        # center edge right bottom:
        [inner_max[0], outer_max[1], outer_max[2]],  # V_28
        [inner_min[0], outer_max[1], outer_max[2]],  # V_29

        # center edge right top:
        [inner_max[0], outer_max[1], outer_min[2]],  # V_30
        [inner_min[0], outer_max[1], outer_min[2]],  # V_31

        # outlet center block
        [outer_min[0], inner_max[1], inner_min[2]],  # V_32
        [outer_min[0], inner_max[1], inner_max[2]],  # V_33
        [outer_min[0], inner_min[1], inner_max[2]],  # V_34
        [outer_min[0], inner_min[1], inner_min[2]],  # V_35

        # inlet center block
        [outer_max[0], inner_max[1], inner_min[2]],  # V_36
        [outer_max[0], inner_max[1], inner_max[2]],  # V_37
        [outer_max[0], inner_min[1], inner_min[2]],  # V_38
        [outer_max[0], inner_min[1], inner_max[2]],  # V_39

        # outlet plane
        [outer_min[0], outer_max[1], outer_min[2]],  # V_40
        [outer_min[0], outer_max[1], inner_min[2]],  # V_41
        [outer_min[0], outer_max[1], inner_max[2]],  # V_42
        [outer_min[0], outer_max[1], outer_max[2]],  # V_43
        outer_min,  # V_44
        [outer_min[0], outer_min[1], inner_min[2]],  # V_45
        [outer_min[0], outer_min[1], inner_max[2]],  # V_46
        [outer_min[0], outer_min[1], outer_max[2]],  # V_47
        [outer_min[0], inner_max[1], outer_min[2]],  # V_48
        [outer_min[0], inner_min[1], outer_min[2]],  # V_49
        [outer_min[0], inner_max[1], outer_max[2]],  # V_50
        [outer_min[0], inner_min[1], outer_max[2]],  # V_51

        # inlet plane
        [outer_max[0], outer_max[1], outer_min[2]],  # V_52
        [outer_max[0], outer_max[1], inner_min[2]],  # V_53
        [outer_max[0], outer_max[1], inner_max[2]],  # V_54
        outer_max,  # V_55
        [outer_max[0], outer_min[1], outer_min[2]],  # V_56
        [outer_max[0], outer_min[1], inner_min[2]],  # V_57
        [outer_max[0], outer_min[1], inner_max[2]],  # V_58
        [outer_max[0], outer_min[1], outer_max[2]],  # V_59
        [outer_max[0], inner_max[1], outer_min[2]],  # V_60
        [outer_max[0], inner_min[1], outer_min[2]],  # V_61
        [outer_max[0], inner_max[1], outer_max[2]],  # V_62
        [outer_max[0], inner_min[1], outer_max[2]]  # V_63
    ]

    return vertices


def return_blockmeshdict(mesh_params):
    if not mesh_params["whole_mesh"]:
        mesh_params["inner_max"][1] = 0
        mesh_params["outer_max"][1] = 0

    # Vertice-koordinaten berechnen:
    def get_num(i):
        return int((mesh_params["inner_max"][i] - mesh_params["inner_min"][i]) // mesh_params["inner_size"])

    mesh_params["inner_num_x"] = get_num(0)
    mesh_params["inner_num_y"] = get_num(1)
    mesh_params["inner_num_z"] = get_num(2)

    def auto_grading(keyword_grading, keyword_number, length, inverse=False):
        if mesh_params[keyword_grading] is None and mesh_params[keyword_number] is None:
            raise ValueError("either %s or %s have to be set for auto-grading" % (keyword_grading, keyword_number))
        elif mesh_params[keyword_grading] is None:
            if inverse:
                #print(mesh_params[keyword_number], length)
                mesh_params[keyword_grading] = 1/get_grading(mesh_params[keyword_number], mesh_params["inner_size"], abs(length))
            else:
                mesh_params[keyword_grading] = get_grading(mesh_params[keyword_number], mesh_params["inner_size"], abs(length))
        else:
            raise NotImplementedError("can only auto-grade not auto-cellno")

    auto_grading("bottom_grading", "bottom_cells", mesh_params["outer_max"][2] - mesh_params["inner_max"][2])
    auto_grading("top_grading", "top_cells", mesh_params["inner_max"][2] - mesh_params["outer_max"][2], inverse=True)

    auto_grading("inlet_grading", "inlet_cells", mesh_params["inner_min"][0] - mesh_params["outer_min"][0])
    auto_grading("outlet_grading", "outlet_cells", mesh_params["inner_min"][0] - mesh_params["outer_min"][0], inverse=True)
    auto_grading("side_grading", "side_cells", mesh_params["inner_min"][1] - mesh_params["outer_min"][1], inverse=True)
    mesh_params["side_grading_inv"] = 1/mesh_params["side_grading"]

    vertices = get_vertices(mesh_params)

    return env.get_template("blockMeshDict").render(vertices=vertices, **mesh_params)
