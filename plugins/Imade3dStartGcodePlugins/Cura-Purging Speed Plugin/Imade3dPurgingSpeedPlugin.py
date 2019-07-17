# Copyright (c) 2019 fieldOfView and filip
# The Imade3dPurgingPlugin is released under the terms of the AGPLv3 or higher.

# needs to be redone like this one to use more variables
# https://github.com/Ketchu13/FadeHeightSettingPlugin/commit/2c14d1f9328f3b50643adf0764d43d23e6b6d543

from UM.Extension import Extension
from UM.Application import Application
from UM.Logger import Logger
from UM.Settings.SettingDefinition import SettingDefinition
from UM.Settings.DefinitionContainer import DefinitionContainer
from UM.Settings.ContainerRegistry import ContainerRegistry

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("Imade3dPurgingSpeedPlugin")

class Imade3dPurgingSpeedPlugin(Extension):
    def __init__(self):
        super().__init__()

        self._application = Application.getInstance()

        self._i18n_catalog = None
        self._purging_speed_setting_key = "material_purging_speed"
        self._purging_speed_setting_dict = {
            "label": "Purging Speed",
            "description": "Adds several Purging Speed to the Cura settings lineup. It must be included included in the start gcode to take effect (e.g., G1 E20 F{material_purging_speed})",
            "type": "float",
            "default_value": 300,
            "value": "round(speed_print * 60 / 9)",
            "minimum_value": "0",
            "minimum_value_warning": "round(speed_print * 60 / 15)",
            "maximum_value_warning": "round(speed_print * 60 / 5)",
            "settable_per_mesh": False,
            "settable_per_extruder": True,
            "settable_per_meshgroup": False
        }

        ContainerRegistry.getInstance().containerLoadComplete.connect(self._onContainerLoadComplete)

    def _onContainerLoadComplete(self, container_id):
        container = ContainerRegistry.getInstance().findContainers(id = container_id)[0]
        if not isinstance(container, DefinitionContainer):
            # skip containers that are not definitions
            return
        if container.getMetaDataEntry("type") == "extruder":
            # skip extruder definitions
            return

        material_category = container.findDefinitions(key="material")
        material_purging_speed = container.findDefinitions(key=self._purging_speed_setting_key)
        if material_category and not material_purging_speed:
            # this machine doesn't have a Purging Speed setting yet
            material_category = material_category[0]
            material_purging_speed_definition = SettingDefinition(self._purging_speed_setting_key, container, material_category, self._i18n_catalog)
            material_purging_speed_definition.deserialize(self._purging_speed_setting_dict)

            # add the setting to the already existing meterial settingdefinition
            # private member access is naughty, but the alternative is to serialise, nix and deserialise the whole thing,
            # which breaks stuff
            material_category._children.append(material_purging_speed_definition)
            container._definition_cache[self._purging_speed_setting_key] = material_purging_speed_definition
            container._updateRelations(material_purging_speed_definition)