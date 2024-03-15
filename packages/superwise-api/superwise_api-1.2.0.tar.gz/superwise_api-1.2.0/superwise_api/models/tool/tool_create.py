from typing import Union

from superwise_api.client import ToolConfigBigQuery
from superwise_api.client import ToolConfigSQLDatabaseMSSQL
from superwise_api.client import ToolConfigSQLDatabaseMySQL
from superwise_api.client import ToolConfigSQLDatabaseOracle
from superwise_api.client import ToolConfigSQLDatabasePostgres
from superwise_api.client.models.tool_create import ToolCreate as RawToolCreate
from superwise_api.models.tool.tool_config_pg_vector import ToolConfigPGVector


class ToolCreate(RawToolCreate):
    config: Union[
        ToolConfigPGVector,
        ToolConfigSQLDatabasePostgres,
        ToolConfigSQLDatabaseMySQL,
        ToolConfigSQLDatabaseMSSQL,
        ToolConfigSQLDatabaseOracle,
        ToolConfigBigQuery,
    ]

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of description
        if self.description:
            _dict["description"] = self.description.to_dict()
        # override the default output from pydantic by calling `to_dict()` of config
        if self.config:
            _dict["config"] = self.config.to_dict()
        return _dict
