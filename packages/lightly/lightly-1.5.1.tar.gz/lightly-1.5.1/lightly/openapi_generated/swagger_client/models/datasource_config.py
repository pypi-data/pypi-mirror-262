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
from inspect import getfullargspec
import json
import pprint
import re  # noqa: F401

from typing import Any, List, Optional
from pydantic import BaseModel, Field, StrictStr, ValidationError, validator
from lightly.openapi_generated.swagger_client.models.datasource_config_azure import DatasourceConfigAzure
from lightly.openapi_generated.swagger_client.models.datasource_config_gcs import DatasourceConfigGCS
from lightly.openapi_generated.swagger_client.models.datasource_config_lightly import DatasourceConfigLIGHTLY
from lightly.openapi_generated.swagger_client.models.datasource_config_local import DatasourceConfigLOCAL
from lightly.openapi_generated.swagger_client.models.datasource_config_obs import DatasourceConfigOBS
from lightly.openapi_generated.swagger_client.models.datasource_config_s3 import DatasourceConfigS3
from lightly.openapi_generated.swagger_client.models.datasource_config_s3_delegated_access import DatasourceConfigS3DelegatedAccess
from typing import Any, List
from pydantic import StrictStr, Field, Extra

DATASOURCECONFIG_ONE_OF_SCHEMAS = ["DatasourceConfigAzure", "DatasourceConfigGCS", "DatasourceConfigLIGHTLY", "DatasourceConfigLOCAL", "DatasourceConfigOBS", "DatasourceConfigS3", "DatasourceConfigS3DelegatedAccess"]

class DatasourceConfig(BaseModel):
    """
    DatasourceConfig
    """
    # data type: DatasourceConfigLIGHTLY
    oneof_schema_1_validator: Optional[DatasourceConfigLIGHTLY] = None
    # data type: DatasourceConfigS3
    oneof_schema_2_validator: Optional[DatasourceConfigS3] = None
    # data type: DatasourceConfigS3DelegatedAccess
    oneof_schema_3_validator: Optional[DatasourceConfigS3DelegatedAccess] = None
    # data type: DatasourceConfigGCS
    oneof_schema_4_validator: Optional[DatasourceConfigGCS] = None
    # data type: DatasourceConfigAzure
    oneof_schema_5_validator: Optional[DatasourceConfigAzure] = None
    # data type: DatasourceConfigOBS
    oneof_schema_6_validator: Optional[DatasourceConfigOBS] = None
    # data type: DatasourceConfigLOCAL
    oneof_schema_7_validator: Optional[DatasourceConfigLOCAL] = None
    actual_instance: Any
    one_of_schemas: List[str] = Field(DATASOURCECONFIG_ONE_OF_SCHEMAS, const=True)

    class Config:
        validate_assignment = True
        use_enum_values = True
        extra = Extra.forbid

    discriminator_value_class_map = {
    }

    def __init__(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = DatasourceConfig.construct()
        error_messages = []
        match = 0
        # validate data type: DatasourceConfigLIGHTLY
        if not isinstance(v, DatasourceConfigLIGHTLY):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasourceConfigLIGHTLY`")
        else:
            match += 1
        # validate data type: DatasourceConfigS3
        if not isinstance(v, DatasourceConfigS3):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasourceConfigS3`")
        else:
            match += 1
        # validate data type: DatasourceConfigS3DelegatedAccess
        if not isinstance(v, DatasourceConfigS3DelegatedAccess):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasourceConfigS3DelegatedAccess`")
        else:
            match += 1
        # validate data type: DatasourceConfigGCS
        if not isinstance(v, DatasourceConfigGCS):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasourceConfigGCS`")
        else:
            match += 1
        # validate data type: DatasourceConfigAzure
        if not isinstance(v, DatasourceConfigAzure):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasourceConfigAzure`")
        else:
            match += 1
        # validate data type: DatasourceConfigOBS
        if not isinstance(v, DatasourceConfigOBS):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasourceConfigOBS`")
        else:
            match += 1
        # validate data type: DatasourceConfigLOCAL
        if not isinstance(v, DatasourceConfigLOCAL):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasourceConfigLOCAL`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in DatasourceConfig with oneOf schemas: DatasourceConfigAzure, DatasourceConfigGCS, DatasourceConfigLIGHTLY, DatasourceConfigLOCAL, DatasourceConfigOBS, DatasourceConfigS3, DatasourceConfigS3DelegatedAccess. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in DatasourceConfig with oneOf schemas: DatasourceConfigAzure, DatasourceConfigGCS, DatasourceConfigLIGHTLY, DatasourceConfigLOCAL, DatasourceConfigOBS, DatasourceConfigS3, DatasourceConfigS3DelegatedAccess. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: dict) -> DatasourceConfig:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> DatasourceConfig:
        """Returns the object represented by the json string"""
        instance = DatasourceConfig.construct()
        error_messages = []
        match = 0

        # use oneOf discriminator to lookup the data type
        _data_type = json.loads(json_str).get("type")
        if not _data_type:
            raise ValueError("Failed to lookup data type from the field `type` in the input.")

        # check if data type is `DatasourceConfigAzure`
        if _data_type == "AZURE":
            instance.actual_instance = DatasourceConfigAzure.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigAzure`
        if _data_type == "DatasourceConfigAzure":
            instance.actual_instance = DatasourceConfigAzure.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigGCS`
        if _data_type == "DatasourceConfigGCS":
            instance.actual_instance = DatasourceConfigGCS.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigLIGHTLY`
        if _data_type == "DatasourceConfigLIGHTLY":
            instance.actual_instance = DatasourceConfigLIGHTLY.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigLOCAL`
        if _data_type == "DatasourceConfigLOCAL":
            instance.actual_instance = DatasourceConfigLOCAL.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigOBS`
        if _data_type == "DatasourceConfigOBS":
            instance.actual_instance = DatasourceConfigOBS.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigS3`
        if _data_type == "DatasourceConfigS3":
            instance.actual_instance = DatasourceConfigS3.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigS3DelegatedAccess`
        if _data_type == "DatasourceConfigS3DelegatedAccess":
            instance.actual_instance = DatasourceConfigS3DelegatedAccess.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigGCS`
        if _data_type == "GCS":
            instance.actual_instance = DatasourceConfigGCS.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigLIGHTLY`
        if _data_type == "LIGHTLY":
            instance.actual_instance = DatasourceConfigLIGHTLY.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigLOCAL`
        if _data_type == "LOCAL":
            instance.actual_instance = DatasourceConfigLOCAL.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigOBS`
        if _data_type == "OBS":
            instance.actual_instance = DatasourceConfigOBS.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigS3`
        if _data_type == "S3":
            instance.actual_instance = DatasourceConfigS3.from_json(json_str)
            return instance

        # check if data type is `DatasourceConfigS3DelegatedAccess`
        if _data_type == "S3DelegatedAccess":
            instance.actual_instance = DatasourceConfigS3DelegatedAccess.from_json(json_str)
            return instance

        # deserialize data into DatasourceConfigLIGHTLY
        try:
            instance.actual_instance = DatasourceConfigLIGHTLY.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DatasourceConfigS3
        try:
            instance.actual_instance = DatasourceConfigS3.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DatasourceConfigS3DelegatedAccess
        try:
            instance.actual_instance = DatasourceConfigS3DelegatedAccess.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DatasourceConfigGCS
        try:
            instance.actual_instance = DatasourceConfigGCS.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DatasourceConfigAzure
        try:
            instance.actual_instance = DatasourceConfigAzure.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DatasourceConfigOBS
        try:
            instance.actual_instance = DatasourceConfigOBS.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into DatasourceConfigLOCAL
        try:
            instance.actual_instance = DatasourceConfigLOCAL.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into DatasourceConfig with oneOf schemas: DatasourceConfigAzure, DatasourceConfigGCS, DatasourceConfigLIGHTLY, DatasourceConfigLOCAL, DatasourceConfigOBS, DatasourceConfigS3, DatasourceConfigS3DelegatedAccess. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into DatasourceConfig with oneOf schemas: DatasourceConfigAzure, DatasourceConfigGCS, DatasourceConfigLIGHTLY, DatasourceConfigLOCAL, DatasourceConfigOBS, DatasourceConfigS3, DatasourceConfigS3DelegatedAccess. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self, by_alias: bool = False) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        to_json = getattr(self.actual_instance, "to_json", None)
        if callable(to_json):
            return self.actual_instance.to_json(by_alias=by_alias)
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self, by_alias: bool = False) -> dict:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        to_dict = getattr(self.actual_instance, "to_dict", None)
        if callable(to_dict):
            return self.actual_instance.to_dict(by_alias=by_alias)
        else:
            # primitive type
            return self.actual_instance

    def to_str(self, by_alias: bool = False) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.dict(by_alias=by_alias))

