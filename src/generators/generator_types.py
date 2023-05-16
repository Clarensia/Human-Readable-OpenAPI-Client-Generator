from typing import Dict, TypedDict

class ItemsDict(TypedDict):
    "$ref": str

class PropertyOptional(TypedDict, total=False):
    items: ItemsDict    

class PropertyRequired(TypedDict):
    title: str
    type: str
    description: str
    
class Property(PropertyRequired, PropertyOptional):
    pass

Schema = TypedDict('Schema', {
    "title": str,
    "type": str,
    "properties": Dict[str, Property],
    "example": Dict[str, str | int]
})
