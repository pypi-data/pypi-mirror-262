import typing
import bl_ui.properties_grease_pencil_common
import bl_ui.properties_mask_common
import bl_ui.properties_paint_common
import bl_ui.space_toolsystem_common
import bpy_types

GenericType = typing.TypeVar("GenericType")

class BrushButtonsPanel(bl_ui.properties_paint_common.UnifiedPaintPanel):
    bl_region_type: typing.Any
    bl_space_type: typing.Any

    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

class IMAGE_HT_header(bpy_types.Header, bpy_types._GenericUI):
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_xform_template(self, layout, context):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_HT_tool_header(bpy_types.Header, bpy_types._GenericUI):
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_mode_settings(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_tool_settings(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_editor_menus(bpy_types.Menu, bpy_types._GenericUI):
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_image(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_image_invert(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_image_transform(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_mask_context_menu(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_pivot_pie(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_select(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_select_linked(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_align(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_context_menu(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_merge(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_mirror(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_select_mode(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_showhide(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_snap(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_snap_pie(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_split(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_transform(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_uvs_unwrap(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_view(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_view_pie(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_MT_view_zoom(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def draw_collapsible(self, context, layout):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        """
        ...

    def draw_preset(self, _context):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
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

    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_active_mask_point(
    bpy_types.Panel, bl_ui.properties_mask_common.MASK_PT_point, bpy_types._GenericUI
):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_active_mask_spline(
    bpy_types.Panel, bl_ui.properties_mask_common.MASK_PT_spline, bpy_types._GenericUI
):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_active_tool(
    bpy_types._GenericUI,
    bpy_types.Panel,
    bl_ui.space_toolsystem_common.ToolActivePanelHelper,
):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_annotation(
    bpy_types.Panel,
    bl_ui.properties_grease_pencil_common.AnnotationDataPanel,
    bpy_types._GenericUI,
):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_header(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_layers(self, context, layout, gpd):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        :param layout:
        :type layout:
        :param gpd:
        :type gpd:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_gizmo_display(bpy_types.Panel, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    bl_ui_units_x: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_image_properties(bpy_types.Panel, bpy_types._GenericUI):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_mask(
    bpy_types.Panel, bl_ui.properties_mask_common.MASK_PT_mask, bpy_types._GenericUI
):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_mask_display(
    bpy_types.Panel, bl_ui.properties_mask_common.MASK_PT_display, bpy_types._GenericUI
):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_mask_layers(
    bpy_types.Panel, bl_ui.properties_mask_common.MASK_PT_layers, bpy_types._GenericUI
):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_overlay(bpy_types.Panel, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    bl_ui_units_x: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_overlay_guides(bpy_types.Panel, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_overlay_image(bpy_types.Panel, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_overlay_texture_paint(bpy_types.Panel, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_overlay_uv_edit_geometry(bpy_types.Panel, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_overlay_uv_stretch(bpy_types.Panel, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_proportional_edit(bpy_types.Panel, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    bl_ui_units_x: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_render_slots(bpy_types.Panel, bpy_types._GenericUI):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_snapping(bpy_types.Panel, bpy_types._GenericUI):
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_udim_tiles(bpy_types.Panel, bpy_types._GenericUI):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_uv_cursor(bpy_types.Panel, bpy_types._GenericUI):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_view_display(bpy_types.Panel, bpy_types._GenericUI):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_UL_render_slots(bpy_types.UIList, bpy_types._GenericUI):
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw_item(
        self,
        _context,
        layout,
        _data,
        item,
        _icon,
        _active_data,
        _active_propname,
        _index,
    ):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        :param layout:
        :type layout:
        :param _data:
        :type _data:
        :param item:
        :type item:
        :param _icon:
        :type _icon:
        :param _active_data:
        :type _active_data:
        :param _active_propname:
        :type _active_propname:
        :param _index:
        :type _index:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_UL_udim_tiles(bpy_types.UIList, bpy_types._GenericUI):
    bl_rna: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw_item(
        self,
        _context,
        layout,
        _data,
        item,
        _icon,
        _active_data,
        _active_propname,
        _index,
    ):
        """

        :param self:
        :type self:
        :param _context:
        :type _context:
        :param layout:
        :type layout:
        :param _data:
        :type _data:
        :param item:
        :type item:
        :param _icon:
        :type _icon:
        :param _active_data:
        :type _active_data:
        :param _active_propname:
        :type _active_propname:
        :param _index:
        :type _index:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class ImagePaintPanel:
    bl_region_type: typing.Any
    bl_space_type: typing.Any

class ImageScopesPanel:
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

class UVSculptPanel(bl_ui.properties_paint_common.UnifiedPaintPanel):
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

class _draw_tool_settings_context_mode:
    def PAINT(self, context, layout, tool):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        :param tool:
        :type tool:
        """
        ...

    def UV(self, context, layout, tool):
        """

        :param context:
        :type context:
        :param layout:
        :type layout:
        :param tool:
        :type tool:
        """
        ...

class IMAGE_PT_paint_curve(
    bl_ui.properties_paint_common.BrushPanel,
    bpy_types._GenericUI,
    BrushButtonsPanel,
    bpy_types.Panel,
    bl_ui.properties_paint_common.FalloffPanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_paint_stroke(
    bl_ui.properties_paint_common.BrushPanel,
    bpy_types._GenericUI,
    BrushButtonsPanel,
    bpy_types.Panel,
    bl_ui.properties_paint_common.StrokePanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    bl_ui_units_x: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_paint_stroke_smooth_stroke(
    bl_ui.properties_paint_common.BrushPanel,
    BrushButtonsPanel,
    bpy_types.Panel,
    bpy_types._GenericUI,
    bl_ui.properties_paint_common.SmoothStrokePanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_header(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_tools_brush_display(
    bl_ui.properties_paint_common.BrushPanel,
    BrushButtonsPanel,
    bpy_types.Panel,
    bpy_types._GenericUI,
    bl_ui.properties_paint_common.DisplayPanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    bl_ui_units_x: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_header(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_tools_brush_texture(
    bpy_types.Panel,
    BrushButtonsPanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
    bpy_types._GenericUI,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_tools_imagepaint_symmetry(
    bpy_types.Panel,
    BrushButtonsPanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
    bpy_types._GenericUI,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_tools_mask_texture(
    bl_ui.properties_paint_common.BrushPanel,
    BrushButtonsPanel,
    bpy_types.Panel,
    bpy_types._GenericUI,
    bl_ui.properties_paint_common.TextureMaskPanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    bl_ui_units_x: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_paint_clone(
    ImagePaintPanel,
    bl_ui.properties_paint_common.BrushPanel,
    bpy_types.Panel,
    bpy_types._GenericUI,
    bl_ui.properties_paint_common.ClonePanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def draw_header(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_paint_color(ImagePaintPanel, bpy_types._GenericUI, bpy_types.Panel):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_paint_select(
    ImagePaintPanel,
    bl_ui.properties_paint_common.BrushPanel,
    bpy_types.Panel,
    bpy_types._GenericUI,
    bl_ui.properties_paint_common.BrushSelectPanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_paint_settings(ImagePaintPanel, bpy_types._GenericUI, bpy_types.Panel):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_paint_settings_advanced(
    ImagePaintPanel, bpy_types._GenericUI, bpy_types.Panel
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    bl_ui_units_x: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_paint_swatches(
    ImagePaintPanel,
    bl_ui.properties_paint_common.BrushPanel,
    bpy_types.Panel,
    bpy_types._GenericUI,
    bl_ui.properties_paint_common.ColorPalettePanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_sample_line(ImageScopesPanel, bpy_types.Panel, bpy_types._GenericUI):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_scope_sample(ImageScopesPanel, bpy_types.Panel, bpy_types._GenericUI):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_view_histogram(ImageScopesPanel, bpy_types.Panel, bpy_types._GenericUI):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_view_vectorscope(
    ImageScopesPanel, bpy_types.Panel, bpy_types._GenericUI
):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_view_waveform(ImageScopesPanel, bpy_types.Panel, bpy_types._GenericUI):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_uv_sculpt_brush_select(
    UVSculptPanel,
    ImagePaintPanel,
    bl_ui.properties_paint_common.BrushPanel,
    bpy_types._GenericUI,
    bpy_types.Panel,
    bl_ui.properties_paint_common.BrushSelectPanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_uv_sculpt_brush_settings(
    UVSculptPanel,
    ImagePaintPanel,
    bpy_types._GenericUI,
    bpy_types.Panel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_uv_sculpt_curve(
    UVSculptPanel,
    ImagePaintPanel,
    bl_ui.properties_paint_common.BrushPanel,
    bpy_types._GenericUI,
    bpy_types.Panel,
    bl_ui.properties_paint_common.FalloffPanel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_parent_id: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...

class IMAGE_PT_uv_sculpt_options(
    UVSculptPanel,
    ImagePaintPanel,
    bpy_types._GenericUI,
    bpy_types.Panel,
    bl_ui.properties_paint_common.UnifiedPaintPanel,
):
    bl_category: typing.Any
    bl_context: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def append(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def as_pointer(self): ...
    def bl_rna_get_subclass(self): ...
    def bl_rna_get_subclass_py(self): ...
    def draw(self, context):
        """

        :param self:
        :type self:
        :param context:
        :type context:
        """
        ...

    def driver_add(self): ...
    def driver_remove(self): ...
    def get(self): ...
    def get_brush_mode(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def id_properties_clear(self): ...
    def id_properties_ensure(self): ...
    def id_properties_ui(self): ...
    def is_extended(self): ...
    def is_property_hidden(self): ...
    def is_property_overridable_library(self): ...
    def is_property_readonly(self): ...
    def is_property_set(self): ...
    def items(self): ...
    def keyframe_delete(self): ...
    def keyframe_insert(self): ...
    def keys(self): ...
    def paint_settings(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def path_from_id(self): ...
    def path_resolve(self): ...
    def poll(self, context):
        """

        :param context:
        :type context:
        """
        ...

    def pop(self): ...
    def prepend(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def prop_unified(
        self,
        layout,
        context,
        brush,
        prop_name,
        unified_name,
        pressure_name,
        icon,
        text,
        slider,
        header,
    ):
        """

        :param layout:
        :type layout:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param unified_name:
        :type unified_name:
        :param pressure_name:
        :type pressure_name:
        :param icon:
        :type icon:
        :param text:
        :type text:
        :param slider:
        :type slider:
        :param header:
        :type header:
        """
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param text:
        :type text:
        """
        ...

    def prop_unified_color_picker(
        self, parent, context, brush, prop_name, value_slider
    ):
        """

        :param parent:
        :type parent:
        :param context:
        :type context:
        :param brush:
        :type brush:
        :param prop_name:
        :type prop_name:
        :param value_slider:
        :type value_slider:
        """
        ...

    def property_overridable_library_set(self): ...
    def property_unset(self): ...
    def remove(self, draw_func):
        """

        :param draw_func:
        :type draw_func:
        """
        ...

    def type_recast(self): ...
    def values(self): ...
