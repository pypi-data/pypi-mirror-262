from superwise_api.client.models.tool_config_pg_vector import ToolConfigPGVector as RawToolConfigPGVector
from superwise_api.models.tool.embeding_model import EmbeddingModel


class ToolConfigPGVector(RawToolConfigPGVector):
    type: str = "PGVector"
    embedding_model: EmbeddingModel
