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


class BlockAndOrders(object):
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
        'orders': 'list[Order]'
    }

    attribute_map = {
        'block': 'block',
        'orders': 'orders'
    }

    required_map = {
        'block': 'required',
        'orders': 'required'
    }

    def __init__(self, block=None, orders=None, local_vars_configuration=None):  # noqa: E501
        """BlockAndOrders - a model defined in OpenAPI"
        
        :param block:  (required)
        :type block: lusid.Block
        :param orders:  (required)
        :type orders: list[lusid.Order]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._block = None
        self._orders = None
        self.discriminator = None

        self.block = block
        self.orders = orders

    @property
    def block(self):
        """Gets the block of this BlockAndOrders.  # noqa: E501


        :return: The block of this BlockAndOrders.  # noqa: E501
        :rtype: lusid.Block
        """
        return self._block

    @block.setter
    def block(self, block):
        """Sets the block of this BlockAndOrders.


        :param block: The block of this BlockAndOrders.  # noqa: E501
        :type block: lusid.Block
        """
        if self.local_vars_configuration.client_side_validation and block is None:  # noqa: E501
            raise ValueError("Invalid value for `block`, must not be `None`")  # noqa: E501

        self._block = block

    @property
    def orders(self):
        """Gets the orders of this BlockAndOrders.  # noqa: E501


        :return: The orders of this BlockAndOrders.  # noqa: E501
        :rtype: list[lusid.Order]
        """
        return self._orders

    @orders.setter
    def orders(self, orders):
        """Sets the orders of this BlockAndOrders.


        :param orders: The orders of this BlockAndOrders.  # noqa: E501
        :type orders: list[lusid.Order]
        """
        if self.local_vars_configuration.client_side_validation and orders is None:  # noqa: E501
            raise ValueError("Invalid value for `orders`, must not be `None`")  # noqa: E501

        self._orders = orders

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
        if not isinstance(other, BlockAndOrders):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BlockAndOrders):
            return True

        return self.to_dict() != other.to_dict()
