from importlib import metadata

from .client import IPFClient

__version__ = metadata.version("mini_ipfabric")

__all__ = ["IPFClient"]
