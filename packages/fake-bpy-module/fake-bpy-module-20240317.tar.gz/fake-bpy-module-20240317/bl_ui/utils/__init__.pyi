import typing

GenericType = typing.TypeVar("GenericType")

class PresetPanel:
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_space_type: typing.Any

    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_menu(self, layout, text):
        """

        :param layout:
        :type layout:
        :param text:
        :type text:
        """
        ...

    def draw_panel_header(self, layout):
        """

        :param layout:
        :type layout:
        """
        ...

    def path_menu(
        self,
        searchpaths,
        operator,
        props_default,
        prop_filepath,
        filter_ext,
        filter_path,
        display_name,
        add_operator,
    ):
        """

        :param self:
        :type self:
        :param searchpaths:
        :type searchpaths:
        :param operator:
        :type operator:
        :param props_default:
        :type props_default:
        :param prop_filepath:
        :type prop_filepath:
        :param filter_ext:
        :type filter_ext:
        :param filter_path:
        :type filter_path:
        :param display_name:
        :type display_name:
        :param add_operator:
        :type add_operator:
        """
        ...
