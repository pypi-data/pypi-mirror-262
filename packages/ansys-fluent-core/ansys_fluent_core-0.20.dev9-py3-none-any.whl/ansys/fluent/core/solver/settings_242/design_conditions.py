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

from .selection_1 import selection as selection_cls
from .definition_3 import definition as definition_cls
class design_conditions(Group):
    """
    Design conditions menu.
    """

    fluent_name = "design-conditions"

    child_names = \
        ['selection', 'definition']

    _child_classes = dict(
        selection=selection_cls,
        definition=definition_cls,
    )

