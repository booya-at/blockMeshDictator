from __future__ import division
import json
import os
from optparse import OptionParser

import scipy.optimize

__all__ = ['return_blockmeshdict']

def get_grading(num_blocks, length_center, length_total):
    # L=sum(x^i*d_0, {i, 1, num_blocks}) -> sum(x^i) - L/d_0 == 0
    f = lambda x: sum([x ** (i+1) for i in range(num_blocks)]) - length_total / length_center
    return scipy.optimize.newton(f, 1, maxiter=5000)**num_blocks


def get_length(num_blocks, length_center, grading):
    # L=sum(x^i*d_0, {i, 1, num_blocks})
    return sum([grading ** (i + 1) for i in range(num_blocks)]) * length_center


def return_blockmeshdict(mesh_params):
    if not mesh_params["whole_mesh"]:
        mesh_params["inner_max"][1] = 0
        mesh_params["outer_max"][1] = 0

    # Vertice-koordinaten berechnen:
    mesh_params["inner_num_x"], mesh_params["inner_num_y"], mesh_params["inner_num_z"] = \
        [int((mesh_params["inner_max"][i] - mesh_params["inner_min"][i]) // mesh_params["inner_size"]) for i in
         range(3)]

    inner_max = mesh_params["inner_max"]
    inner_min = mesh_params["inner_min"]
    outer_max = mesh_params["outer_max"]
    outer_min = mesh_params["outer_min"]

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

    # Header
    blockmeshdict = """\
/*--------------------------------*- C++ -*----------------------------------*
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  2.1.0                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.com                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

convertToMeters 1;

vertices
(
"""

    # Vertices
    for i, vertex in enumerate(vertices):
        blockmeshdict += "\t( {}\t\t{}\t\t{} )\t// {}\n".format(*(vertex + [i]))

    # Blocks

    blockmeshdict += """\
);

blocks
(
    //Center Blocks
    hex (0 1 2 3 4 5 6 7) ( %(inner_num_x)s %(inner_num_y)s %(inner_num_z)s ) \
edgeGrading ( 1 1 1 1 1 1 1 1 1 1 1 1) // 0: Center Block
    hex (8 9 10 11 0 1 2 3) ( %(inner_num_x)s %(inner_num_y)s %(bottom_num)s ) \
edgeGrading ( 1 1 1 1 1 1 1 1 %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s ) //1: Center Cross Bottom
    hex (4 5 6 7 12 13 14 15) ( %(inner_num_x)s %(inner_num_y)s %(top_num)s ) \
edgeGrading ( 1 1 1 1 1 1 1 1 %(top_grading)s %(top_grading)s %(top_grading)s %(top_grading)s ) //2: Center Cross Top
    hex (16 17 1 0 19 18 5 4) ( %(inner_num_x)s %(side_num)s %(inner_num_z)s ) \
edgeGrading ( 1 1 1 1 %(side_grading)s %(side_grading)s %(side_grading)s %(side_grading)s 1 1 1 1 ) //3: Center Cross Left
    """ % mesh_params

    if mesh_params["whole_mesh"]:
        blockmeshdict += """\
hex (3 2 25 24 7 6 27 26) ( %(inner_num_x)s %(side_num)s %(inner_num_z)s ) \
edgeGrading (1 1 1 1 %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s 1 1 1 1) //4: center cross right
    """ % mesh_params

    blockmeshdict += """
    hex (20 21 9 8 16 17 1 0) ( %(inner_num_x)s %(side_num)s %(bottom_num)s ) edgeGrading (1 1 1 1 %(side_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s )  //5
    hex (19 18 5 4 22 23 13 12)  ( %(inner_num_x)s %(side_num)s %(top_num)s )  edgeGrading (1 1 1 1 %(side_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(top_grading)s %(top_grading)s %(top_grading)s %(top_grading)s )  //6
    """ % mesh_params

    if mesh_params["whole_mesh"]:
        blockmeshdict += """
    hex (11 10 29 28 3 2 25 24) ( %(inner_num_x)s %(side_num)s %(bottom_num)s ) edgeGrading ( 1 1 1 1 %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s ) //7: Center Block Right Top Edge
    hex (7 6 27 26 15 14 31 30) ( %(inner_num_x)s %(side_num)s  %(top_num)s ) edgeGrading (1 1 1 1 %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(top_grading)s %(top_grading)s %(top_grading)s %(top_grading)s )    //8
    """ % mesh_params

    blockmeshdict += """
    hex (1 34 33 2 5 35 32 6) ( %(outlet_num)s %(inner_num_y)s %(inner_num_z)s ) edgeGrading ( %(outlet_grading)s %(outlet_grading)s %(outlet_grading)s %(outlet_grading)s 1 1 1 1 1 1 1 1)   //9: max x center outlet
    hex (39 0 3 37 38 4 7 36) ( %(inlet_num)s %(inner_num_y)s %(inner_num_z)s ) edgeGrading ( %(inlet_grading)s %(inlet_grading)s %(inlet_grading)s %(inlet_grading)s 1 1 1 1 1 1 1 1)   //10: min x center outlet
    """ % mesh_params

    if mesh_params["whole_mesh"]:
        blockmeshdict += """
    hex (2 33 42 25 6 32 41 27) ( %(outlet_num)s %(side_num)s %(inner_num_z)s ) edgeGrading ( %(outlet_grading)s %(outlet_grading)s %(outlet_grading)s %(outlet_grading)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s 1 1 1 1)  //11: max x Cross right\
    """ % mesh_params

    blockmeshdict += """
    hex (17 46 34 1 18 45 35 5) ( %(outlet_num)s %(side_num)s %(inner_num_z)s ) edgeGrading ( %(outlet_grading)s %(outlet_grading)s %(outlet_grading)s %(outlet_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(side_grading)s 1 1 1 1)	//12: max x Cross Links
    hex (9 51 50 10 1 34 33 2) (  %(outlet_num)s  %(inner_num_y)s %(bottom_num)s ) edgeGrading (  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s 1 1 1 1 %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s ) //13: max x Cross Bottom
    hex (5 35 32 6 13 49 48 14) (  %(outlet_num)s  %(inner_num_y)s  %(top_num)s ) edgeGrading (  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s 1 1 1 1 %(top_grading)s %(top_grading)s %(top_grading)s %(top_grading)s )   //14: max x Cross Top

    //max Edge blocks""" % mesh_params

    if mesh_params["whole_mesh"]:
        blockmeshdict += """
    hex (6 32 41 27 14 48 40 31) (  %(outlet_num)s %(side_num)s  %(top_num)s ) edgeGrading (  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s  %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(top_grading)s %(top_grading)s %(top_grading)s %(top_grading)s )   //15\
    """ % mesh_params

    blockmeshdict += """
    hex (18 45 35 5 23 44 49 13) (  %(outlet_num)s %(side_num)s  %(top_num)s ) edgeGrading (  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(top_grading)s %(top_grading)s %(top_grading)s %(top_grading)s )    //16
    hex (21 47 51 9 17 46 34 1) (  %(outlet_num)s %(side_num)s %(bottom_num)s ) edgeGrading (  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s )   //17
    """ % mesh_params

    if mesh_params["whole_mesh"]:
        blockmeshdict += """hex (10 50 43 29 2 33 42 25) (  %(outlet_num)s %(side_num)s %(bottom_num)s ) edgeGrading (  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s  %(outlet_grading)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s )	//18
    """ % mesh_params

    blockmeshdict += """\
    //***********************************************************

    //min x Blocks"
    """

    if mesh_params["whole_mesh"]:
        # Inlet Right Block
        blockmeshdict += """
    hex (37 3 24 54 36 7 26 53) (  %(inlet_num)s %(side_num)s  %(inner_num_z)s ) edgeGrading (  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s 1 1 1 1 )    //19: min x Cross Right\
    """ % mesh_params

    blockmeshdict += """
    hex (58 16 0 39 57 19 4 38) (  %(inlet_num)s %(side_num)s  %(inner_num_z)s ) edgeGrading (  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(side_grading)s 1 1 1 1) //20: min x Cross Left
    hex (63 8 11 62 39 0 3 37) (  %(inlet_num)s  %(inner_num_y)s %(bottom_num)s ) edgeGrading (  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s 1 1 1 1 %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s)    //21: min x Cross Bottom
    hex (38 4 7 36 61 12 15 60) (  %(inlet_num)s  %(inner_num_y)s  %(top_num)s ) edgeGrading (  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s 1 1 1 1 %(top_grading)s %(top_grading)s %(top_grading)s %(top_grading)s )   //22: min x Cross Top


    //min x edge blocks"
    """ % mesh_params

    if mesh_params["whole_mesh"]:
        blockmeshdict += """
    hex (36 7 26 53 60 15 30 52) ( %(inlet_num)s %(side_num)s  %(top_num)s ) edgeGrading (  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(top_grading)s %(top_grading)s %(top_grading)s %(top_grading)s )  //23
    """ % mesh_params

    blockmeshdict += """
    hex (57 19 4 38 56 22 12 61) (  %(inlet_num)s %(side_num)s  %(top_num)s ) edgeGrading (  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(top_grading)s %(top_grading)s %(top_grading)s %(top_grading)s ) //24
    hex (59 20 8 63 58 16 0 39) (  %(inlet_num)s %(side_num)s %(bottom_num)s ) edgeGrading (  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(side_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s )  //25
    """ % mesh_params

    if mesh_params["whole_mesh"]:
        blockmeshdict += """
    hex (62 11 28 55 37 3 24 54) (  %(inlet_num)s %(side_num)s %(bottom_num)s ) edgeGrading (  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s  %(inlet_grading)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(side_grading_inv)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s %(bottom_grading)s)    //26
    """ % mesh_params

    blockmeshdict += """
);
edges
(
);
boundary
(
    inlet
    {
        type patch;
        faces
        ("""

    if mesh_params["whole_mesh"]:
        blockmeshdict += """
            (60 36 53 52)
            (36 37 54 53)
            (37 62 55 54)"""

    blockmeshdict += """
            (61 38 36 60)
            (38 39 37 36)
            (39 63 62 37)
            (56 57 38 61)
            (57 58 39 38)
            (58 59 63 39)
        );
    }
    outlet
    {
        type patch;
        faces
        ("""

    if mesh_params["whole_mesh"]:
        blockmeshdict += """
            (48 32 41 40)
            (32 33 42 41)
            (33 50 43 42)"""

    blockmeshdict += """
            (49 35 32 48)
            (35 34 33 32)
            (34 51 50 33)
            (44 45 35 49)
            (45 46 34 35)
            (46 47 51 34)
        );
    }
    frontAndBack
    {
        type patch;
        faces
        (
            (56 22 19 57)
            (22 23 18 19)
            (23 44 45 18)
            (57 19 16 58)
            (19 18 17 16)
            (18 45 46 17)
            (58 16 20 59)
            (16 17 21 20)
            (17 46 47 21)"""

    if mesh_params["whole_mesh"]:
        blockmeshdict += """
            (52 30 26 53)
            (30 31 27 26)
            (31 40 41 27)
            (53 26 24 54)
            (26 27 25 24)
            (27 41 42 25)
            (54 24 28 55)
            (24 25 29 28)
            (25 42 43 29)"""
    else:
        blockmeshdict += """
            (60 15 7 36)
            (15 14 6 7)
            (14 48 32 6)
            (36 7 3 37)
            (7 6 2 3)
            (6 32 33 2)
            (37 3 11 62)
            (3 2 10 11)
            (2 33 50 10)"""

    blockmeshdict += """
        );
    }
    lowerWall
    {
        type patch;
        faces
        ("""

    if mesh_params["whole_mesh"]:
        blockmeshdict += """
            (55 62 11 28)
            (28 11 10 29)
            (29 10 50 43)"""

    blockmeshdict += """
            (62 63 8 11)
            (11 8 9 10)
            (10 9 51 50)
            (63 59 20 8)
            (8 20 21 9)
            (9 21 47 51)
        );
    }
    upperWall
    {
        type patch;
        faces
        ("""

    if mesh_params["whole_mesh"]:
        blockmeshdict += """
            (52 60 15 30)
            (30 15 14 31)
            (31 14 48 40)"""

    blockmeshdict += """
            (60 61 12 15)
            (15 12 13 14)
            (14 13 49 48)
            (61 56 22 12)
            (12 22 23 13)
            (13 23 44 49)
        );
    }
);
// ************************************************************************* //
"""

    return blockmeshdict


if __name__ == "__main__":
    parser = OptionParser()
    from optparse import OptionParser
    parser.add_option("-f", "--file", dest="filename",
                  help="the input file to user", metavar="FILE")
    parser.add_option("-o", "--out", dest="target",
                      help="")

    options, args = parser.parse_args()
    file_name = options.filename or "mesh_params.json"
    if not os.path.isfile(file_name):
        raise IOError("file not found: {}".format(file_name))
    with open(file_name, 'r') as paramfile:
        mesh_params = json.load(paramfile)
    print(return_blockmeshdict(mesh_params))