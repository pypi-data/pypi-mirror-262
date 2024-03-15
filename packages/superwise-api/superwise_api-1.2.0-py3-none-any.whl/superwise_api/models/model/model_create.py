from superwise_api.client.models.model_create import ModelCreate as RawModelCreate


class ModelCreate(RawModelCreate):
    version: str

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        return _dict
