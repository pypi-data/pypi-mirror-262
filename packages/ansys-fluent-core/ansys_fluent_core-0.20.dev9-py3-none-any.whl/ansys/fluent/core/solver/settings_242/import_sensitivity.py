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

from .filename_10 import filename as filename_cls
class import_sensitivity(Command):
    """
    Read sensitivities from data file.
    
    Parameters
    ----------
        filename : str
            Sensitivities file input name.
    
    """

    fluent_name = "import-sensitivity"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

