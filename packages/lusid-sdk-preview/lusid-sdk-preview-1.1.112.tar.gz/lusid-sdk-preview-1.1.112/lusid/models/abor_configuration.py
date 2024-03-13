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


class AborConfiguration(object):
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
        'href': 'str',
        'id': 'ResourceId',
        'display_name': 'str',
        'description': 'str',
        'recipe_id': 'ResourceId',
        'chart_of_accounts_id': 'ResourceId',
        'posting_module_codes': 'list[str]',
        'cleardown_module_codes': 'list[str]',
        'properties': 'dict(str, ModelProperty)',
        'version': 'Version',
        'links': 'list[Link]'
    }

    attribute_map = {
        'href': 'href',
        'id': 'id',
        'display_name': 'displayName',
        'description': 'description',
        'recipe_id': 'recipeId',
        'chart_of_accounts_id': 'chartOfAccountsId',
        'posting_module_codes': 'postingModuleCodes',
        'cleardown_module_codes': 'cleardownModuleCodes',
        'properties': 'properties',
        'version': 'version',
        'links': 'links'
    }

    required_map = {
        'href': 'optional',
        'id': 'required',
        'display_name': 'optional',
        'description': 'optional',
        'recipe_id': 'optional',
        'chart_of_accounts_id': 'required',
        'posting_module_codes': 'optional',
        'cleardown_module_codes': 'optional',
        'properties': 'optional',
        'version': 'optional',
        'links': 'optional'
    }

    def __init__(self, href=None, id=None, display_name=None, description=None, recipe_id=None, chart_of_accounts_id=None, posting_module_codes=None, cleardown_module_codes=None, properties=None, version=None, links=None, local_vars_configuration=None):  # noqa: E501
        """AborConfiguration - a model defined in OpenAPI"
        
        :param href:  The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.
        :type href: str
        :param id:  (required)
        :type id: lusid.ResourceId
        :param display_name:  The name of the Abor Configuration.
        :type display_name: str
        :param description:  A description for the Abor Configuration.
        :type description: str
        :param recipe_id: 
        :type recipe_id: lusid.ResourceId
        :param chart_of_accounts_id:  (required)
        :type chart_of_accounts_id: lusid.ResourceId
        :param posting_module_codes:  The Posting Module Codes from which the rules to be applied are retrieved.
        :type posting_module_codes: list[str]
        :param cleardown_module_codes:  The Cleardown Module Codes from which the rules to be applied are retrieved.
        :type cleardown_module_codes: list[str]
        :param properties:  A set of properties for the Abor Configuration.
        :type properties: dict[str, lusid.ModelProperty]
        :param version: 
        :type version: lusid.Version
        :param links:  Collection of links.
        :type links: list[lusid.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._href = None
        self._id = None
        self._display_name = None
        self._description = None
        self._recipe_id = None
        self._chart_of_accounts_id = None
        self._posting_module_codes = None
        self._cleardown_module_codes = None
        self._properties = None
        self._version = None
        self._links = None
        self.discriminator = None

        self.href = href
        self.id = id
        self.display_name = display_name
        self.description = description
        if recipe_id is not None:
            self.recipe_id = recipe_id
        self.chart_of_accounts_id = chart_of_accounts_id
        self.posting_module_codes = posting_module_codes
        self.cleardown_module_codes = cleardown_module_codes
        self.properties = properties
        if version is not None:
            self.version = version
        self.links = links

    @property
    def href(self):
        """Gets the href of this AborConfiguration.  # noqa: E501

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :return: The href of this AborConfiguration.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this AborConfiguration.

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :param href: The href of this AborConfiguration.  # noqa: E501
        :type href: str
        """

        self._href = href

    @property
    def id(self):
        """Gets the id of this AborConfiguration.  # noqa: E501


        :return: The id of this AborConfiguration.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AborConfiguration.


        :param id: The id of this AborConfiguration.  # noqa: E501
        :type id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def display_name(self):
        """Gets the display_name of this AborConfiguration.  # noqa: E501

        The name of the Abor Configuration.  # noqa: E501

        :return: The display_name of this AborConfiguration.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this AborConfiguration.

        The name of the Abor Configuration.  # noqa: E501

        :param display_name: The display_name of this AborConfiguration.  # noqa: E501
        :type display_name: str
        """

        self._display_name = display_name

    @property
    def description(self):
        """Gets the description of this AborConfiguration.  # noqa: E501

        A description for the Abor Configuration.  # noqa: E501

        :return: The description of this AborConfiguration.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AborConfiguration.

        A description for the Abor Configuration.  # noqa: E501

        :param description: The description of this AborConfiguration.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def recipe_id(self):
        """Gets the recipe_id of this AborConfiguration.  # noqa: E501


        :return: The recipe_id of this AborConfiguration.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._recipe_id

    @recipe_id.setter
    def recipe_id(self, recipe_id):
        """Sets the recipe_id of this AborConfiguration.


        :param recipe_id: The recipe_id of this AborConfiguration.  # noqa: E501
        :type recipe_id: lusid.ResourceId
        """

        self._recipe_id = recipe_id

    @property
    def chart_of_accounts_id(self):
        """Gets the chart_of_accounts_id of this AborConfiguration.  # noqa: E501


        :return: The chart_of_accounts_id of this AborConfiguration.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._chart_of_accounts_id

    @chart_of_accounts_id.setter
    def chart_of_accounts_id(self, chart_of_accounts_id):
        """Sets the chart_of_accounts_id of this AborConfiguration.


        :param chart_of_accounts_id: The chart_of_accounts_id of this AborConfiguration.  # noqa: E501
        :type chart_of_accounts_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and chart_of_accounts_id is None:  # noqa: E501
            raise ValueError("Invalid value for `chart_of_accounts_id`, must not be `None`")  # noqa: E501

        self._chart_of_accounts_id = chart_of_accounts_id

    @property
    def posting_module_codes(self):
        """Gets the posting_module_codes of this AborConfiguration.  # noqa: E501

        The Posting Module Codes from which the rules to be applied are retrieved.  # noqa: E501

        :return: The posting_module_codes of this AborConfiguration.  # noqa: E501
        :rtype: list[str]
        """
        return self._posting_module_codes

    @posting_module_codes.setter
    def posting_module_codes(self, posting_module_codes):
        """Sets the posting_module_codes of this AborConfiguration.

        The Posting Module Codes from which the rules to be applied are retrieved.  # noqa: E501

        :param posting_module_codes: The posting_module_codes of this AborConfiguration.  # noqa: E501
        :type posting_module_codes: list[str]
        """

        self._posting_module_codes = posting_module_codes

    @property
    def cleardown_module_codes(self):
        """Gets the cleardown_module_codes of this AborConfiguration.  # noqa: E501

        The Cleardown Module Codes from which the rules to be applied are retrieved.  # noqa: E501

        :return: The cleardown_module_codes of this AborConfiguration.  # noqa: E501
        :rtype: list[str]
        """
        return self._cleardown_module_codes

    @cleardown_module_codes.setter
    def cleardown_module_codes(self, cleardown_module_codes):
        """Sets the cleardown_module_codes of this AborConfiguration.

        The Cleardown Module Codes from which the rules to be applied are retrieved.  # noqa: E501

        :param cleardown_module_codes: The cleardown_module_codes of this AborConfiguration.  # noqa: E501
        :type cleardown_module_codes: list[str]
        """

        self._cleardown_module_codes = cleardown_module_codes

    @property
    def properties(self):
        """Gets the properties of this AborConfiguration.  # noqa: E501

        A set of properties for the Abor Configuration.  # noqa: E501

        :return: The properties of this AborConfiguration.  # noqa: E501
        :rtype: dict[str, lusid.ModelProperty]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this AborConfiguration.

        A set of properties for the Abor Configuration.  # noqa: E501

        :param properties: The properties of this AborConfiguration.  # noqa: E501
        :type properties: dict[str, lusid.ModelProperty]
        """

        self._properties = properties

    @property
    def version(self):
        """Gets the version of this AborConfiguration.  # noqa: E501


        :return: The version of this AborConfiguration.  # noqa: E501
        :rtype: lusid.Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this AborConfiguration.


        :param version: The version of this AborConfiguration.  # noqa: E501
        :type version: lusid.Version
        """

        self._version = version

    @property
    def links(self):
        """Gets the links of this AborConfiguration.  # noqa: E501

        Collection of links.  # noqa: E501

        :return: The links of this AborConfiguration.  # noqa: E501
        :rtype: list[lusid.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this AborConfiguration.

        Collection of links.  # noqa: E501

        :param links: The links of this AborConfiguration.  # noqa: E501
        :type links: list[lusid.Link]
        """

        self._links = links

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
        if not isinstance(other, AborConfiguration):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AborConfiguration):
            return True

        return self.to_dict() != other.to_dict()
