import os

import requests
import logging
import yaml

class Space:
    """Encapsulates a Junos Space cluster and provides access to all RESTful
    web-service APIs provided by Space. An instance of this class is also
    referred to as a *'rest end point'* in this documentation.
    """

    def __init__(self, url, user, passwd):
        """Creates an instance of this class to represent a Junos Space cluster.

        :param url: URL of the Junos Space cluster using its VIP address.
                    E.g. https://<VIP>
        :type url: str
        :param user: A valid userid for invoking APIs on this Space cluster.
        :type user: str
        :param passwd: Password for the userid.
        :type passwd: str

        :returns:  An instance of this class encapsulating the Junos Space
                   cluster whose **url** was given as a parameter. It can be
                   used to access all APIs provided by Space.
        """
        self.space_url = url
        self.space_user = user
        self.space_passwd = passwd
        self._logger = logging.getLogger('root')
        self._meta_services = self._init_services()
        self._services = {}

    def __str__(self):
        return ' '.join(['Space <',
                       '@'.join([self.space_user, self.space_url]),
                       '>'])

    def _init_services(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        with open(dir_path + '/descriptions/services.yml') as f:
            return yaml.load(f)['services']

    def __getattr__(self, attr):
        if attr in self._services:
            return self._services[attr]

        if attr in self._meta_services:
            from jnpr.space import service
            value = self._meta_services[attr]
            self._services[attr] = service.Service(self, attr, value)
            return self._services[attr]

        raise AttributeError("No attribute '%s'" % attr)

    def get(self, url, headers={}):
        """Performs an HTTP GET on the given url. Acts as a wrapper over
        requests.get() function.

        :param str url: URL for performing GET
        :param dict headers: A dict with the headers that need to be sent with
            the GET request. Defaults to ``{}``.

        :returns:  The response object (`requests.Response <http://docs.python-requests.org/en/latest/api/#requests.Response />`_)
                   returned by the GET request.
        """
        req_url = self.space_url + url
        self._logger.debug("GET %s" % req_url)
        self._logger.debug(headers)
        r = requests.get(req_url, auth=(self.space_user, self.space_passwd), headers=headers, verify=False)
        self._logger.debug(r)
        self._logger.debug(r.text)
        return r

    def head(self, url, headers={}):
        """Performs an HTTP HEAD on the given url. Acts as a wrapper over
        requests.head() function.

        :param str url: URL for performing HEAD
        :param dict headers: A dict with the headers that need to be sent with
            the HEAD request. Defaults to ``{}``.

        :returns:  The response object (`requests.Response <http://docs.python-requests.org/en/latest/api/#requests.Response />`_)
            returned by the HEAD request.
        """
        req_url = self.space_url + url
        self._logger.debug("HEAD %s" % req_url)
        self._logger.debug(headers)
        r = requests.head(req_url, auth=(self.space_user, self.space_passwd), headers=headers, verify=False)
        self._logger.debug(r)
        self._logger.debug(r.headers)
        self._logger.debug(r.text)
        return r

    def post(self, url, headers, body):
        """Performs an HTTP POST on the given url. Acts as a wrapper over
        requests.post() function.

        :param str url: URL for performing POST
        :param dict headers: A dict with the headers that need to be sent with
            the POST request. This is a mandatory parameter.
        :param str body: A string that forms the body of the POST request.
            This is a mandatory parameter.

        :returns:  The response object (`requests.Response <http://docs.python-requests.org/en/latest/api/#requests.Response />`_)
                   returned by the POST request.
        """
        req_url = self.space_url + url
        self._logger.debug("POST %s" % req_url)
        self._logger.debug(headers)
        self._logger.debug(body)
        r = requests.post(req_url, auth=(self.space_user, self.space_passwd), data=body, headers=headers, verify=False)
        self._logger.debug(r)
        self._logger.debug(r.headers)
        self._logger.debug(r.text)
        return r

    def put(self, put_url, headers, body):
        """Performs an HTTP PUT on the given url. Acts as a wrapper over
        requests.put() function.

        :param str url: URL for performing PUT
        :param dict headers: A dict with the headers that need to be sent with
            the PUT request. This is a mandatory parameter.
        :param str body: A string that forms the body of the PUT request.
            This is a mandatory parameter.

        :returns:  The response object (`requests.Response <http://docs.python-requests.org/en/latest/api/#requests.Response />`_)
                   returned by the PUT request.
        """
        req_url = self.space_url + put_url
        self._logger.debug("PUT %s" % req_url)
        self._logger.debug(headers)
        self._logger.debug(body)
        r = requests.put(req_url, auth=(self.space_user, self.space_passwd), data=body, headers=headers, verify=False)
        self._logger.debug(r)
        self._logger.debug(r.text)
        return r

    def delete(self, delete_url):
        """Performs an HTTP DELETE on the given url. Acts as a wrapper over
        requests.delete() function.

        :param str url: URL for performing DELETE

        :returns:  The response object (`requests.Response <http://docs.python-requests.org/en/latest/api/#requests.Response />`_)
                   returned by the POST request.
        """
        req_url = self.space_url + delete_url
        self._logger.debug("DELETE %s" % req_url)
        r = requests.delete(req_url, auth=(self.space_user, self.space_passwd), verify=False)
        self._logger.debug(r)
        self._logger.debug(r.text)
        return r

class RestException(Exception):
    """An exception that is raised when a REST API invocation returns a response
    indicating an error. The exception contains the complete response inside.

    Attributes:
        response: The response object (`requests.Response <http://docs.python-requests.org/en/latest/api/#requests.Response />`_) \
                  which resulted in this exception.
    """
    def __init__(self, message, response):
        Exception.__init__(self, message)
        self.response = response