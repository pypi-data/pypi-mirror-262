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


class AccessMetadataOperation(object):
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
        'value': 'list[AccessMetadataValue]',
        'path': 'str',
        'op': 'str',
        '_from': 'str'
    }

    attribute_map = {
        'value': 'value',
        'path': 'path',
        'op': 'op',
        '_from': 'from'
    }

    required_map = {
        'value': 'required',
        'path': 'required',
        'op': 'required',
        '_from': 'optional'
    }

    def __init__(self, value=None, path=None, op=None, _from=None, local_vars_configuration=None):  # noqa: E501
        """AccessMetadataOperation - a model defined in OpenAPI"
        
        :param value:  (required)
        :type value: list[lusid.AccessMetadataValue]
        :param path:  (required)
        :type path: str
        :param op:  The available values are: add (required)
        :type op: str
        :param _from: 
        :type _from: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._value = None
        self._path = None
        self._op = None
        self.__from = None
        self.discriminator = None

        self.value = value
        self.path = path
        self.op = op
        self._from = _from

    @property
    def value(self):
        """Gets the value of this AccessMetadataOperation.  # noqa: E501


        :return: The value of this AccessMetadataOperation.  # noqa: E501
        :rtype: list[lusid.AccessMetadataValue]
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this AccessMetadataOperation.


        :param value: The value of this AccessMetadataOperation.  # noqa: E501
        :type value: list[lusid.AccessMetadataValue]
        """
        if self.local_vars_configuration.client_side_validation and value is None:  # noqa: E501
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                value is not None and len(value) < 1):
            raise ValueError("Invalid value for `value`, number of items must be greater than or equal to `1`")  # noqa: E501

        self._value = value

    @property
    def path(self):
        """Gets the path of this AccessMetadataOperation.  # noqa: E501


        :return: The path of this AccessMetadataOperation.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this AccessMetadataOperation.


        :param path: The path of this AccessMetadataOperation.  # noqa: E501
        :type path: str
        """
        if self.local_vars_configuration.client_side_validation and path is None:  # noqa: E501
            raise ValueError("Invalid value for `path`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                path is not None and len(path) > 1025):
            raise ValueError("Invalid value for `path`, length must be less than or equal to `1025`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                path is not None and len(path) < 1):
            raise ValueError("Invalid value for `path`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                path is not None and not re.search(r'^\/.+', path)):  # noqa: E501
            raise ValueError(r"Invalid value for `path`, must be a follow pattern or equal to `/^\/.+/`")  # noqa: E501

        self._path = path

    @property
    def op(self):
        """Gets the op of this AccessMetadataOperation.  # noqa: E501

        The available values are: add  # noqa: E501

        :return: The op of this AccessMetadataOperation.  # noqa: E501
        :rtype: str
        """
        return self._op

    @op.setter
    def op(self, op):
        """Sets the op of this AccessMetadataOperation.

        The available values are: add  # noqa: E501

        :param op: The op of this AccessMetadataOperation.  # noqa: E501
        :type op: str
        """
        if self.local_vars_configuration.client_side_validation and op is None:  # noqa: E501
            raise ValueError("Invalid value for `op`, must not be `None`")  # noqa: E501
        allowed_values = ["add"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and op not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `op` ({0}), must be one of {1}"  # noqa: E501
                .format(op, allowed_values)
            )

        self._op = op

    @property
    def _from(self):
        """Gets the _from of this AccessMetadataOperation.  # noqa: E501


        :return: The _from of this AccessMetadataOperation.  # noqa: E501
        :rtype: str
        """
        return self.__from

    @_from.setter
    def _from(self, _from):
        """Sets the _from of this AccessMetadataOperation.


        :param _from: The _from of this AccessMetadataOperation.  # noqa: E501
        :type _from: str
        """

        self.__from = _from

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
        if not isinstance(other, AccessMetadataOperation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AccessMetadataOperation):
            return True

        return self.to_dict() != other.to_dict()
