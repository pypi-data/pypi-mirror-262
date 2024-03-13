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

class DockerAuthorizationResponse(BaseModel):
    """
    DockerAuthorizationResponse
    """
    body_string: StrictStr = Field(..., alias="bodyString")
    body_hmac: StrictStr = Field(..., alias="bodyHmac")
    __properties = ["bodyString", "bodyHmac"]

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
    def from_json(cls, json_str: str) -> DockerAuthorizationResponse:
        """Create an instance of DockerAuthorizationResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self, by_alias: bool = False):
        """Returns the dictionary representation of the model"""
        _dict = self.dict(by_alias=by_alias,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DockerAuthorizationResponse:
        """Create an instance of DockerAuthorizationResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DockerAuthorizationResponse.parse_obj(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in DockerAuthorizationResponse) in the input: " + str(obj))

        _obj = DockerAuthorizationResponse.parse_obj({
            "body_string": obj.get("bodyString"),
            "body_hmac": obj.get("bodyHmac")
        })
        return _obj

