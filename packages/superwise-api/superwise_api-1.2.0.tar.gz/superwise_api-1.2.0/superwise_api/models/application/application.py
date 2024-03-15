from superwise_api.client.models.application_create import ApplicationCreate as RawApplicationCreate


class ApplicationCreate(RawApplicationCreate):
    model_id: str

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)

        # override the default output from pydantic by calling `to_dict()` of prompt
        if self.prompt:
            _dict["prompt"] = self.prompt.to_dict()
        return _dict
