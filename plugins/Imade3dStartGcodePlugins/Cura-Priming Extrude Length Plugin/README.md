# Imade3dPrimingExtrudeLengthPlugin

This plugin adds a setting named Imade3dPrimingExtrudeLengthPlugin to the Material category in the Custom print setup of Cura.

This is based on Linear Advance Settings by Field of View.

Until there's a release, the plugins is completely or not even yet under development.

---

Original readme:

If the start gcode doesn't include an M900 statement to set the linear advance parameters, a single G-code line is added before the start G-code:
```
...
M900 K{material_linear_advance_factor}
...
```

Users may want to add more detailed M900 parameters in their start G-code snippet, eg:

```
...
M900 K{material_linear_advance_factor}
M900 W{line_width} H{layer_height} D{material_diameter}
...
```
