# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.1.112
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class OrderGraphBlockAllocationSynopsis(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'quantity': 'float',
        'details': 'list[OrderGraphBlockAllocationDetail]'
    }

    attribute_map = {
        'quantity': 'quantity',
        'details': 'details'
    }

    required_map = {
        'quantity': 'required',
        'details': 'required'
    }

    def __init__(self, quantity=None, details=None, local_vars_configuration=None):  # noqa: E501
        """OrderGraphBlockAllocationSynopsis - a model defined in OpenAPI"
        
        :param quantity:  Total number of units allocated. (required)
        :type quantity: float
        :param details:  Identifiers for each allocation in this block. (required)
        :type details: list[lusid.OrderGraphBlockAllocationDetail]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._quantity = None
        self._details = None
        self.discriminator = None

        self.quantity = quantity
        self.details = details

    @property
    def quantity(self):
        """Gets the quantity of this OrderGraphBlockAllocationSynopsis.  # noqa: E501

        Total number of units allocated.  # noqa: E501

        :return: The quantity of this OrderGraphBlockAllocationSynopsis.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this OrderGraphBlockAllocationSynopsis.

        Total number of units allocated.  # noqa: E501

        :param quantity: The quantity of this OrderGraphBlockAllocationSynopsis.  # noqa: E501
        :type quantity: float
        """
        if self.local_vars_configuration.client_side_validation and quantity is None:  # noqa: E501
            raise ValueError("Invalid value for `quantity`, must not be `None`")  # noqa: E501

        self._quantity = quantity

    @property
    def details(self):
        """Gets the details of this OrderGraphBlockAllocationSynopsis.  # noqa: E501

        Identifiers for each allocation in this block.  # noqa: E501

        :return: The details of this OrderGraphBlockAllocationSynopsis.  # noqa: E501
        :rtype: list[lusid.OrderGraphBlockAllocationDetail]
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this OrderGraphBlockAllocationSynopsis.

        Identifiers for each allocation in this block.  # noqa: E501

        :param details: The details of this OrderGraphBlockAllocationSynopsis.  # noqa: E501
        :type details: list[lusid.OrderGraphBlockAllocationDetail]
        """
        if self.local_vars_configuration.client_side_validation and details is None:  # noqa: E501
            raise ValueError("Invalid value for `details`, must not be `None`")  # noqa: E501

        self._details = details

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OrderGraphBlockAllocationSynopsis):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrderGraphBlockAllocationSynopsis):
            return True

        return self.to_dict() != other.to_dict()
