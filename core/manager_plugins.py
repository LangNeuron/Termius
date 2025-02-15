# core.manager_plugins.py

import yaml
from .loger import get_logger
import importlib
import sys


class ManagerPlugins:
    def __init__(self, signals):
        self.signals = signals
        self.path_modules = "module.yml"
        self.config = None
        self.len_plugins = None
        self.logger = get_logger()

        self.update_config()

    def update_config(self):
        with open(self.path_modules, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
        self.logger.debug("loaded config %s", self.config)
        self.logger.info("Config loaded")
        self._get_plugins()

    def _get_plugins(self):
        self.len_plugins = len(self.config["plugins"])
        self.logger.debug("len plugins %s", self.len_plugins)
        self.table_plugins = {}
        for plug_name in self.config["plugins"]:
            self.table_plugins[self.config["plugins"][plug_name]["command"]] = {
                "path": self.config["plugins"][plug_name]["path"],
                "class": self.config["plugins"][plug_name]["class"],
                "run": self.config["plugins"][plug_name]["run"],
                "config": self.config["plugins"][plug_name].get("config", {}),
            }
            self.table_plugins[self.config["plugins"][plug_name]["command"]][
                "loaded"
            ] = self._create_runner_module(self.config["plugins"][plug_name]["command"])
        self.logger.debug("table plugins %s", self.table_plugins)
        self.logger.info("Plugins loaded")

    def _import_module(self, module_name):
        try:
            if module_name in sys.modules:
                module = importlib.reload(module_name)
            return module
        except ModuleNotFoundError as e:
            self.logger.error("Module not found: %s", e)
            raise e

    def _create_runner_module(self, name):
        if not self.table_plugins[name].get("class", False):
            if not self.table_plugins[name].get("run", False):
                return False
            temp = self._import_module(self.table_plugins[name]["path"])
            temp = getattr(temp, self.table_plugins[name]["run"])
            return temp
        temp = importlib.import_module(self.table_plugins[name]["path"])
        temp = getattr(temp, self.table_plugins[name]["class"])
        temp = temp(self.signals, **self.table_plugins[name]["config"])
        temp = getattr(temp, self.table_plugins[name]["run"])
        return temp

    def run_code(self, comm):
        self.logger.debug("run code %s", comm)
        if self.table_plugins[comm]["loaded"]:
            self.logger.debug("code %s loaded ", comm)
            out = self.table_plugins[comm]["loaded"]()
            return out
        else:
            importlib.reload(self.table_plugins[comm]["path"])

    def run(self):
        while self.signals.ai_run:
            try:
                el = self.signals.get_task()
                out = self.run_code(el)
                self.signals.put_output(out)
            except Exception as e:
                self.logger.error("Error in plugins: %s", e)
