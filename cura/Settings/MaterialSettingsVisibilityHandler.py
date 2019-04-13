# Copyright (c) 2017 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

import UM.Settings.Models.SettingVisibilityHandler


class MaterialSettingsVisibilityHandler(UM.Settings.Models.SettingVisibilityHandler.SettingVisibilityHandler):
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent = parent, *args, **kwargs)

        material_settings = {
            "default_material_print_temperature",
            "default_material_bed_temperature",
            "material_standby_temperature",
            #"material_flow_temp_graph",
            "material_bed_temperature_layer_0",
            "material_flow",
            "material_flow_layer_0",
            #"material_linear_advance_factor", # uncomment if you are using Linear Advance Plugin
            "cool_fan_speed",
            "retraction_amount",
            "retraction_speed",
        }

        self.setVisible(material_settings)
