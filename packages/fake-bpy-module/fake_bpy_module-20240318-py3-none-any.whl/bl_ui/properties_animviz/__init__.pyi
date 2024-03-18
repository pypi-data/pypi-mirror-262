import typing

GenericType = typing.TypeVar("GenericType")

class MotionPathButtonsPanel:
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_space_type: typing.Any

    def draw_settings(self, _context, avs, mpath, bones):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        :param avs:
        :type avs:
        :param mpath:
        :type mpath:
        :param bones:
        :type bones:
        """
        ...

class MotionPathButtonsPanel_display:
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_space_type: typing.Any

    def draw_settings(self, _context, avs, mpath, bones):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        :param avs:
        :type avs:
        :param mpath:
        :type mpath:
        :param bones:
        :type bones:
        """
        ...
