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



from pydantic import Extra,  BaseModel, Field, StrictStr

class DatasourceConfigBaseFullPath(BaseModel):
    """
    DatasourceConfigBaseFullPath
    """
    full_path: StrictStr = Field(..., alias="fullPath", description="path includes the bucket name and the path within the bucket where you have stored your information")
    __properties = ["fullPath"]

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
    def from_json(cls, json_str: str) -> DatasourceConfigBaseFullPath:
        """Create an instance of DatasourceConfigBaseFullPath from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self, by_alias: bool = False):
        """Returns the dictionary representation of the model"""
        _dict = self.dict(by_alias=by_alias,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DatasourceConfigBaseFullPath:
        """Create an instance of DatasourceConfigBaseFullPath from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DatasourceConfigBaseFullPath.parse_obj(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in DatasourceConfigBaseFullPath) in the input: " + str(obj))

        _obj = DatasourceConfigBaseFullPath.parse_obj({
            "full_path": obj.get("fullPath")
        })
        return _obj

