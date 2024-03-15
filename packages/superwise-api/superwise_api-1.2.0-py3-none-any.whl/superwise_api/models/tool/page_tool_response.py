from typing import Optional

from pydantic import conint
from pydantic import conlist
from pydantic import StrictInt

from superwise_api.client.models.page_tool_response import PageToolResponse as RawPageToolResponse
from superwise_api.models.tool.tool_response import ToolResponse


class PageToolResponse(RawPageToolResponse):
    items: conlist(ToolResponse)
    total: Optional[StrictInt] = 0
    page: conint(strict=True, ge=1)
    size: conint(strict=True, ge=1)
    pages: conint(strict=True, ge=1)

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[PageToolResponse]":
        """Create an instance of PageToolResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PageToolResponse.parse_obj(obj)

        _obj = PageToolResponse.parse_obj(
            {
                "items": [ToolResponse.from_dict(_item) for _item in obj.get("items")]
                if obj.get("items") is not None
                else None,
                "total": obj.get("total") if obj.get("total") is not None else 0,
                "page": obj.get("page"),
                "size": obj.get("size"),
                "pages": obj.get("pages"),
            }
        )
        return _obj
