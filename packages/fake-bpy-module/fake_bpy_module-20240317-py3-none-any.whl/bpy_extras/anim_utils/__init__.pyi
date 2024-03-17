import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def bake_action(
    obj: "bpy.types.Object",
    *,
    action: typing.Optional["bpy.types.Action"],
    frames: int,
    bake_options,
) -> "bpy.types.Action":
    """

        :param obj: Object to bake.
        :type obj: 'bpy.types.Object'
        :param action: An action to bake the data into, or None for a new action
    to be created.
        :type action: typing.Optional['bpy.types.Action']
        :param frames: Frames to bake.
        :type frames: int
        :rtype: 'bpy.types.Action'
        :return: an action or None
    """

    ...

def bake_action_iter(
    obj: "bpy.types.Object",
    *,
    action: typing.Optional["bpy.types.Action"],
    bake_options: typing.Any,
) -> "bpy.types.Action":
    """An coroutine that bakes action for a single object.

        :param obj: Object to bake.
        :type obj: 'bpy.types.Object'
        :param action: An action to bake the data into, or None for a new action
    to be created.
        :type action: typing.Optional['bpy.types.Action']
        :param bake_options: Boolean options of what to include into the action bake.
        :type bake_options: typing.Any
        :rtype: 'bpy.types.Action'
        :return: an action or None
    """

    ...

def bake_action_objects(
    object_action_pairs, *, frames: int, bake_options
) -> typing.Iterable["bpy.types.Action"]:
    """A version of `bake_action_objects_iter` that takes frames and returns the output.

    :param frames: Frames to bake.
    :type frames: int
    :rtype: typing.Iterable['bpy.types.Action']
    :return: A sequence of Action or None types (aligned with object_action_pairs)
    """

    ...

def bake_action_objects_iter(
    object_action_pairs: typing.Union[
        "bpy.types.Action", "bpy.types.Object", "bpy.types.Sequence"
    ],
    bake_options,
):
    """An coroutine that bakes actions for multiple objects.

        :param object_action_pairs: Sequence of object action tuples,
    action is the destination for the baked data. When None a new action will be created.
        :type object_action_pairs: typing.Union['bpy.types.Action', 'bpy.types.Object', 'bpy.types.Sequence']
    """

    ...
