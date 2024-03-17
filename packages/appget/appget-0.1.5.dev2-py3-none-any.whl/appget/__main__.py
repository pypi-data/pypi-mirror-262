#!/usr/bin/env python3
import importlib
import os
import sys

from . import appget, log


def load_plugins(plugin_folder):
    plugins = []

    # for filename in os.listdir(plugin_folder):
    #     if filename.endswith(".py"):
    #         plugin_name = filename[:-3]
    #         # plugin_module = importlib.import_module(f"{plugin_folder}.{plugin_name}")
    #         plugin_module = importlib.import_module('plugins.example')
    #         plugin_class = getattr(plugin_module, 'MyPlugin')
    #         # plugin_class = getattr(plugin_module, plugin_name)
    #         plugins.append(plugin_class())

    plugin_module = importlib.import_module('plugins.example')
    plugin_class = getattr(plugin_module, 'MyPlugin')
    plugins.append(plugin_class())

    return plugins


def testing():
    plugin_folder = "/Users/wyb/PycharmProjects/appget/example"
    sys.path.append(plugin_folder)
    plugins = load_plugins(plugin_folder)

    for plugin in plugins:
        plugin.install()


def main():
    try:
        testing()
        appget.cli()
        return 0
    except Exception as err:
        log.error(err)
        return 1


if __name__ == "__main__":
    sys.exit(main())
