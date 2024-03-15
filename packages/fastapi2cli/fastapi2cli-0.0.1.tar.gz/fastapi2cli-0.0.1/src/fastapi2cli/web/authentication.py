import typing

from fastapi.dependencies.models import Dependant
from fastapi.params import Security
from fastapi.routing import APIRoute


class AuthenticationResolverProtocol(typing.Protocol):
    """
    Protocol defining methods for an authentication resolver.

    This protocol defines the methods that an authentication resolver must implement.

    """

    def get_headers(self) -> dict[str, typing.Any]:
        """
        Get headers for authentication.

        :return: A dictionary containing headers.
        :rtype: dict[str, typing.Any]
        """

    def get_cookies(self) -> dict[str, typing.Any]:
        """
        Get cookies for authentication.

        :return: A dictionary containing cookies.
        :rtype: dict[str, typing.Any]
        """

    def get_query_parameters(self) -> dict[str, typing.Any]:
        """
        Get query parameters for authentication.

        :return: A dictionary containing query parameters.
        :rtype: dict[str, typing.Any]
        """


class AuthenticationResolverBase:
    """
    Base class for authentication resolver.

    This class provides default implementations for authentication resolver methods.

    """

    def get_headers(self) -> dict[str, typing.Any]:
        """
        Get headers for authentication.

        :return: A dictionary containing headers.
        :rtype: dict[str, typing.Any]
        """
        return {}

    def get_cookies(self) -> dict[str, typing.Any]:
        """
        Get cookies for authentication.

        :return: A dictionary containing cookies.
        :rtype: dict[str, typing.Any]
        """
        return {}

    def get_query_parameters(self) -> dict[str, typing.Any]:
        """
        Get query parameters for authentication.

        :return: A dictionary containing query parameters.
        :rtype: dict[str, typing.Any]
        """
        return {}


class NoAuthResolverException(Exception):
    """
    Exception raised when authentication resolver is not available.

    This exception is raised when attempting to access authenticated resources but no authentication resolver are
    provided.
    """
    pass


class NoAuthResolver(AuthenticationResolverBase):
    """
    Authentication resolver for no authentication.

    This class provides an implementation for authentication resolver methods
    when no authentication is required.

    """

    def get_headers(self) -> dict[str, typing.Any]:
        """
        Get headers for authentication.

        :raises NoAuthResolverException: Always raised since no authentication headers are available.
        """
        raise NoAuthResolverException()

    def get_cookies(self) -> dict[str, typing.Any]:
        """
        Get cookies for authentication.

        :raises NoAuthResolverException: Always raised since no authentication cookies are available.
        """
        raise NoAuthResolverException()

    def get_query_parameters(self) -> dict[str, typing.Any]:
        """
        Get query parameters for authentication.

        :raises NoAuthResolverException: Always raised since no authentication query parameters are available.
        """
        raise NoAuthResolverException()


class AuthenticationManager:
    """
    Manager for authentication.

    This class manages authentication for dependencies and routes.

    """

    def __init__(self, authenticated_dependencies: list[typing.Callable],
                 authentication_resolver: AuthenticationResolverProtocol):
        """
        Initialize AuthenticationManager.

        :param authenticated_dependencies: List of authenticated dependencies.
        :type authenticated_dependencies: list[typing.Callable]
        :param authentication_resolver: Authentication resolver.
        :type authentication_resolver: AuthenticationResolverProtocol
        """
        self.authenticated_dependencies = authenticated_dependencies
        self.authentication_resolver = authentication_resolver

    def is_dependency_authenticated(self, dependency: Dependant):
        """
        Check if a dependency is authenticated.

        :param dependency: The dependency to check.
        :type dependency: Dependant
        :return: True if the dependency is authenticated, False otherwise.
        :rtype: bool
        """
        if isinstance(dependency, Security) or dependency.call in self.authenticated_dependencies:
            return True
        return any(
            self.is_dependency_authenticated(dep) for dep in dependency.dependencies
        )

    def is_route_authenticated(self, route: APIRoute) -> bool:
        """
        Check if a route is authenticated.

        :param route: The route to check.
        :type route: APIRoute
        :return: True if the route is authenticated, False otherwise.
        :rtype: bool
        """
        return self.is_dependency_authenticated(route.dependant)

    @property
    def headers(self) -> dict[str, typing.Any]:
        """
        Get headers for authentication.

        :return: A dictionary containing headers.
        :rtype: dict[str, typing.Any]
        """
        return self.authentication_resolver.get_headers()

    @property
    def query_parameters(self) -> dict[str, typing.Any]:
        """
        Get query parameters for authentication.

        :return: A dictionary containing query parameters.
        :rtype: dict[str, typing.Any]
        """
        return self.authentication_resolver.get_query_parameters()

    @property
    def cookies(self) -> dict[str, typing.Any]:
        """
        Get cookies for authentication.

        :return: A dictionary containing cookies.
        :rtype: dict[str, typing.Any]
        """
        return self.authentication_resolver.get_cookies()
