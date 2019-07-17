# Copyright (c) 2019 fieldOfView & Filip
# The Imade3dPrimingPlugin is released under the terms of the AGPLv3 or higher.

from . import Imade3dPrimingExtrudeLengthPlugin


def getMetaData():
    return {}

def register(app):
    return {"extension": Imade3dPrimingExtrudeLengthPlugin.Imade3dPrimingExtrudeLengthPlugin()}
