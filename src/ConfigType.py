from typing import TypedDict

PackageType = TypedDict("PackageType", {
    "name": str,
    "author": str,
    "version": str,
    "description": str
})

ConfigType = TypedDict("ConfigType", {
    "name": str,
    "api-url": str,
    "package": PackageType
})
