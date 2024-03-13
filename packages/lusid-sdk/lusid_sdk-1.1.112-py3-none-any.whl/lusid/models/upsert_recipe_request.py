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


class UpsertRecipeRequest(object):
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
        'configuration_recipe': 'ConfigurationRecipe'
    }

    attribute_map = {
        'configuration_recipe': 'configurationRecipe'
    }

    required_map = {
        'configuration_recipe': 'optional'
    }

    def __init__(self, configuration_recipe=None, local_vars_configuration=None):  # noqa: E501
        """UpsertRecipeRequest - a model defined in OpenAPI"
        
        :param configuration_recipe: 
        :type configuration_recipe: lusid.ConfigurationRecipe

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._configuration_recipe = None
        self.discriminator = None

        if configuration_recipe is not None:
            self.configuration_recipe = configuration_recipe

    @property
    def configuration_recipe(self):
        """Gets the configuration_recipe of this UpsertRecipeRequest.  # noqa: E501


        :return: The configuration_recipe of this UpsertRecipeRequest.  # noqa: E501
        :rtype: lusid.ConfigurationRecipe
        """
        return self._configuration_recipe

    @configuration_recipe.setter
    def configuration_recipe(self, configuration_recipe):
        """Sets the configuration_recipe of this UpsertRecipeRequest.


        :param configuration_recipe: The configuration_recipe of this UpsertRecipeRequest.  # noqa: E501
        :type configuration_recipe: lusid.ConfigurationRecipe
        """

        self._configuration_recipe = configuration_recipe

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
        if not isinstance(other, UpsertRecipeRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpsertRecipeRequest):
            return True

        return self.to_dict() != other.to_dict()
