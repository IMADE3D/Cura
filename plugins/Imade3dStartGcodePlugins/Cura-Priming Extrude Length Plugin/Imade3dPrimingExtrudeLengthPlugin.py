# Copyright (c) 2019 fieldOfView and filip
# The Imade3dPrimingPlugin is released under the terms of the AGPLv3 or higher.

from UM.Extension import Extension
from UM.Application import Application
from UM.Logger import Logger
from UM.Settings.SettingDefinition import SettingDefinition
from UM.Settings.DefinitionContainer import DefinitionContainer
from UM.Settings.ContainerRegistry import ContainerRegistry

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("Imade3dPrimingExtrudeLengthPlugin")

class Imade3dPrimingExtrudeLengthPlugin(Extension):
    def __init__(self):
        super().__init__()

        self._application = Application.getInstance()

        self._i18n_catalog = None
        self._priming_extrude_length_setting_key = "material_priming_extrude_length"
        self._priming_extrude_length_setting_dict = {
            "label": "Priming Extrude Length",
            "description": "Adds Priming Extrude Length to the Cura settings lineup. It must be included included in the start gcode to take effect (e.g., G1 E20 F{material_priming_extrude_length})",
            "type": "float",
            "default_value": 7,
            "minimum_value": "0",
            "minimum_value_warning": "0",
            "maximum_value_warning": "20",
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
        material_priming_extrude_length = container.findDefinitions(key=self._priming_extrude_length_setting_key)
        if material_category and not material_priming_extrude_length:
            # this machine doesn't have a This setting yet
            material_category = material_category[0]
            material_priming_extrude_length_definition = SettingDefinition(self._priming_extrude_length_setting_key, container, material_category, self._i18n_catalog)
            material_priming_extrude_length_definition.deserialize(self._priming_extrude_length_setting_dict)

            # add the setting to the already existing meterial settingdefinition
            # private member access is naughty, but the alternative is to serialise, nix and deserialise the whole thing,
            # which breaks stuff
            material_category._children.append(material_priming_extrude_length_definition)
            container._definition_cache[self._priming_extrude_length_setting_key] = material_priming_extrude_length_definition
            container._updateRelations(material_priming_extrude_length_definition)