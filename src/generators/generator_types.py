from typing import Any, Dict, List, TypedDict

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

FuncSchema = TypedDict("FuncSchema", {
    "title": str,
    "type": str,
    "description": str,
    "default": str | int
})

FuncParam = TypedDict("FuncParam", {
    "description": str,
    "required": bool,
    "schema": FuncSchema,
    "name": str,
    "in": str
})

Get = TypedDict("Get", {
    "tags": List[str],
    "summary": str,
    "operationId": str,
    "parameters": List[FuncParam],
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
    "example": Dict[str, Any]
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
