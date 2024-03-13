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


class OrderGraphBlock(object):
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
        'block': 'Block',
        'ordered': 'OrderGraphBlockOrderSynopsis',
        'placed': 'OrderGraphBlockPlacementSynopsis',
        'executed': 'OrderGraphBlockExecutionSynopsis',
        'allocated': 'OrderGraphBlockAllocationSynopsis',
        'derived_state': 'str',
        'derived_compliance_state': 'str',
        'derived_approval_state': 'str'
    }

    attribute_map = {
        'block': 'block',
        'ordered': 'ordered',
        'placed': 'placed',
        'executed': 'executed',
        'allocated': 'allocated',
        'derived_state': 'derivedState',
        'derived_compliance_state': 'derivedComplianceState',
        'derived_approval_state': 'derivedApprovalState'
    }

    required_map = {
        'block': 'required',
        'ordered': 'required',
        'placed': 'required',
        'executed': 'required',
        'allocated': 'required',
        'derived_state': 'required',
        'derived_compliance_state': 'required',
        'derived_approval_state': 'required'
    }

    def __init__(self, block=None, ordered=None, placed=None, executed=None, allocated=None, derived_state=None, derived_compliance_state=None, derived_approval_state=None, local_vars_configuration=None):  # noqa: E501
        """OrderGraphBlock - a model defined in OpenAPI"
        
        :param block:  (required)
        :type block: lusid.Block
        :param ordered:  (required)
        :type ordered: lusid.OrderGraphBlockOrderSynopsis
        :param placed:  (required)
        :type placed: lusid.OrderGraphBlockPlacementSynopsis
        :param executed:  (required)
        :type executed: lusid.OrderGraphBlockExecutionSynopsis
        :param allocated:  (required)
        :type allocated: lusid.OrderGraphBlockAllocationSynopsis
        :param derived_state:  A simple description of the overall state of a block. (required)
        :type derived_state: str
        :param derived_compliance_state:  The overall compliance state of a block, derived from the block's orders. Possible values are 'Pending', 'Failed', 'Manually approved' and 'Passed'. (required)
        :type derived_compliance_state: str
        :param derived_approval_state:  The overall approval state of a block, derived from approval of the block's orders. Possible values are 'Pending', 'Approved' and 'Rejected'. (required)
        :type derived_approval_state: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._block = None
        self._ordered = None
        self._placed = None
        self._executed = None
        self._allocated = None
        self._derived_state = None
        self._derived_compliance_state = None
        self._derived_approval_state = None
        self.discriminator = None

        self.block = block
        self.ordered = ordered
        self.placed = placed
        self.executed = executed
        self.allocated = allocated
        self.derived_state = derived_state
        self.derived_compliance_state = derived_compliance_state
        self.derived_approval_state = derived_approval_state

    @property
    def block(self):
        """Gets the block of this OrderGraphBlock.  # noqa: E501


        :return: The block of this OrderGraphBlock.  # noqa: E501
        :rtype: lusid.Block
        """
        return self._block

    @block.setter
    def block(self, block):
        """Sets the block of this OrderGraphBlock.


        :param block: The block of this OrderGraphBlock.  # noqa: E501
        :type block: lusid.Block
        """
        if self.local_vars_configuration.client_side_validation and block is None:  # noqa: E501
            raise ValueError("Invalid value for `block`, must not be `None`")  # noqa: E501

        self._block = block

    @property
    def ordered(self):
        """Gets the ordered of this OrderGraphBlock.  # noqa: E501


        :return: The ordered of this OrderGraphBlock.  # noqa: E501
        :rtype: lusid.OrderGraphBlockOrderSynopsis
        """
        return self._ordered

    @ordered.setter
    def ordered(self, ordered):
        """Sets the ordered of this OrderGraphBlock.


        :param ordered: The ordered of this OrderGraphBlock.  # noqa: E501
        :type ordered: lusid.OrderGraphBlockOrderSynopsis
        """
        if self.local_vars_configuration.client_side_validation and ordered is None:  # noqa: E501
            raise ValueError("Invalid value for `ordered`, must not be `None`")  # noqa: E501

        self._ordered = ordered

    @property
    def placed(self):
        """Gets the placed of this OrderGraphBlock.  # noqa: E501


        :return: The placed of this OrderGraphBlock.  # noqa: E501
        :rtype: lusid.OrderGraphBlockPlacementSynopsis
        """
        return self._placed

    @placed.setter
    def placed(self, placed):
        """Sets the placed of this OrderGraphBlock.


        :param placed: The placed of this OrderGraphBlock.  # noqa: E501
        :type placed: lusid.OrderGraphBlockPlacementSynopsis
        """
        if self.local_vars_configuration.client_side_validation and placed is None:  # noqa: E501
            raise ValueError("Invalid value for `placed`, must not be `None`")  # noqa: E501

        self._placed = placed

    @property
    def executed(self):
        """Gets the executed of this OrderGraphBlock.  # noqa: E501


        :return: The executed of this OrderGraphBlock.  # noqa: E501
        :rtype: lusid.OrderGraphBlockExecutionSynopsis
        """
        return self._executed

    @executed.setter
    def executed(self, executed):
        """Sets the executed of this OrderGraphBlock.


        :param executed: The executed of this OrderGraphBlock.  # noqa: E501
        :type executed: lusid.OrderGraphBlockExecutionSynopsis
        """
        if self.local_vars_configuration.client_side_validation and executed is None:  # noqa: E501
            raise ValueError("Invalid value for `executed`, must not be `None`")  # noqa: E501

        self._executed = executed

    @property
    def allocated(self):
        """Gets the allocated of this OrderGraphBlock.  # noqa: E501


        :return: The allocated of this OrderGraphBlock.  # noqa: E501
        :rtype: lusid.OrderGraphBlockAllocationSynopsis
        """
        return self._allocated

    @allocated.setter
    def allocated(self, allocated):
        """Sets the allocated of this OrderGraphBlock.


        :param allocated: The allocated of this OrderGraphBlock.  # noqa: E501
        :type allocated: lusid.OrderGraphBlockAllocationSynopsis
        """
        if self.local_vars_configuration.client_side_validation and allocated is None:  # noqa: E501
            raise ValueError("Invalid value for `allocated`, must not be `None`")  # noqa: E501

        self._allocated = allocated

    @property
    def derived_state(self):
        """Gets the derived_state of this OrderGraphBlock.  # noqa: E501

        A simple description of the overall state of a block.  # noqa: E501

        :return: The derived_state of this OrderGraphBlock.  # noqa: E501
        :rtype: str
        """
        return self._derived_state

    @derived_state.setter
    def derived_state(self, derived_state):
        """Sets the derived_state of this OrderGraphBlock.

        A simple description of the overall state of a block.  # noqa: E501

        :param derived_state: The derived_state of this OrderGraphBlock.  # noqa: E501
        :type derived_state: str
        """
        if self.local_vars_configuration.client_side_validation and derived_state is None:  # noqa: E501
            raise ValueError("Invalid value for `derived_state`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                derived_state is not None and len(derived_state) < 1):
            raise ValueError("Invalid value for `derived_state`, length must be greater than or equal to `1`")  # noqa: E501

        self._derived_state = derived_state

    @property
    def derived_compliance_state(self):
        """Gets the derived_compliance_state of this OrderGraphBlock.  # noqa: E501

        The overall compliance state of a block, derived from the block's orders. Possible values are 'Pending', 'Failed', 'Manually approved' and 'Passed'.  # noqa: E501

        :return: The derived_compliance_state of this OrderGraphBlock.  # noqa: E501
        :rtype: str
        """
        return self._derived_compliance_state

    @derived_compliance_state.setter
    def derived_compliance_state(self, derived_compliance_state):
        """Sets the derived_compliance_state of this OrderGraphBlock.

        The overall compliance state of a block, derived from the block's orders. Possible values are 'Pending', 'Failed', 'Manually approved' and 'Passed'.  # noqa: E501

        :param derived_compliance_state: The derived_compliance_state of this OrderGraphBlock.  # noqa: E501
        :type derived_compliance_state: str
        """
        if self.local_vars_configuration.client_side_validation and derived_compliance_state is None:  # noqa: E501
            raise ValueError("Invalid value for `derived_compliance_state`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                derived_compliance_state is not None and len(derived_compliance_state) < 1):
            raise ValueError("Invalid value for `derived_compliance_state`, length must be greater than or equal to `1`")  # noqa: E501

        self._derived_compliance_state = derived_compliance_state

    @property
    def derived_approval_state(self):
        """Gets the derived_approval_state of this OrderGraphBlock.  # noqa: E501

        The overall approval state of a block, derived from approval of the block's orders. Possible values are 'Pending', 'Approved' and 'Rejected'.  # noqa: E501

        :return: The derived_approval_state of this OrderGraphBlock.  # noqa: E501
        :rtype: str
        """
        return self._derived_approval_state

    @derived_approval_state.setter
    def derived_approval_state(self, derived_approval_state):
        """Sets the derived_approval_state of this OrderGraphBlock.

        The overall approval state of a block, derived from approval of the block's orders. Possible values are 'Pending', 'Approved' and 'Rejected'.  # noqa: E501

        :param derived_approval_state: The derived_approval_state of this OrderGraphBlock.  # noqa: E501
        :type derived_approval_state: str
        """
        if self.local_vars_configuration.client_side_validation and derived_approval_state is None:  # noqa: E501
            raise ValueError("Invalid value for `derived_approval_state`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                derived_approval_state is not None and len(derived_approval_state) < 1):
            raise ValueError("Invalid value for `derived_approval_state`, length must be greater than or equal to `1`")  # noqa: E501

        self._derived_approval_state = derived_approval_state

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
        if not isinstance(other, OrderGraphBlock):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrderGraphBlock):
            return True

        return self.to_dict() != other.to_dict()
