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


class CorporateActionTransitionRequest(object):
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
        'input_transition': 'CorporateActionTransitionComponentRequest',
        'output_transitions': 'list[CorporateActionTransitionComponentRequest]'
    }

    attribute_map = {
        'input_transition': 'inputTransition',
        'output_transitions': 'outputTransitions'
    }

    required_map = {
        'input_transition': 'optional',
        'output_transitions': 'optional'
    }

    def __init__(self, input_transition=None, output_transitions=None, local_vars_configuration=None):  # noqa: E501
        """CorporateActionTransitionRequest - a model defined in OpenAPI"
        
        :param input_transition: 
        :type input_transition: lusid.CorporateActionTransitionComponentRequest
        :param output_transitions: 
        :type output_transitions: list[lusid.CorporateActionTransitionComponentRequest]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._input_transition = None
        self._output_transitions = None
        self.discriminator = None

        if input_transition is not None:
            self.input_transition = input_transition
        self.output_transitions = output_transitions

    @property
    def input_transition(self):
        """Gets the input_transition of this CorporateActionTransitionRequest.  # noqa: E501


        :return: The input_transition of this CorporateActionTransitionRequest.  # noqa: E501
        :rtype: lusid.CorporateActionTransitionComponentRequest
        """
        return self._input_transition

    @input_transition.setter
    def input_transition(self, input_transition):
        """Sets the input_transition of this CorporateActionTransitionRequest.


        :param input_transition: The input_transition of this CorporateActionTransitionRequest.  # noqa: E501
        :type input_transition: lusid.CorporateActionTransitionComponentRequest
        """

        self._input_transition = input_transition

    @property
    def output_transitions(self):
        """Gets the output_transitions of this CorporateActionTransitionRequest.  # noqa: E501


        :return: The output_transitions of this CorporateActionTransitionRequest.  # noqa: E501
        :rtype: list[lusid.CorporateActionTransitionComponentRequest]
        """
        return self._output_transitions

    @output_transitions.setter
    def output_transitions(self, output_transitions):
        """Sets the output_transitions of this CorporateActionTransitionRequest.


        :param output_transitions: The output_transitions of this CorporateActionTransitionRequest.  # noqa: E501
        :type output_transitions: list[lusid.CorporateActionTransitionComponentRequest]
        """

        self._output_transitions = output_transitions

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
        if not isinstance(other, CorporateActionTransitionRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CorporateActionTransitionRequest):
            return True

        return self.to_dict() != other.to_dict()
