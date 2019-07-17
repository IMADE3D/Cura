# Copyright (c) 2019 fieldOfView and filip
# The Imade3dMaterialProbingTemperaturePlugin is released under the terms of the AGPLv3 or higher.

# needs to be redone like this one to use more variables
# https://github.com/Ketchu13/FadeHeightSettingPlugin/commit/2c14d1f9328f3b50643adf0764d43d23e6b6d543

from UM.Extension import Extension
from UM.Application import Application
from UM.Logger import Logger
from UM.Settings.SettingDefinition import SettingDefinition
from UM.Settings.DefinitionContainer import DefinitionContainer
from UM.Settings.ContainerRegistry import ContainerRegistry

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("Imade3dMaterialProbingTemperaturePlugin")

class Imade3dMaterialProbingTemperaturePlugin(Extension):
    def __init__(self):
        super().__init__()

        self._application = Application.getInstance()

        self._i18n_catalog = None
        self._probing_temperature_setting_key = "material_probing_temperature"
        self._probing_temperature_setting_dict = {
            "label": "Probing Temperature",
            "description": "Adds Probing Temperature to the Cura settings lineup. It must be included included in the start gcode to take effect (e.g., G1 E20 F{material_probing_temperature})",
            "type": "float",
            "default_value": 180,
            "value": "round(material_print_temperature - 30)",
            "minimum_value": "0",
            "minimum_value_warning": "round(material_print_temperature - 80)",
            "maximum_value_warning": "round(material_print_temperature - 10)",
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
        material_probing_temperature = container.findDefinitions(key=self._probing_temperature_setting_key)
        if material_category and not material_probing_temperature:
            # this machine doesn't have a Probing Temperature setting yet
            material_category = material_category[0]
            material_probing_temperature_definition = SettingDefinition(self._probing_temperature_setting_key, container, material_category, self._i18n_catalog)
            material_probing_temperature_definition.deserialize(self._probing_temperature_setting_dict)

            # add the setting to the already existing meterial settingdefinition
            # private member access is naughty, but the alternative is to serialise, nix and deserialise the whole thing,
            # which breaks stuff
            material_category._children.append(material_probing_temperature_definition)
            container._definition_cache[self._probing_temperature_setting_key] = material_probing_temperature_definition
            container._updateRelations(material_probing_temperature_definition)