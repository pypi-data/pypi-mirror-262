import typing

GenericType = typing.TypeVar("GenericType")

class I18n:
    parsers: typing.Any
    py_file: typing.Any
    writers: typing.Any

    def check_py_module_has_translations(self, src, settings):
        """

        :param src:
        :type src:
        :param settings:
        :type settings:
        """
        ...

    def escape(self, do_all):
        """

        :param self:
        :type self:
        :param do_all:
        :type do_all:
        """
        ...

    def parse(self, kind, src, langs):
        """

        :param self:
        :type self:
        :param kind:
        :type kind:
        :param src:
        :type src:
        :param langs:
        :type langs:
        """
        ...

    def parse_from_po(self, src, langs):
        """

        :param self:
        :type self:
        :param src:
        :type src:
        :param langs:
        :type langs:
        """
        ...

    def parse_from_py(self, src, langs):
        """

        :param self:
        :type self:
        :param src:
        :type src:
        :param langs:
        :type langs:
        """
        ...

    def print_stats(self, prefix, print_msgs):
        """

        :param self:
        :type self:
        :param prefix:
        :type prefix:
        :param print_msgs:
        :type print_msgs:
        """
        ...

    def unescape(self, do_all):
        """

        :param self:
        :type self:
        :param do_all:
        :type do_all:
        """
        ...

    def update_info(self):
        """

        :param self:
        :type self:
        """
        ...

    def write(self, kind, langs):
        """

        :param self:
        :type self:
        :param kind:
        :type kind:
        :param langs:
        :type langs:
        """
        ...

    def write_to_po(self, langs):
        """

        :param self:
        :type self:
        :param langs:
        :type langs:
        """
        ...

    def write_to_py(self, langs):
        """

        :param self:
        :type self:
        :param langs:
        :type langs:
        """
        ...

class I18nMessage:
    comment_lines: typing.Any
    is_commented: typing.Any
    is_fuzzy: typing.Any
    is_tooltip: typing.Any
    msgctxt: typing.Any
    msgctxt_lines: typing.Any
    msgid: typing.Any
    msgid_lines: typing.Any
    msgstr: typing.Any
    msgstr_lines: typing.Any
    settings: typing.Any
    sources: typing.Any

    def copy(self):
        """

        :param self:
        :type self:
        """
        ...

    def do_escape(self, txt):
        """

        :param txt:
        :type txt:
        """
        ...

    def do_unescape(self, txt):
        """

        :param txt:
        :type txt:
        """
        ...

    def escape(self, do_all):
        """

        :param self:
        :type self:
        :param do_all:
        :type do_all:
        """
        ...

    def normalize(self, max_len):
        """

        :param self:
        :type self:
        :param max_len:
        :type max_len:
        """
        ...

    def unescape(self, do_all):
        """

        :param self:
        :type self:
        :param do_all:
        :type do_all:
        """
        ...

class I18nMessages:
    parsers: typing.Any
    writers: typing.Any

    def check(self, fix):
        """

        :param self:
        :type self:
        :param fix:
        :type fix:
        """
        ...

    def clean_commented(self):
        """

        :param self:
        :type self:
        """
        ...

    def escape(self, do_all):
        """

        :param self:
        :type self:
        :param do_all:
        :type do_all:
        """
        ...

    def find_best_messages_matches(
        self, msgs, msgmap, rna_ctxt, rna_struct_name, rna_prop_name, rna_enum_name
    ):
        """

        :param self:
        :type self:
        :param msgs:
        :type msgs:
        :param msgmap:
        :type msgmap:
        :param rna_ctxt:
        :type rna_ctxt:
        :param rna_struct_name:
        :type rna_struct_name:
        :param rna_prop_name:
        :type rna_prop_name:
        :param rna_enum_name:
        :type rna_enum_name:
        """
        ...

    def gen_empty_messages(
        self, uid, blender_ver, blender_hash, bl_time, default_copyright, settings
    ):
        """

        :param uid:
        :type uid:
        :param blender_ver:
        :type blender_ver:
        :param blender_hash:
        :type blender_hash:
        :param bl_time:
        :type bl_time:
        :param default_copyright:
        :type default_copyright:
        :param settings:
        :type settings:
        """
        ...

    def invalidate_reverse_cache(self, rebuild_now):
        """

        :param self:
        :type self:
        :param rebuild_now:
        :type rebuild_now:
        """
        ...

    def merge(self, msgs, replace):
        """

        :param self:
        :type self:
        :param msgs:
        :type msgs:
        :param replace:
        :type replace:
        """
        ...

    def normalize(self, max_len):
        """

        :param self:
        :type self:
        :param max_len:
        :type max_len:
        """
        ...

    def parse(self, kind, key, src):
        """

        :param self:
        :type self:
        :param kind:
        :type kind:
        :param key:
        :type key:
        :param src:
        :type src:
        """
        ...

    def parse_messages_from_po(self, src, key):
        """

        :param self:
        :type self:
        :param src:
        :type src:
        :param key:
        :type key:
        """
        ...

    def print_info(self, prefix, output, print_stats, print_errors):
        """

        :param self:
        :type self:
        :param prefix:
        :type prefix:
        :param output:
        :type output:
        :param print_stats:
        :type print_stats:
        :param print_errors:
        :type print_errors:
        """
        ...

    def rtl_process(self):
        """

        :param self:
        :type self:
        """
        ...

    def unescape(self, do_all):
        """

        :param self:
        :type self:
        :param do_all:
        :type do_all:
        """
        ...

    def update(self, ref, use_similar, keep_old_commented):
        """

        :param self:
        :type self:
        :param ref:
        :type ref:
        :param use_similar:
        :type use_similar:
        :param keep_old_commented:
        :type keep_old_commented:
        """
        ...

    def update_info(self):
        """

        :param self:
        :type self:
        """
        ...

    def write(self, kind, dest):
        """

        :param self:
        :type self:
        :param kind:
        :type kind:
        :param dest:
        :type dest:
        """
        ...

    def write_messages_to_mo(self, fname):
        """

        :param self:
        :type self:
        :param fname:
        :type fname:
        """
        ...

    def write_messages_to_po(self, fname, compact):
        """

        :param self:
        :type self:
        :param fname:
        :type fname:
        :param compact:
        :type compact:
        """
        ...

def enable_addons(addons, support, disable, check_only): ...
def find_best_isocode_matches(uid, iso_codes): ...
def get_best_similar(data): ...
def get_po_files_from_dir(root_dir, langs): ...
def is_valid_po_path(path): ...
def list_po_dir(root_path, settings): ...
def locale_explode(locale): ...
def locale_match(loc1, loc2): ...
