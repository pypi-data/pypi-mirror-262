# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, conlist, constr
from finbourne_access.models.entitlement_metadata import EntitlementMetadata
from finbourne_access.models.policy_collection_id import PolicyCollectionId
from finbourne_access.models.policy_id import PolicyId

class PolicyCollectionUpdateRequest(BaseModel):
    """
    Update an existing PolicyCollection  # noqa: E501
    """
    policies: Optional[conlist(PolicyId)] = Field(None, description="The identifiers of the Policies in this collection")
    metadata: Optional[Dict[str, conlist(EntitlementMetadata)]] = Field(None, description="Any relevant metadata associated with this resource for controlling access to this resource")
    policy_collections: Optional[conlist(PolicyCollectionId)] = Field(None, alias="policyCollections", description="The identifiers of the PolicyCollections in this collection")
    description: Optional[constr(strict=True, max_length=1024, min_length=0)] = Field(None, description="A description of this policy collection")
    __properties = ["policies", "metadata", "policyCollections", "description"]

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
    def from_json(cls, json_str: str) -> PolicyCollectionUpdateRequest:
        """Create an instance of PolicyCollectionUpdateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in policies (list)
        _items = []
        if self.policies:
            for _item in self.policies:
                if _item:
                    _items.append(_item.to_dict())
            _dict['policies'] = _items
        # override the default output from pydantic by calling `to_dict()` of each value in metadata (dict of array)
        _field_dict_of_array = {}
        if self.metadata:
            for _key in self.metadata:
                if self.metadata[_key]:
                    _field_dict_of_array[_key] = [
                        _item.to_dict() for _item in self.metadata[_key]
                    ]
            _dict['metadata'] = _field_dict_of_array
        # override the default output from pydantic by calling `to_dict()` of each item in policy_collections (list)
        _items = []
        if self.policy_collections:
            for _item in self.policy_collections:
                if _item:
                    _items.append(_item.to_dict())
            _dict['policyCollections'] = _items
        # set to None if policies (nullable) is None
        # and __fields_set__ contains the field
        if self.policies is None and "policies" in self.__fields_set__:
            _dict['policies'] = None

        # set to None if metadata (nullable) is None
        # and __fields_set__ contains the field
        if self.metadata is None and "metadata" in self.__fields_set__:
            _dict['metadata'] = None

        # set to None if policy_collections (nullable) is None
        # and __fields_set__ contains the field
        if self.policy_collections is None and "policy_collections" in self.__fields_set__:
            _dict['policyCollections'] = None

        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PolicyCollectionUpdateRequest:
        """Create an instance of PolicyCollectionUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PolicyCollectionUpdateRequest.parse_obj(obj)

        _obj = PolicyCollectionUpdateRequest.parse_obj({
            "policies": [PolicyId.from_dict(_item) for _item in obj.get("policies")] if obj.get("policies") is not None else None,
            "metadata": dict(
                (_k,
                        [EntitlementMetadata.from_dict(_item) for _item in _v]
                        if _v is not None
                        else None
                )
                for _k, _v in obj.get("metadata").items()
            ),
            "policy_collections": [PolicyCollectionId.from_dict(_item) for _item in obj.get("policyCollections")] if obj.get("policyCollections") is not None else None,
            "description": obj.get("description")
        })
        return _obj
