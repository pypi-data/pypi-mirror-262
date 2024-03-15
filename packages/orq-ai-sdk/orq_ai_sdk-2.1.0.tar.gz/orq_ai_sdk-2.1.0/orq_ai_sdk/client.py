import os

from orq_ai_sdk.exceptions import OrqInvalidAPIException
from .api_resources.deployments import AsyncDeployments, Deployments
from .models import Store
from .options import OrqClientOptions


class Orq:
    options = None
    user = None

    """
    Represents an Orq client.

    Args:
        options (OrqClientOptions): The options for the Orq client.

    Attributes:
        deployments (Deployments): An instance of the Deployments class.

    Raises:
        OrqInvalidAPIException: If the provided API key is invalid.
    """

    def __init__(self, options: OrqClientOptions):
        api_key = options.api_key or os.environ.get("ORQ_API_KEY")

        if api_key is None or len(api_key) == 0:
            raise OrqInvalidAPIException("The provided API key is invalid.")

        self.options = options
        Store["api_key"] = api_key
        Store["environment"] = options.environment

    @property
    def deployments(self):
        return Deployments()

    def set_user(self, id=None):
        Store["user_info"] = {"id": id}


class AsyncOrq:
    options = None
    user = None

    """
    Represents an Orq client.

    Args:
        options (OrqClientOptions): The options for the Orq client.

    Attributes:
        deployments (Deployments): An instance of the Deployments class.

    Raises:
        OrqInvalidAPIException: If the provided API key is invalid.
    """

    def __init__(self, options: OrqClientOptions):
        api_key = options.api_key or os.environ.get("ORQ_API_KEY")

        if api_key is None or len(api_key) == 0:
            raise OrqInvalidAPIException("The provided API key is invalid.")

        self.options = options
        Store["api_key"] = api_key
        Store["environment"] = options.environment

    @property
    def deployments(self):
        return AsyncDeployments()

    def set_user(self, id=None):
        Store["user_info"] = {"id": id}
