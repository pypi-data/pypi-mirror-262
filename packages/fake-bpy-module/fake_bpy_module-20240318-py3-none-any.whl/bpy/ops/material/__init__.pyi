import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def copy(
    override_context: typing.Optional[
        typing.Union["bpy.types.Context", typing.Dict]
    ] = None,
    execution_context: typing.Optional[typing.Union[int, str]] = None,
    undo: typing.Optional[bool] = None,
):
    """Copy the material settings and nodes

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def new(
    override_context: typing.Optional[
        typing.Union["bpy.types.Context", typing.Dict]
    ] = None,
    execution_context: typing.Optional[typing.Union[int, str]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add a new material

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def paste(
    override_context: typing.Optional[
        typing.Union["bpy.types.Context", typing.Dict]
    ] = None,
    execution_context: typing.Optional[typing.Union[int, str]] = None,
    undo: typing.Optional[bool] = None,
):
    """Paste the material settings and nodes

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
