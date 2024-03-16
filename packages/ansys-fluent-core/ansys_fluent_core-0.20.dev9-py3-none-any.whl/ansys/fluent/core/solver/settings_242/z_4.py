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

from .points import points as points_cls
from .motion_enabled import motion_enabled as motion_enabled_cls
from .invariant import invariant as invariant_cls
from .symmetric import symmetric as symmetric_cls
from .periodicity_1 import periodicity as periodicity_cls
class z(Group):
    """
    Region conditions in the Z direction.
    """

    fluent_name = "z"

    child_names = \
        ['points', 'motion_enabled', 'invariant', 'symmetric', 'periodicity']

    _child_classes = dict(
        points=points_cls,
        motion_enabled=motion_enabled_cls,
        invariant=invariant_cls,
        symmetric=symmetric_cls,
        periodicity=periodicity_cls,
    )

