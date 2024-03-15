"""
A provider class that can parse and return Lambda Functions from a variety of sources. A SAM template is one such
source
"""

from collections import namedtuple

# Named Tuple to representing the properties of a Lambda Function
_Function = namedtuple("Function", [
    # Function name or logical ID
    "name",

    # Function all properties
    "properties"
])

class Function(_Function):
    @property
    def codeuri(self):
        return self.properties.get("CodeUri")

    @property
    def handler(self):
        return self.properties.get("Handler")

    @property
    def timeout(self):
        return self.properties.get("Timeout")

    @property
    def environment(self):
        return self.properties.get("Environment")

    @property
    def memory(self):
        return self.properties.get("Memory")

    @property
    def runtime(self):
        return self.properties.get("Runtime")

class FunctionProvider(object):
    """
    Abstract base class of the function provider.
    """

    def get(self, name):
        """
        Given name of the function, this method must return the Function object

        :param string name: Name of the function
        :return Function: namedtuple containing the Function information
        """
        raise NotImplementedError("not implemented")

    def get_all(self):
        """
        Yields all the Lambda functions available in the provider.

        :yields Function: namedtuple containing the function information
        """
        raise NotImplementedError("not implemented")


# Named Tuple to representing the properties of a Lambda Function
Layer = namedtuple("Layer", [
    # str Layer name or logical ID
    "name",

    # str layer file dir
    "layer_uri",

    # array of str 
    "compatible_runtimes",

    # str
    "description",

    # str
    "license_info"
])

class LayerProvider(object):
    """
    Abstract base class of the layer provider.
    """

    def get(self, name):
        """
        Given name of the layer, this method must return the layer object

        :param string name: Name of the layer
        :return layer: namedtuple containing the layer information
        """
        raise NotImplementedError("not implemented")

    def get_all(self):
        """
        Yields all the layers available in the provider.

        :yields layer: namedtuple containing the layer information
        """
        raise NotImplementedError("not implemented")
    
    def deploy(self, name):
        """
        Yields all the layers available in the provider.

        :yields layer: namedtuple containing the layer information
        """
        raise NotImplementedError("not implemented")


_ApiTuple = namedtuple("Api", [

    # String. Path that this API serves. Ex: /foo, /bar/baz
    "path",

    # String. HTTP Method this API responds with
    "method",

    # String. Name of the Function this API connects to
    "function_name",

    # Optional Dictionary containing CORS configuration on this path+method
    # If this configuration is set, then API server will automatically respond to OPTIONS HTTP method on this path and
    # respond with appropriate CORS headers based on configuration.
    "cors",

    # List(Str). List of the binary media types the API
    "binary_media_types"
])
_ApiTuple.__new__.__defaults__ = (None,  # Cors is optional and defaults to None
                                  []     # binary_media_types is optional and defaults to empty
                                  )


class Api(_ApiTuple):
    def __hash__(self):
        # Other properties are not a part of the hash
        return hash(self.path) * hash(self.method) * hash(self.function_name)


Cors = namedtuple("Cors", ["AllowOrigin", "AllowMethods", "AllowHeaders"])


class ApiProvider(object):
    """
    Abstract base class to return APIs and the functions they route to
    """

    def get_all(self):
        """
        Yields all the APIs available.

        :yields Api: namedtuple containing the API information
        """
        raise NotImplementedError("not implemented")

BosEvent = namedtuple("BosEvent", [

    # String. Path that this API serves. Ex: /foo, /bar/baz
    "bucket",

    # String List. HTTP Method this API responds with
    "event_types",

    # String
    "prefix",

    # String
    "suffix",

    # String
    "function_name",
])

DuerosEvent = namedtuple("DuerosEvent", [
    # String
    "function_name",
])

HttpEvent = namedtuple("HttpEvent", [
    # String
    "function_name",

    # String
    "resource_path",

    # List of String
    "method",

    # String
    "auth_type",

    # Bool
    "is_binary"
])


class EventSourceProvider(object):
    def get(self, name):
        """
        Given name of the function, this method must return the Function object

        :param string name: Name of the function
        :return Function: namedtuple containing the Function information
        """
        raise NotImplementedError("not implemented")

    def deploy(self, cfc_client, func_config):
        raise NotImplementedError("not implemented")
