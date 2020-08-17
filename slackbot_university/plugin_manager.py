import os
import importlib
from abc import abstractmethod, ABC
from typing import Optional

from .log import get_logger

logger = get_logger("plugin_manager")

default_worker_plugins = [
    "lang_assistant",        
    "professor_knowall"
]

PACKAGE_NAME = os.path.basename(os.path.dirname(__file__))


class PluginManager(ABC):

    def __init__(self, plugins):
        self.plugins = {}
        for plugin in plugins:
            self.register(plugin)

    @abstractmethod
    def load(self, plugin: str) -> Optional["ModuleType"]:
        pass

    def register(self, plugin: str):
        """Return True if register successful, else False"""
        logger.info(f"registering {plugin}")
        try:
            module = self.load(plugin)
        except Exception:
            logger.exception("")
            module = None
        if module is None:
            logger.warn(f"Failed to load {plugin}")
            return False
        self.plugins[plugin] = module
        logger.info(f"{plugin} is loaded successfully")
        return True


