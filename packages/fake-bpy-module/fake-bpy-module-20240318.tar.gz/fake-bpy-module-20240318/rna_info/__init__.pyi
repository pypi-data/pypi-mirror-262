import typing

GenericType = typing.TypeVar("GenericType")

class InfoFunctionRNA:
    args: typing.Any
    bl_func: typing.Any
    description: typing.Any
    global_lookup: typing.Any
    identifier: typing.Any
    is_classmethod: typing.Any
    return_values: typing.Any

    def build(self):
        """

        :param self:
        :type self:
        """
        ...

class InfoOperatorRNA:
    args: typing.Any
    bl_op: typing.Any
    description: typing.Any
    func_name: typing.Any
    global_lookup: typing.Any
    identifier: typing.Any
    module_name: typing.Any
    name: typing.Any

    def build(self):
        """

        :param self:
        :type self:
        """
        ...

    def get_location(self):
        """

        :param self:
        :type self:
        """
        ...

class InfoPropertyRNA:
    array_dimensions: typing.Any
    array_length: typing.Any
    bl_prop: typing.Any
    collection_type: typing.Any
    default: typing.Any
    default_str: typing.Any
    description: typing.Any
    enum_items: typing.Any
    enum_pointer: typing.Any
    fixed_type: typing.Any
    global_lookup: typing.Any
    identifier: typing.Any
    is_argument_optional: typing.Any
    is_enum_flag: typing.Any
    is_never_none: typing.Any
    is_readonly: typing.Any
    is_required: typing.Any
    max: typing.Any
    min: typing.Any
    name: typing.Any
    srna: typing.Any
    subtype: typing.Any
    type: typing.Any

    def build(self):
        """

        :param self:
        :type self:
        """
        ...

    def get_arg_default(self, force):
        """

        :param self:
        :type self:
        :param force:
        :type force:
        """
        ...

    def get_type_description(
        self,
        as_ret,
        as_arg,
        class_fmt,
        mathutils_fmt,
        collection_id,
        enum_descr_override,
    ):
        """

        :param self:
        :type self:
        :param as_ret:
        :type as_ret:
        :param as_arg:
        :type as_arg:
        :param class_fmt:
        :type class_fmt:
        :param mathutils_fmt:
        :type mathutils_fmt:
        :param collection_id:
        :type collection_id:
        :param enum_descr_override:
        :type enum_descr_override:
        """
        ...

class InfoStructRNA:
    base: typing.Any
    bl_rna: typing.Any
    children: typing.Any
    description: typing.Any
    full_path: typing.Any
    functions: typing.Any
    global_lookup: typing.Any
    identifier: typing.Any
    module_name: typing.Any
    name: typing.Any
    nested: typing.Any
    properties: typing.Any
    py_class: typing.Any
    references: typing.Any

    def build(self):
        """

        :param self:
        :type self:
        """
        ...

    def get_bases(self):
        """

        :param self:
        :type self:
        """
        ...

    def get_nested_properties(self, ls):
        """

        :param self:
        :type self:
        :param ls:
        :type ls:
        """
        ...

    def get_py_c_functions(self):
        """

        :param self:
        :type self:
        """
        ...

    def get_py_c_properties_getset(self):
        """

        :param self:
        :type self:
        """
        ...

    def get_py_functions(self):
        """

        :param self:
        :type self:
        """
        ...

    def get_py_properties(self):
        """

        :param self:
        :type self:
        """
        ...

def BuildRNAInfo(): ...
def GetInfoFunctionRNA(bl_rna, parent_id): ...
def GetInfoOperatorRNA(bl_rna): ...
def GetInfoPropertyRNA(bl_rna, parent_id): ...
def GetInfoStructRNA(bl_rna): ...
def float_as_string(f): ...
def get_direct_functions(rna_type): ...
def get_direct_properties(rna_type): ...
def get_py_class_from_rna(rna_type): ...
def main(): ...
def range_str(val): ...
def rna_id_ignore(rna_id): ...
