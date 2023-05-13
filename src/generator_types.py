from typing import Dict, TypedDict

Property = TypedDict('Property', {
    "title": str,
    "type": str,
    "default": str
})

Schema = TypedDict('Schema', {
    "title": str,
    "type": str,
    "properties": Dict[str, Property],
    "example": Dict[str, str | int]
})
