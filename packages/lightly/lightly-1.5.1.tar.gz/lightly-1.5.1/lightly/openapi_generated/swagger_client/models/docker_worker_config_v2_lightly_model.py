# coding: utf-8

"""
    Lightly API

    Lightly.ai enables you to do self-supervised learning in an easy and intuitive way. The lightly.ai OpenAPI spec defines how one can interact with our REST API to unleash the full potential of lightly.ai  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: support@lightly.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import Extra,  BaseModel, Field, conint
from lightly.openapi_generated.swagger_client.models.lightly_model_v2 import LightlyModelV2

class DockerWorkerConfigV2LightlyModel(BaseModel):
    """
    DockerWorkerConfigV2LightlyModel
    """
    name: Optional[LightlyModelV2] = None
    out_dim: Optional[conint(strict=True, ge=1)] = Field(None, alias="outDim")
    num_ftrs: Optional[conint(strict=True, ge=1)] = Field(None, alias="numFtrs")
    width: Optional[conint(strict=True, ge=1)] = None
    __properties = ["name", "outDim", "numFtrs", "width"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True
        use_enum_values = True
        extra = Extra.forbid

    def to_str(self, by_alias: bool = False) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.dict(by_alias=by_alias))

    def to_json(self, by_alias: bool = False) -> str:
        """Returns the JSON representation of the model"""
        return json.dumps(self.to_dict(by_alias=by_alias))

    @classmethod
    def from_json(cls, json_str: str) -> DockerWorkerConfigV2LightlyModel:
        """Create an instance of DockerWorkerConfigV2LightlyModel from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self, by_alias: bool = False):
        """Returns the dictionary representation of the model"""
        _dict = self.dict(by_alias=by_alias,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DockerWorkerConfigV2LightlyModel:
        """Create an instance of DockerWorkerConfigV2LightlyModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DockerWorkerConfigV2LightlyModel.parse_obj(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in DockerWorkerConfigV2LightlyModel) in the input: " + str(obj))

        _obj = DockerWorkerConfigV2LightlyModel.parse_obj({
            "name": obj.get("name"),
            "out_dim": obj.get("outDim"),
            "num_ftrs": obj.get("numFtrs"),
            "width": obj.get("width")
        })
        return _obj

