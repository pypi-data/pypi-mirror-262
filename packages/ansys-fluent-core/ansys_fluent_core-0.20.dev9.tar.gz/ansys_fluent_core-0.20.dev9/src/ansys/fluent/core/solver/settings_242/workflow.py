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

from .results_1 import results as results_cls
from .export_2 import export as export_cls
from .check_1 import check as check_cls
from .calculate_design_change import calculate_design_change as calculate_design_change_cls
from .modify import modify as modify_cls
from .revert import revert as revert_cls
from .remesh import remesh as remesh_cls
class workflow(Group):
    """
    Design tool workflow menu.
    """

    fluent_name = "workflow"

    child_names = \
        ['results', 'export']

    command_names = \
        ['check', 'calculate_design_change', 'modify', 'revert', 'remesh']

    _child_classes = dict(
        results=results_cls,
        export=export_cls,
        check=check_cls,
        calculate_design_change=calculate_design_change_cls,
        modify=modify_cls,
        revert=revert_cls,
        remesh=remesh_cls,
    )

