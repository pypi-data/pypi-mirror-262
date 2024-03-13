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


class ReconciledTransaction(object):
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
        'left': 'Transaction',
        'right': 'Transaction',
        'percentage_match': 'float',
        'mapping_rule_set_results': 'list[bool]'
    }

    attribute_map = {
        'left': 'left',
        'right': 'right',
        'percentage_match': 'percentageMatch',
        'mapping_rule_set_results': 'mappingRuleSetResults'
    }

    required_map = {
        'left': 'optional',
        'right': 'optional',
        'percentage_match': 'optional',
        'mapping_rule_set_results': 'optional'
    }

    def __init__(self, left=None, right=None, percentage_match=None, mapping_rule_set_results=None, local_vars_configuration=None):  # noqa: E501
        """ReconciledTransaction - a model defined in OpenAPI"
        
        :param left: 
        :type left: lusid.Transaction
        :param right: 
        :type right: lusid.Transaction
        :param percentage_match:  How good a match this is considered to be.
        :type percentage_match: float
        :param mapping_rule_set_results:  The result of each individual mapping rule result.  Will only be present if both Finbourne.WebApi.Interface.Dto.Reconciliation.ReconciledTransaction.Left and Finbourne.WebApi.Interface.Dto.Reconciliation.ReconciledTransaction.Right are populated.
        :type mapping_rule_set_results: list[bool]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._left = None
        self._right = None
        self._percentage_match = None
        self._mapping_rule_set_results = None
        self.discriminator = None

        if left is not None:
            self.left = left
        if right is not None:
            self.right = right
        if percentage_match is not None:
            self.percentage_match = percentage_match
        self.mapping_rule_set_results = mapping_rule_set_results

    @property
    def left(self):
        """Gets the left of this ReconciledTransaction.  # noqa: E501


        :return: The left of this ReconciledTransaction.  # noqa: E501
        :rtype: lusid.Transaction
        """
        return self._left

    @left.setter
    def left(self, left):
        """Sets the left of this ReconciledTransaction.


        :param left: The left of this ReconciledTransaction.  # noqa: E501
        :type left: lusid.Transaction
        """

        self._left = left

    @property
    def right(self):
        """Gets the right of this ReconciledTransaction.  # noqa: E501


        :return: The right of this ReconciledTransaction.  # noqa: E501
        :rtype: lusid.Transaction
        """
        return self._right

    @right.setter
    def right(self, right):
        """Sets the right of this ReconciledTransaction.


        :param right: The right of this ReconciledTransaction.  # noqa: E501
        :type right: lusid.Transaction
        """

        self._right = right

    @property
    def percentage_match(self):
        """Gets the percentage_match of this ReconciledTransaction.  # noqa: E501

        How good a match this is considered to be.  # noqa: E501

        :return: The percentage_match of this ReconciledTransaction.  # noqa: E501
        :rtype: float
        """
        return self._percentage_match

    @percentage_match.setter
    def percentage_match(self, percentage_match):
        """Sets the percentage_match of this ReconciledTransaction.

        How good a match this is considered to be.  # noqa: E501

        :param percentage_match: The percentage_match of this ReconciledTransaction.  # noqa: E501
        :type percentage_match: float
        """

        self._percentage_match = percentage_match

    @property
    def mapping_rule_set_results(self):
        """Gets the mapping_rule_set_results of this ReconciledTransaction.  # noqa: E501

        The result of each individual mapping rule result.  Will only be present if both Finbourne.WebApi.Interface.Dto.Reconciliation.ReconciledTransaction.Left and Finbourne.WebApi.Interface.Dto.Reconciliation.ReconciledTransaction.Right are populated.  # noqa: E501

        :return: The mapping_rule_set_results of this ReconciledTransaction.  # noqa: E501
        :rtype: list[bool]
        """
        return self._mapping_rule_set_results

    @mapping_rule_set_results.setter
    def mapping_rule_set_results(self, mapping_rule_set_results):
        """Sets the mapping_rule_set_results of this ReconciledTransaction.

        The result of each individual mapping rule result.  Will only be present if both Finbourne.WebApi.Interface.Dto.Reconciliation.ReconciledTransaction.Left and Finbourne.WebApi.Interface.Dto.Reconciliation.ReconciledTransaction.Right are populated.  # noqa: E501

        :param mapping_rule_set_results: The mapping_rule_set_results of this ReconciledTransaction.  # noqa: E501
        :type mapping_rule_set_results: list[bool]
        """

        self._mapping_rule_set_results = mapping_rule_set_results

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
        if not isinstance(other, ReconciledTransaction):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReconciledTransaction):
            return True

        return self.to_dict() != other.to_dict()
