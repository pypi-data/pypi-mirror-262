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


class FxLinkedNotionalSchedule(object):
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
        'fx_conventions': 'FxConventions',
        'varying_notional_currency': 'str',
        'varying_notional_fixing_dates': 'RelativeDateOffset',
        'varying_notional_interim_exchange_payment_dates': 'RelativeDateOffset',
        'schedule_type': 'str'
    }

    attribute_map = {
        'fx_conventions': 'fxConventions',
        'varying_notional_currency': 'varyingNotionalCurrency',
        'varying_notional_fixing_dates': 'varyingNotionalFixingDates',
        'varying_notional_interim_exchange_payment_dates': 'varyingNotionalInterimExchangePaymentDates',
        'schedule_type': 'scheduleType'
    }

    required_map = {
        'fx_conventions': 'required',
        'varying_notional_currency': 'required',
        'varying_notional_fixing_dates': 'required',
        'varying_notional_interim_exchange_payment_dates': 'optional',
        'schedule_type': 'required'
    }

    def __init__(self, fx_conventions=None, varying_notional_currency=None, varying_notional_fixing_dates=None, varying_notional_interim_exchange_payment_dates=None, schedule_type=None, local_vars_configuration=None):  # noqa: E501
        """FxLinkedNotionalSchedule - a model defined in OpenAPI"
        
        :param fx_conventions:  (required)
        :type fx_conventions: lusid.FxConventions
        :param varying_notional_currency:  The currency of the varying notional amount. (required)
        :type varying_notional_currency: str
        :param varying_notional_fixing_dates:  (required)
        :type varying_notional_fixing_dates: lusid.RelativeDateOffset
        :param varying_notional_interim_exchange_payment_dates: 
        :type varying_notional_interim_exchange_payment_dates: lusid.RelativeDateOffset
        :param schedule_type:  The available values are: FixedSchedule, FloatSchedule, OptionalitySchedule, StepSchedule, Exercise, FxRateSchedule, FxLinkedNotionalSchedule, Invalid (required)
        :type schedule_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._fx_conventions = None
        self._varying_notional_currency = None
        self._varying_notional_fixing_dates = None
        self._varying_notional_interim_exchange_payment_dates = None
        self._schedule_type = None
        self.discriminator = None

        self.fx_conventions = fx_conventions
        self.varying_notional_currency = varying_notional_currency
        self.varying_notional_fixing_dates = varying_notional_fixing_dates
        if varying_notional_interim_exchange_payment_dates is not None:
            self.varying_notional_interim_exchange_payment_dates = varying_notional_interim_exchange_payment_dates
        self.schedule_type = schedule_type

    @property
    def fx_conventions(self):
        """Gets the fx_conventions of this FxLinkedNotionalSchedule.  # noqa: E501


        :return: The fx_conventions of this FxLinkedNotionalSchedule.  # noqa: E501
        :rtype: lusid.FxConventions
        """
        return self._fx_conventions

    @fx_conventions.setter
    def fx_conventions(self, fx_conventions):
        """Sets the fx_conventions of this FxLinkedNotionalSchedule.


        :param fx_conventions: The fx_conventions of this FxLinkedNotionalSchedule.  # noqa: E501
        :type fx_conventions: lusid.FxConventions
        """
        if self.local_vars_configuration.client_side_validation and fx_conventions is None:  # noqa: E501
            raise ValueError("Invalid value for `fx_conventions`, must not be `None`")  # noqa: E501

        self._fx_conventions = fx_conventions

    @property
    def varying_notional_currency(self):
        """Gets the varying_notional_currency of this FxLinkedNotionalSchedule.  # noqa: E501

        The currency of the varying notional amount.  # noqa: E501

        :return: The varying_notional_currency of this FxLinkedNotionalSchedule.  # noqa: E501
        :rtype: str
        """
        return self._varying_notional_currency

    @varying_notional_currency.setter
    def varying_notional_currency(self, varying_notional_currency):
        """Sets the varying_notional_currency of this FxLinkedNotionalSchedule.

        The currency of the varying notional amount.  # noqa: E501

        :param varying_notional_currency: The varying_notional_currency of this FxLinkedNotionalSchedule.  # noqa: E501
        :type varying_notional_currency: str
        """
        if self.local_vars_configuration.client_side_validation and varying_notional_currency is None:  # noqa: E501
            raise ValueError("Invalid value for `varying_notional_currency`, must not be `None`")  # noqa: E501

        self._varying_notional_currency = varying_notional_currency

    @property
    def varying_notional_fixing_dates(self):
        """Gets the varying_notional_fixing_dates of this FxLinkedNotionalSchedule.  # noqa: E501


        :return: The varying_notional_fixing_dates of this FxLinkedNotionalSchedule.  # noqa: E501
        :rtype: lusid.RelativeDateOffset
        """
        return self._varying_notional_fixing_dates

    @varying_notional_fixing_dates.setter
    def varying_notional_fixing_dates(self, varying_notional_fixing_dates):
        """Sets the varying_notional_fixing_dates of this FxLinkedNotionalSchedule.


        :param varying_notional_fixing_dates: The varying_notional_fixing_dates of this FxLinkedNotionalSchedule.  # noqa: E501
        :type varying_notional_fixing_dates: lusid.RelativeDateOffset
        """
        if self.local_vars_configuration.client_side_validation and varying_notional_fixing_dates is None:  # noqa: E501
            raise ValueError("Invalid value for `varying_notional_fixing_dates`, must not be `None`")  # noqa: E501

        self._varying_notional_fixing_dates = varying_notional_fixing_dates

    @property
    def varying_notional_interim_exchange_payment_dates(self):
        """Gets the varying_notional_interim_exchange_payment_dates of this FxLinkedNotionalSchedule.  # noqa: E501


        :return: The varying_notional_interim_exchange_payment_dates of this FxLinkedNotionalSchedule.  # noqa: E501
        :rtype: lusid.RelativeDateOffset
        """
        return self._varying_notional_interim_exchange_payment_dates

    @varying_notional_interim_exchange_payment_dates.setter
    def varying_notional_interim_exchange_payment_dates(self, varying_notional_interim_exchange_payment_dates):
        """Sets the varying_notional_interim_exchange_payment_dates of this FxLinkedNotionalSchedule.


        :param varying_notional_interim_exchange_payment_dates: The varying_notional_interim_exchange_payment_dates of this FxLinkedNotionalSchedule.  # noqa: E501
        :type varying_notional_interim_exchange_payment_dates: lusid.RelativeDateOffset
        """

        self._varying_notional_interim_exchange_payment_dates = varying_notional_interim_exchange_payment_dates

    @property
    def schedule_type(self):
        """Gets the schedule_type of this FxLinkedNotionalSchedule.  # noqa: E501

        The available values are: FixedSchedule, FloatSchedule, OptionalitySchedule, StepSchedule, Exercise, FxRateSchedule, FxLinkedNotionalSchedule, Invalid  # noqa: E501

        :return: The schedule_type of this FxLinkedNotionalSchedule.  # noqa: E501
        :rtype: str
        """
        return self._schedule_type

    @schedule_type.setter
    def schedule_type(self, schedule_type):
        """Sets the schedule_type of this FxLinkedNotionalSchedule.

        The available values are: FixedSchedule, FloatSchedule, OptionalitySchedule, StepSchedule, Exercise, FxRateSchedule, FxLinkedNotionalSchedule, Invalid  # noqa: E501

        :param schedule_type: The schedule_type of this FxLinkedNotionalSchedule.  # noqa: E501
        :type schedule_type: str
        """
        if self.local_vars_configuration.client_side_validation and schedule_type is None:  # noqa: E501
            raise ValueError("Invalid value for `schedule_type`, must not be `None`")  # noqa: E501
        allowed_values = ["FixedSchedule", "FloatSchedule", "OptionalitySchedule", "StepSchedule", "Exercise", "FxRateSchedule", "FxLinkedNotionalSchedule", "Invalid"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and schedule_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `schedule_type` ({0}), must be one of {1}"  # noqa: E501
                .format(schedule_type, allowed_values)
            )

        self._schedule_type = schedule_type

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
        if not isinstance(other, FxLinkedNotionalSchedule):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FxLinkedNotionalSchedule):
            return True

        return self.to_dict() != other.to_dict()
