bpyCAD
=================================
Python CAD library using Blender's bpy

This codebase provides a Python script for generating CAD models from Blender's bpy API.
The aim is to provide the same functionality as CadQuery, OpenSCAD, and other programmatic CAD.

Installation
------------

From Pip
^^^^^^^^

.. code-block:: console

    $ pip install bpycad

From Source
^^^^^^^^^^^

.. code-block:: console

    $ git clone https://github.com/simleek/bpyCAD.git
    $ cd bpyCAD
    $ pip install -r requirements.txt
    $ pip install -r requirements_dev.txt
    $ pip install -e .

Usage
-----

To use the CAD generator script, first open the Blender scene that you want to generate CAD files for. Then, in the Blender Text Editor, open the `cad_generator.py` script and run it. The script will prompt you to specify the output file format and location.

Once you have specified the output file format and location, the script will generate the CAD file and save it to the specified location.

Supported File Formats
----------------------

Currently supported:

- None

Future Support:
- STL (.stl)
- OBJ (.obj)
- STEP (.step)

License
-------

This codebase is released under the MIT License. See `LICENSE` for more information.

Contributing
------------

Contributions to this project are welcome. To contribute, please fork this repository, make your changes, and submit a pull request.

Contact
-------

If you have any questions or issues with this script, please feel free to contact SimLeek
