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
from .surfaces_18 import surfaces as surfaces_cls
class stl_surfaces(Command):
    """
    Export specified surfaces from 3D cases as an .stl file.
    
    Parameters
    ----------
        filename : str
            Export specified surfaces from 3D cases as an .stl file.
        surfaces : typing.List[str]
            Specify surfaces to be exported as .stl file.
    
    """

    fluent_name = "stl-surfaces"

    argument_names = \
        ['filename', 'surfaces']

    _child_classes = dict(
        filename=filename_cls,
        surfaces=surfaces_cls,
    )

