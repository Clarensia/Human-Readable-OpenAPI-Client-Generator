from typing import Dict, List, TypedDict

Info = TypedDict('Info', {
    "title": str,
    "description": str,
    "version": str
})

ItemsDict = TypedDict('ItemsDict', {
    "$ref": str
})

AdvancedItemDict = TypedDict("AdvancedItemDict", {
    "title": str,
    "type": str,
    "items": ItemsDict
})

ApplicationJson = TypedDict("ApplicationJson", {
    "schema": ItemsDict | AdvancedItemDict
}, total=False)

Content = TypedDict("Content", {
    "application/json": ApplicationJson
})

Response = TypedDict("Response", {
    "description": str,
    "content": Content
})

Get = TypedDict("Get", {
    "tags": List[str],
    "summary": str,
    "operationId": str,
    "responses": Dict[str, Response]
})

OpenAPIPath = TypedDict('Path', {
    "get": Get
})

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

Components = TypedDict('Components', {
    "schemas": Dict[str, Schema]
})

OpenAPI = TypedDict("OpenAPI", {
    "openapi": str,
    "info": Info,
    "paths": Dict[str, OpenAPIPath],
    "components": Components
})
