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


class ComponentTransaction(object):
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
        'display_name': 'str',
        'condition': 'str',
        'transaction_field_map': 'TransactionFieldMap',
        'transaction_property_map': 'list[TransactionPropertyMap]'
    }

    attribute_map = {
        'display_name': 'displayName',
        'condition': 'condition',
        'transaction_field_map': 'transactionFieldMap',
        'transaction_property_map': 'transactionPropertyMap'
    }

    required_map = {
        'display_name': 'required',
        'condition': 'optional',
        'transaction_field_map': 'required',
        'transaction_property_map': 'required'
    }

    def __init__(self, display_name=None, condition=None, transaction_field_map=None, transaction_property_map=None, local_vars_configuration=None):  # noqa: E501
        """ComponentTransaction - a model defined in OpenAPI"
        
        :param display_name:  (required)
        :type display_name: str
        :param condition: 
        :type condition: str
        :param transaction_field_map:  (required)
        :type transaction_field_map: lusid.TransactionFieldMap
        :param transaction_property_map:  (required)
        :type transaction_property_map: list[lusid.TransactionPropertyMap]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._display_name = None
        self._condition = None
        self._transaction_field_map = None
        self._transaction_property_map = None
        self.discriminator = None

        self.display_name = display_name
        self.condition = condition
        self.transaction_field_map = transaction_field_map
        self.transaction_property_map = transaction_property_map

    @property
    def display_name(self):
        """Gets the display_name of this ComponentTransaction.  # noqa: E501


        :return: The display_name of this ComponentTransaction.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this ComponentTransaction.


        :param display_name: The display_name of this ComponentTransaction.  # noqa: E501
        :type display_name: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and len(display_name) > 100):
            raise ValueError("Invalid value for `display_name`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and len(display_name) < 0):
            raise ValueError("Invalid value for `display_name`, length must be greater than or equal to `0`")  # noqa: E501

        self._display_name = display_name

    @property
    def condition(self):
        """Gets the condition of this ComponentTransaction.  # noqa: E501


        :return: The condition of this ComponentTransaction.  # noqa: E501
        :rtype: str
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """Sets the condition of this ComponentTransaction.


        :param condition: The condition of this ComponentTransaction.  # noqa: E501
        :type condition: str
        """
        if (self.local_vars_configuration.client_side_validation and
                condition is not None and len(condition) > 1024):
            raise ValueError("Invalid value for `condition`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                condition is not None and len(condition) < 0):
            raise ValueError("Invalid value for `condition`, length must be greater than or equal to `0`")  # noqa: E501

        self._condition = condition

    @property
    def transaction_field_map(self):
        """Gets the transaction_field_map of this ComponentTransaction.  # noqa: E501


        :return: The transaction_field_map of this ComponentTransaction.  # noqa: E501
        :rtype: lusid.TransactionFieldMap
        """
        return self._transaction_field_map

    @transaction_field_map.setter
    def transaction_field_map(self, transaction_field_map):
        """Sets the transaction_field_map of this ComponentTransaction.


        :param transaction_field_map: The transaction_field_map of this ComponentTransaction.  # noqa: E501
        :type transaction_field_map: lusid.TransactionFieldMap
        """
        if self.local_vars_configuration.client_side_validation and transaction_field_map is None:  # noqa: E501
            raise ValueError("Invalid value for `transaction_field_map`, must not be `None`")  # noqa: E501

        self._transaction_field_map = transaction_field_map

    @property
    def transaction_property_map(self):
        """Gets the transaction_property_map of this ComponentTransaction.  # noqa: E501


        :return: The transaction_property_map of this ComponentTransaction.  # noqa: E501
        :rtype: list[lusid.TransactionPropertyMap]
        """
        return self._transaction_property_map

    @transaction_property_map.setter
    def transaction_property_map(self, transaction_property_map):
        """Sets the transaction_property_map of this ComponentTransaction.


        :param transaction_property_map: The transaction_property_map of this ComponentTransaction.  # noqa: E501
        :type transaction_property_map: list[lusid.TransactionPropertyMap]
        """
        if self.local_vars_configuration.client_side_validation and transaction_property_map is None:  # noqa: E501
            raise ValueError("Invalid value for `transaction_property_map`, must not be `None`")  # noqa: E501

        self._transaction_property_map = transaction_property_map

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
        if not isinstance(other, ComponentTransaction):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ComponentTransaction):
            return True

        return self.to_dict() != other.to_dict()
