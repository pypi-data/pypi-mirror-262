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
    """Create a new world Data-Block

    :type override_context: typing.Optional[typing.Union['bpy.types.Context', typing.Dict]]
    :type execution_context: typing.Optional[typing.Union[int, str]]
    :type undo: typing.Optional[bool]
    """

    ...
