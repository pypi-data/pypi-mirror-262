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


class PostingModuleResponse(object):
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
        'posting_module_code': 'str',
        'chart_of_accounts_id': 'ResourceId',
        'display_name': 'str',
        'description': 'str',
        'rules': 'list[PostingModuleRule]',
        'status': 'str',
        'version': 'Version',
        'links': 'list[Link]'
    }

    attribute_map = {
        'href': 'href',
        'posting_module_code': 'postingModuleCode',
        'chart_of_accounts_id': 'chartOfAccountsId',
        'display_name': 'displayName',
        'description': 'description',
        'rules': 'rules',
        'status': 'status',
        'version': 'version',
        'links': 'links'
    }

    required_map = {
        'href': 'optional',
        'posting_module_code': 'required',
        'chart_of_accounts_id': 'required',
        'display_name': 'required',
        'description': 'optional',
        'rules': 'optional',
        'status': 'required',
        'version': 'optional',
        'links': 'optional'
    }

    def __init__(self, href=None, posting_module_code=None, chart_of_accounts_id=None, display_name=None, description=None, rules=None, status=None, version=None, links=None, local_vars_configuration=None):  # noqa: E501
        """PostingModuleResponse - a model defined in OpenAPI"
        
        :param href:  The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.
        :type href: str
        :param posting_module_code:  The code of the Posting Module. (required)
        :type posting_module_code: str
        :param chart_of_accounts_id:  (required)
        :type chart_of_accounts_id: lusid.ResourceId
        :param display_name:  The name of the Posting Module. (required)
        :type display_name: str
        :param description:  A description for the Posting Module.
        :type description: str
        :param rules:  The Posting Rules that apply for the Posting Module. Rules are evaluated in the order they occur in this collection.
        :type rules: list[lusid.PostingModuleRule]
        :param status:  The Posting Module status. Can be Active, Inactive or Deleted. Defaults to Active. (required)
        :type status: str
        :param version: 
        :type version: lusid.Version
        :param links:  Collection of links.
        :type links: list[lusid.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._href = None
        self._posting_module_code = None
        self._chart_of_accounts_id = None
        self._display_name = None
        self._description = None
        self._rules = None
        self._status = None
        self._version = None
        self._links = None
        self.discriminator = None

        self.href = href
        self.posting_module_code = posting_module_code
        self.chart_of_accounts_id = chart_of_accounts_id
        self.display_name = display_name
        self.description = description
        self.rules = rules
        self.status = status
        if version is not None:
            self.version = version
        self.links = links

    @property
    def href(self):
        """Gets the href of this PostingModuleResponse.  # noqa: E501

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :return: The href of this PostingModuleResponse.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this PostingModuleResponse.

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :param href: The href of this PostingModuleResponse.  # noqa: E501
        :type href: str
        """

        self._href = href

    @property
    def posting_module_code(self):
        """Gets the posting_module_code of this PostingModuleResponse.  # noqa: E501

        The code of the Posting Module.  # noqa: E501

        :return: The posting_module_code of this PostingModuleResponse.  # noqa: E501
        :rtype: str
        """
        return self._posting_module_code

    @posting_module_code.setter
    def posting_module_code(self, posting_module_code):
        """Sets the posting_module_code of this PostingModuleResponse.

        The code of the Posting Module.  # noqa: E501

        :param posting_module_code: The posting_module_code of this PostingModuleResponse.  # noqa: E501
        :type posting_module_code: str
        """
        if self.local_vars_configuration.client_side_validation and posting_module_code is None:  # noqa: E501
            raise ValueError("Invalid value for `posting_module_code`, must not be `None`")  # noqa: E501

        self._posting_module_code = posting_module_code

    @property
    def chart_of_accounts_id(self):
        """Gets the chart_of_accounts_id of this PostingModuleResponse.  # noqa: E501


        :return: The chart_of_accounts_id of this PostingModuleResponse.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._chart_of_accounts_id

    @chart_of_accounts_id.setter
    def chart_of_accounts_id(self, chart_of_accounts_id):
        """Sets the chart_of_accounts_id of this PostingModuleResponse.


        :param chart_of_accounts_id: The chart_of_accounts_id of this PostingModuleResponse.  # noqa: E501
        :type chart_of_accounts_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and chart_of_accounts_id is None:  # noqa: E501
            raise ValueError("Invalid value for `chart_of_accounts_id`, must not be `None`")  # noqa: E501

        self._chart_of_accounts_id = chart_of_accounts_id

    @property
    def display_name(self):
        """Gets the display_name of this PostingModuleResponse.  # noqa: E501

        The name of the Posting Module.  # noqa: E501

        :return: The display_name of this PostingModuleResponse.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this PostingModuleResponse.

        The name of the Posting Module.  # noqa: E501

        :param display_name: The display_name of this PostingModuleResponse.  # noqa: E501
        :type display_name: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and len(display_name) < 1):
            raise ValueError("Invalid value for `display_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._display_name = display_name

    @property
    def description(self):
        """Gets the description of this PostingModuleResponse.  # noqa: E501

        A description for the Posting Module.  # noqa: E501

        :return: The description of this PostingModuleResponse.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PostingModuleResponse.

        A description for the Posting Module.  # noqa: E501

        :param description: The description of this PostingModuleResponse.  # noqa: E501
        :type description: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 1024):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 0):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and not re.search(r'^[\s\S]*$', description)):  # noqa: E501
            raise ValueError(r"Invalid value for `description`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._description = description

    @property
    def rules(self):
        """Gets the rules of this PostingModuleResponse.  # noqa: E501

        The Posting Rules that apply for the Posting Module. Rules are evaluated in the order they occur in this collection.  # noqa: E501

        :return: The rules of this PostingModuleResponse.  # noqa: E501
        :rtype: list[lusid.PostingModuleRule]
        """
        return self._rules

    @rules.setter
    def rules(self, rules):
        """Sets the rules of this PostingModuleResponse.

        The Posting Rules that apply for the Posting Module. Rules are evaluated in the order they occur in this collection.  # noqa: E501

        :param rules: The rules of this PostingModuleResponse.  # noqa: E501
        :type rules: list[lusid.PostingModuleRule]
        """

        self._rules = rules

    @property
    def status(self):
        """Gets the status of this PostingModuleResponse.  # noqa: E501

        The Posting Module status. Can be Active, Inactive or Deleted. Defaults to Active.  # noqa: E501

        :return: The status of this PostingModuleResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this PostingModuleResponse.

        The Posting Module status. Can be Active, Inactive or Deleted. Defaults to Active.  # noqa: E501

        :param status: The status of this PostingModuleResponse.  # noqa: E501
        :type status: str
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                status is not None and len(status) < 1):
            raise ValueError("Invalid value for `status`, length must be greater than or equal to `1`")  # noqa: E501

        self._status = status

    @property
    def version(self):
        """Gets the version of this PostingModuleResponse.  # noqa: E501


        :return: The version of this PostingModuleResponse.  # noqa: E501
        :rtype: lusid.Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this PostingModuleResponse.


        :param version: The version of this PostingModuleResponse.  # noqa: E501
        :type version: lusid.Version
        """

        self._version = version

    @property
    def links(self):
        """Gets the links of this PostingModuleResponse.  # noqa: E501

        Collection of links.  # noqa: E501

        :return: The links of this PostingModuleResponse.  # noqa: E501
        :rtype: list[lusid.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this PostingModuleResponse.

        Collection of links.  # noqa: E501

        :param links: The links of this PostingModuleResponse.  # noqa: E501
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
        if not isinstance(other, PostingModuleResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PostingModuleResponse):
            return True

        return self.to_dict() != other.to_dict()
