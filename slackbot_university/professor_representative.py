import os
import importlib
import inspect
from typing import Callable, Optional

from .plugin_manager import PluginManager, PACKAGE_NAME
from .professors import Professor
from .log import get_logger

logger = get_logger("professor_representative")


class ProfessorRepresentative(PluginManager):
    
    folder_name = "professors"

    def __init__(self, plugins):
        self.professors = {}
        self.default_professor = None
        super().__init__(plugins)

    def load(self, plugin: str) -> Optional['ModuleType']:
        path = ".".join([PACKAGE_NAME, self.folder_name, plugin])
        try:
            # internal module
            module = importlib.import_module(path)
        except ModuleNotFoundError:
            try:
                # external module
                module = importlib.import_module(plugin)
            except ModuleNotFoundError:
                logger.exception("")
                return None
        self.register_professor(module)
        return module

    def register_professor(self, module):
        all_classes = inspect.getmembers(module, inspect.isclass)
        for class_name, class_suspect in all_classes:
            if issubclass(class_suspect, Professor):
                instance = class_suspect() 
                if instance.is_default():
                    self.default_professor = instance
                self.professors[class_name] = instance
                logger.info(f"{class_name} found")
        
    def answer_short(self, text):
        professor = self.find_suitable_professor(text)
        print(professor)
        if professor is not None:
            return professor.answer_short(text)

    def find_suitable_professor(self, text):
        return (
            self.self_entrusted_professor(text)
            or self.analyse_text(text)
            or self.default_professor
        )

    def analyse_text(self, text: str) -> Professor:
        return None

    def self_entrusted_professor(self, text):
        for professor in self.professors.values():
            try:
                if professor.is_mine(text):
                    return professor
            except Exception:
                logger.exception("")
                continue
        return None

