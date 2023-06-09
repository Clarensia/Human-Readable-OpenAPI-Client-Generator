from typing import List, TypedDict

PackageType = TypedDict("PackageType", {
    "name": str,
    "author": str,
    "author-comment": str,
    "version": str,
    "description": str,
    "all-exports": List[str]
})

ConfigType = TypedDict("ConfigType", {
    "name": str,
    "api-url": str,
    "package": PackageType,
    "model-package-description": str,
    "exception-package-description": str
})
