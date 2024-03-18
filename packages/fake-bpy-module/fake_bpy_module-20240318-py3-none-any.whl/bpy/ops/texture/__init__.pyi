import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def new(
    override_context: typing.Optional[
        typing.Union["bpy.types.Context", typing.Dict]
    ] = None,
    execution_context: typing.Optional[typing.Union[int, str]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add a new texture

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def slot_copy(
    override_context: typing.Optional[
        typing.Union["bpy.types.Context", typing.Dict]
    ] = None,
    execution_context: typing.Optional[typing.Union[int, str]] = None,
    undo: typing.Optional[bool] = None,
):
    """Copy the material texture settings and nodes

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...

def slot_move(
    override_context: typing.Optional[
        typing.Union["bpy.types.Context", typing.Dict]
    ] = None,
    execution_context: typing.Optional[typing.Union[int, str]] = None,
    undo: typing.Optional[bool] = None,
    *,
    type: typing.Optional[typing.Any] = "UP",
):
    """Move texture slots up and down

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    :param type: Type
    :type type: typing.Optional[typing.Any]
    """

    ...

def slot_paste(
    override_context: typing.Optional[
        typing.Union["bpy.types.Context", typing.Dict]
    ] = None,
    execution_context: typing.Optional[typing.Union[int, str]] = None,
    undo: typing.Optional[bool] = None,
):
    """Copy the texture settings and nodes

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
