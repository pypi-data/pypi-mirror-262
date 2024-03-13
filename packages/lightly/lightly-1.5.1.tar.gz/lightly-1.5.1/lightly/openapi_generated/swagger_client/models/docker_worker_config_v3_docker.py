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
from pydantic import Extra,  BaseModel, Field, StrictBool, StrictStr, conint, constr, validator
from lightly.openapi_generated.swagger_client.models.docker_worker_config_v3_docker_corruptness_check import DockerWorkerConfigV3DockerCorruptnessCheck
from lightly.openapi_generated.swagger_client.models.docker_worker_config_v3_docker_datasource import DockerWorkerConfigV3DockerDatasource
from lightly.openapi_generated.swagger_client.models.docker_worker_config_v3_docker_training import DockerWorkerConfigV3DockerTraining

class DockerWorkerConfigV3Docker(BaseModel):
    """
    docker run configurations, keys should match the structure of https://github.com/lightly-ai/lightly-core/blob/develop/onprem-docker/lightly_worker/src/lightly_worker/resources/docker/docker.yaml 
    """
    checkpoint: Optional[StrictStr] = None
    checkpoint_run_id: Optional[constr(strict=True)] = Field(None, alias="checkpointRunId", description="MongoDB ObjectId")
    corruptness_check: Optional[DockerWorkerConfigV3DockerCorruptnessCheck] = Field(None, alias="corruptnessCheck")
    datasource: Optional[DockerWorkerConfigV3DockerDatasource] = None
    embeddings: Optional[StrictStr] = None
    enable_training: Optional[StrictBool] = Field(None, alias="enableTraining")
    training: Optional[DockerWorkerConfigV3DockerTraining] = None
    normalize_embeddings: Optional[StrictBool] = Field(None, alias="normalizeEmbeddings")
    num_processes: Optional[conint(strict=True, ge=-1)] = Field(None, alias="numProcesses")
    num_threads: Optional[conint(strict=True, ge=-1)] = Field(None, alias="numThreads")
    output_image_format: Optional[StrictStr] = Field(None, alias="outputImageFormat")
    pretagging: Optional[StrictBool] = None
    pretagging_upload: Optional[StrictBool] = Field(None, alias="pretaggingUpload")
    relevant_filenames_file: Optional[StrictStr] = Field(None, alias="relevantFilenamesFile")
    selected_sequence_length: Optional[conint(strict=True, ge=1)] = Field(None, alias="selectedSequenceLength")
    upload_report: Optional[StrictBool] = Field(None, alias="uploadReport")
    shutdown_when_job_finished: Optional[StrictBool] = Field(None, alias="shutdownWhenJobFinished")
    __properties = ["checkpoint", "checkpointRunId", "corruptnessCheck", "datasource", "embeddings", "enableTraining", "training", "normalizeEmbeddings", "numProcesses", "numThreads", "outputImageFormat", "pretagging", "pretaggingUpload", "relevantFilenamesFile", "selectedSequenceLength", "uploadReport", "shutdownWhenJobFinished"]

    @validator('checkpoint_run_id')
    def checkpoint_run_id_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-f0-9]{24}$", value):
            raise ValueError(r"must validate the regular expression /^[a-f0-9]{24}$/")
        return value

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
    def from_json(cls, json_str: str) -> DockerWorkerConfigV3Docker:
        """Create an instance of DockerWorkerConfigV3Docker from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self, by_alias: bool = False):
        """Returns the dictionary representation of the model"""
        _dict = self.dict(by_alias=by_alias,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of corruptness_check
        if self.corruptness_check:
            _dict['corruptnessCheck' if by_alias else 'corruptness_check'] = self.corruptness_check.to_dict(by_alias=by_alias)
        # override the default output from pydantic by calling `to_dict()` of datasource
        if self.datasource:
            _dict['datasource' if by_alias else 'datasource'] = self.datasource.to_dict(by_alias=by_alias)
        # override the default output from pydantic by calling `to_dict()` of training
        if self.training:
            _dict['training' if by_alias else 'training'] = self.training.to_dict(by_alias=by_alias)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DockerWorkerConfigV3Docker:
        """Create an instance of DockerWorkerConfigV3Docker from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DockerWorkerConfigV3Docker.parse_obj(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in DockerWorkerConfigV3Docker) in the input: " + str(obj))

        _obj = DockerWorkerConfigV3Docker.parse_obj({
            "checkpoint": obj.get("checkpoint"),
            "checkpoint_run_id": obj.get("checkpointRunId"),
            "corruptness_check": DockerWorkerConfigV3DockerCorruptnessCheck.from_dict(obj.get("corruptnessCheck")) if obj.get("corruptnessCheck") is not None else None,
            "datasource": DockerWorkerConfigV3DockerDatasource.from_dict(obj.get("datasource")) if obj.get("datasource") is not None else None,
            "embeddings": obj.get("embeddings"),
            "enable_training": obj.get("enableTraining"),
            "training": DockerWorkerConfigV3DockerTraining.from_dict(obj.get("training")) if obj.get("training") is not None else None,
            "normalize_embeddings": obj.get("normalizeEmbeddings"),
            "num_processes": obj.get("numProcesses"),
            "num_threads": obj.get("numThreads"),
            "output_image_format": obj.get("outputImageFormat"),
            "pretagging": obj.get("pretagging"),
            "pretagging_upload": obj.get("pretaggingUpload"),
            "relevant_filenames_file": obj.get("relevantFilenamesFile"),
            "selected_sequence_length": obj.get("selectedSequenceLength"),
            "upload_report": obj.get("uploadReport"),
            "shutdown_when_job_finished": obj.get("shutdownWhenJobFinished")
        })
        return _obj

