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

from .filename_13 import filename as filename_cls
class export_displacements(Command):
    """
    Export the total computed optimal displacements.
    
    Parameters
    ----------
        filename : str
            Displacements file name.
    
    """

    fluent_name = "export-displacements"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

