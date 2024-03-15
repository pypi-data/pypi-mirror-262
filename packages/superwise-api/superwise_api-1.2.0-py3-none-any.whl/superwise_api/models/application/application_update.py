from typing import Optional

from superwise_api.client import ApplicationUpdate as RawApplicationUpdate


class ApplicationUpdate(RawApplicationUpdate):
    """
    ApplicationUpdate
    """

    name: Optional[str] = None
    model_id: Optional[str] = None

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of prompt
        if self.prompt:
            _dict["prompt"] = self.prompt.to_dict()

        return _dict
