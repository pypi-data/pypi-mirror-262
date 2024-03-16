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

from .filename_12 import filename as filename_cls
class expected_changes(Command):
    """
    Write expected changes to file.
    
    Parameters
    ----------
        filename : str
            Expected changes report name.
    
    """

    fluent_name = "expected-changes"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

