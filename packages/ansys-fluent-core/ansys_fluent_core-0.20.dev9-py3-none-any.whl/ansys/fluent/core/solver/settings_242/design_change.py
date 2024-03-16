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

from .parameters_4 import parameters as parameters_cls
from .workflow import workflow as workflow_cls
from .preview_1 import preview as preview_cls
from .history import history as history_cls
class design_change(Group):
    """
    Design change menu.
    """

    fluent_name = "design-change"

    child_names = \
        ['parameters', 'workflow', 'preview', 'history']

    _child_classes = dict(
        parameters=parameters_cls,
        workflow=workflow_cls,
        preview=preview_cls,
        history=history_cls,
    )

