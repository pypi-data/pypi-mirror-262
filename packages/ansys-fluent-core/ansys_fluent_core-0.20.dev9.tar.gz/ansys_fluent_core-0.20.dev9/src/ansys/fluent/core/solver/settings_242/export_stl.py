#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .filename_14 import filename as filename_cls
class export_stl(Command):
    """
    Export specified surfaces from as an .stl file.
    
    Parameters
    ----------
        filename : str
            Export specified surfaces from 3D cases as an .stl file.
    
    """

    fluent_name = "export-stl"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

