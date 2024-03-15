from superwise_api.client import ModelsApi
from superwise_api.errors import raise_exception
from superwise_api.models import ModelCreate


class Model:
    """
        Method | HTTP request | Description
    ------------- | ------------- | -------------
    **create** | **POST** /v1/models | Create Model
    **delete** | **DELETE** /v1/models/{model_id} | Delete Model
    **get_by_id** | **GET** /v1/models/{model_id} | Get Model
    **get** | **GET** /v1/models | Get Models
    **update** | **PATCH** /v1/models/{model_id} | Update Model

    """

    def __init__(self, client):
        self.api = ModelsApi(client)

    @raise_exception
    def create(self, model_create: ModelCreate, **kwargs):
        return self.api.create_model(model_create, **kwargs)

    @raise_exception
    def get_models(self, **query_params):
        return self.api.get_models(**query_params)

    @raise_exception
    def get_model_by_id(self, model_id: str, **kwargs):
        return self.api.get_model_by_id(model_id, **kwargs)
