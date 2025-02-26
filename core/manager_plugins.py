# core.manager_plugins.py

import yaml
from .loger import get_logger
import importlib
import sys
from fuzzywuzzy import process


class ManagerPlugins:
    def __init__(self, signals):
        self.loaded_module = {}
        self.signals = signals
        self.path_modules = "module.yml"
        self.config = None
        self.len_plugins = None
        self.logger = get_logger()
        self.command = {}
        self.table_plugins = {}

        self.update_config()

    def update_config(self):
        with open(self.path_modules, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
        self.logger.debug("loaded config %s", self.config)
        self.logger.info("Config loaded")
        self._get_plugins()

    def create_table(self, command, plug_name):
        self.table_plugins[command] = {
            "path": self.config["plugins"][plug_name]["path"],
            "class": self.config["plugins"][plug_name].get("class", False),
            "run": self.config["plugins"][plug_name].get("run", False),
            "config": self.config["plugins"][plug_name].get("config", {}),
        }
        self.table_plugins[command]["loaded"] = self._create_runner_module(command)

    def _get_plugins(self):
        self.len_plugins = len(self.config["plugins"])
        self.logger.debug("len plugins %s", self.len_plugins)
        for plug_name in self.config["plugins"]:
            command = self.config["plugins"][plug_name]["command"]
            if isinstance(command, list):
                main_command = command[0]
                self.create_table(main_command, plug_name)
                for cmd in command:
                    self.command[cmd] = main_command
            else:
                self.create_table(command, plug_name)
                self.command[command] = command
        self.logger.debug("table plugins %s", self.table_plugins)
        self.logger.info("Plugins loaded")

    def _import_module(self, module_name):
        try:
            if module_name in sys.modules:
                module = importlib.reload(module_name)
                return module
            else:
                module = importlib.import_module(module_name)
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

    def run_code(self, comm, **kwargs):
        self.logger.debug("run code %s", comm)
        if self.table_plugins[comm]["loaded"]:
            if self.table_plugins[comm]["loaded"] is True:
                importlib.reload(self.loaded_module[self.table_plugins[comm]["path"]])
            else:
                self.logger.debug("code %s loaded ", comm)
                out = self.table_plugins[comm]["loaded"](data=kwargs.get("data", None))
                return out
        else:
            n = importlib.import_module(self.table_plugins[comm]["path"])
            self.loaded_module[self.table_plugins[comm]["path"]] = n
            self.table_plugins[comm]["loaded"] = True

    def search_task(self, comm):
        command, percent = process.extractOne(comm, list(self.command.keys()))
        if percent > 70:
            self.logger.info(
                "Command: %s Found %s. TOTAL COMMAND: %s"
                % (command, percent / 100, self.command[command])
            )
            return self.run_code(self.command[command])
        else:
            self.logger.info("Command not found: %s", comm)
            self.logger.info("Start work llm")
            self.run_code("LLM", data=comm)

    async def run(self):
        while self.signals.ai_run:
            task = await self.signals.get_task()
            result = self.search_task(task)
            await self.signals.add_result(result)
