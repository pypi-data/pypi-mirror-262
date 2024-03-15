from typing import Optional

from superwise_api.client.models.tool_response import ToolResponse as RawToolResponse


class ToolResponse(RawToolResponse):
    config: Optional[dict]
    description: Optional[str]

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[ToolResponse]":
        """Create an instance of ToolResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ToolResponse.parse_obj(obj)

        _obj = ToolResponse.parse_obj(
            {
                "id": obj.get("id"),
                "name": obj.get("name"),
                "description": obj.get("description") if obj.get("description") is not None else None,
                "type": obj.get("type"),
                "config": obj.get("config") if obj.get("config") is not None else None,
                "created_at": obj.get("created_at"),
                "created_by": obj.get("created_by"),
            }
        )
        return _obj
