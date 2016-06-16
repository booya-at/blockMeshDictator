BlockMeshDictator
=================

![Dictator](chaplin.jpg)

This is a script to create a simple blockMeshDict from a few parameters
specified in a json file.
It derives from an anonymous donation in c++ which i transscripted to python
to be easier to handle.

It takes as input a very simple json-file with the following structure:

```
{
    "whole_mesh": false,
    "inner_min": [-3, -2.5, -3],
    "inner_max": [3, 2.5, 3],
    "inner_size": 0.25,
    "outer_min": [-30, -10, -10],
    "outer_max": [15, 10, 10],
    "bottom_num": 15,
    "bottom_grading": null,
    "top_num": 15,
    "top_grading": null,
    "side_num": 20,
    "side_grading": null,
    "inlet_num": 20,
    "inlet_grading": null,
    "outlet_num": 45,
    "outlet_grading": null
}
```

Whereas the parameters define the following:

    - whole_mesh: if false, create only half the mesh, cut along the x/z layer
    - inner_min/inner_max: cornerpoints of the inner box
    - inner_size: size of inner-box blocks
    - outer_min/outer_max: cornerpoints of the outer box
    - *_num: number of blocks for the side
    - *_grading: the grading to use for the side (defaults to auto-grading)