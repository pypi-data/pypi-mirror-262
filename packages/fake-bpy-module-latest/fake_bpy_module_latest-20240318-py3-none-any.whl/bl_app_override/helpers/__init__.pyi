import typing

GenericType = typing.TypeVar("GenericType")

class AppOverrideState:
    addon_paths: typing.Any
    addons: typing.Any
    class_ignore: typing.Any
    ui_ignore_classes: typing.Any
    ui_ignore_label: typing.Any
    ui_ignore_menu: typing.Any
    ui_ignore_operator: typing.Any
    ui_ignore_property: typing.Any

    def setup(self):
        """

        :param self:
        :type self:
        """
        ...

    def teardown(self):
        """

        :param self:
        :type self:
        """
        ...
