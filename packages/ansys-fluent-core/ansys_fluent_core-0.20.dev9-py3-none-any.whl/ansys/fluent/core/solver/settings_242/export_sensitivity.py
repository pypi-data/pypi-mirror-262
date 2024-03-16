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

from .filename_9 import filename as filename_cls
class export_sensitivity(Command):
    """
    Write current data sensitivities to file.
    
    Parameters
    ----------
        filename : str
            Sensitivities file output name.
    
    """

    fluent_name = "export-sensitivity"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

