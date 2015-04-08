from __future__ import division
import os
import jinja2

import scipy.optimize

env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
env.filters.update({
    "floatformat": lambda f: "{: 19}".format(f)
})


def get_grading(num_blocks, length_center, length_total):
    # L=sum(x^i*d_0, {i, 1, num_blocks}) -> sum(x^i) - L/d_0 == 0
    f = lambda x: sum([x ** (i+1) for i in range(num_blocks)]) - length_total / length_center
    return scipy.optimize.newton(f, 1, maxiter=5000)**num_blocks


def get_length(num_blocks, length_center, grading):
    # L=sum(x^i*d_0, {i, 1, num_blocks})
    return sum([grading ** (i + 1) for i in range(num_blocks)]) * length_center


def get_vertices(mesh_params):
    inner_max = mesh_params["inner_max"]
    inner_min = mesh_params["inner_min"]
    outer_max = mesh_params["outer_max"]
    outer_min = mesh_params["outer_min"]

    vertices = [
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
    mesh_params["inner_num_x"], mesh_params["inner_num_y"], mesh_params["inner_num_z"] = \
        [int((mesh_params["inner_max"][i] - mesh_params["inner_min"][i]) // mesh_params["inner_size"]) for i in
         range(3)]

    def auto_grading(keyword_grading, keyword_number, length, inverse=False):
        if mesh_params[keyword_grading] is None and mesh_params[keyword_number] is None:
            raise ValueError("either %s or %s have to be set for auto-grading" % (keyword_grading, keyword_number))
        elif mesh_params[keyword_grading] is None:
            if inverse:
                #print(mesh_params[keyword_number], length)
                mesh_params[keyword_grading] = 1/get_grading(mesh_params[keyword_number], mesh_params["inner_size"], length)
            else:
                mesh_params[keyword_grading] = get_grading(mesh_params[keyword_number], mesh_params["inner_size"], length)

    auto_grading("bottom_grading", "bottom_num", mesh_params["outer_max"][2] - mesh_params["inner_max"][2], inverse=True)
    auto_grading("top_grading", "top_num", mesh_params["inner_min"][2] - mesh_params["outer_min"][2])
    auto_grading("side_grading", "side_num", - mesh_params["outer_min"][1] + mesh_params["inner_min"][1], inverse=True)
    auto_grading("inlet_grading", "inlet_num", mesh_params["outer_max"][0] - mesh_params["inner_max"][0], inverse=True)
    auto_grading("outlet_grading", "outlet_num", mesh_params["inner_min"][0] - mesh_params["outer_min"][0])
    auto_grading("side_grading", "side_num", mesh_params["inner_min"][1] - mesh_params["outer_min"][1], inverse=True)
    mesh_params["side_grading_inv"] = 1/mesh_params["side_grading"]

    vertices = get_vertices(mesh_params)

    return env.get_template("blockMeshDict").render(vertices=vertices, **mesh_params)