# coding: utf-8

"""
    FINBOURNE Horizon API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict
from pydantic import BaseModel, Field, StrictStr

class AuditCompleteResponse(BaseModel):
    """
    Response type for Horizon Audit Event  # noqa: E501
    """
    process_name: StrictStr = Field(..., alias="processName", description="The name of the Process the events will be visible under")
    __properties = ["processName"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AuditCompleteResponse:
        """Create an instance of AuditCompleteResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AuditCompleteResponse:
        """Create an instance of AuditCompleteResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AuditCompleteResponse.parse_obj(obj)

        _obj = AuditCompleteResponse.parse_obj({
            "process_name": obj.get("processName")
        })
        return _obj
