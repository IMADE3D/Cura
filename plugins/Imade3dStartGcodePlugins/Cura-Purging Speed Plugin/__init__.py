# Copyright (c) 2019 fieldOfView & Filip
# The Imade3dPurgingPlugin is released under the terms of the AGPLv3 or higher.

from . import Imade3dPurgingSpeedPlugin


def getMetaData():
    return {}

def register(app):
    return {"extension": Imade3dPurgingSpeedPlugin.Imade3dPurgingSpeedPlugin()}
