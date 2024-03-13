# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetBucketResult',
    'AwaitableGetBucketResult',
    'get_bucket',
    'get_bucket_output',
]

@pulumi.output_type
class GetBucketResult:
    """
    A collection of values returned by getBucket.
    """
    def __init__(__self__, created_at=None, description=None, id=None, name=None, org_id=None, retention_period=None, type=None, updated_at=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)
        if retention_period and not isinstance(retention_period, int):
            raise TypeError("Expected argument 'retention_period' to be a int")
        pulumi.set(__self__, "retention_period", retention_period)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Bucket creation date.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        A description of the bucket.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        A Bucket ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A Bucket name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> str:
        """
        An organization ID.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> int:
        """
        The duration in seconds for how long data will be kept in the database. `0` represents infinite retention.
        """
        return pulumi.get(self, "retention_period")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The Bucket type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        Last bucket update date.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetBucketResult(GetBucketResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBucketResult(
            created_at=self.created_at,
            description=self.description,
            id=self.id,
            name=self.name,
            org_id=self.org_id,
            retention_period=self.retention_period,
            type=self.type,
            updated_at=self.updated_at)


def get_bucket(name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBucketResult:
    """
    Retrieves a bucket. Use this data source to retrieve information for a specific bucket.


    :param str name: A Bucket name.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('influxdb:index/getBucket:getBucket', __args__, opts=opts, typ=GetBucketResult).value

    return AwaitableGetBucketResult(
        created_at=pulumi.get(__ret__, 'created_at'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        org_id=pulumi.get(__ret__, 'org_id'),
        retention_period=pulumi.get(__ret__, 'retention_period'),
        type=pulumi.get(__ret__, 'type'),
        updated_at=pulumi.get(__ret__, 'updated_at'))


@_utilities.lift_output_func(get_bucket)
def get_bucket_output(name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBucketResult]:
    """
    Retrieves a bucket. Use this data source to retrieve information for a specific bucket.


    :param str name: A Bucket name.
    """
    ...
