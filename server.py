###############################################################################
# Copyright (C) 2021, created on December 26, 2021
# Written by Justin Ho
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# This source code is distributed in the hope that it will be useful and
# without warranty or implied warranty of merchantability or fitness for a
# particular purpose.
###############################################################################

import logging
from importlib import import_module
from sanic import Sanic
from sanic_jwt import initialize
from db.user import User

logger = logging.getLogger(__name__)


class Server:

    def __init__(self, name, env="main"):
        self.name = name
        self.env = env
        self.settings = {"host": "localhost", "port": 5005}
        self.app = Sanic(name=name)

        self.blueprints = ["user"]

        self.log_format = "%(asctime)s [%(levelname)s]: %(message)s"
        self.log_path = "sanic.log"
        self.log_level = "INFO"

    def setup_logs(self):
        level = getattr(logging, self.log_level)
        logging.basicConfig(filename=self.log_path, format=self.log_format, level=level)

    def setup_blueprints(self):
        for bp in self.blueprints:
            try:
                module = import_module(f"{bp}.views")
                self.app.blueprint(module.bp)
            except ModuleNotFoundError:
                print("failed to load blueprint %s" % bp)
                logger.warning("failed to load blueprint %s", bp)
                pass

    def setup(self):
        self.setup_logs()
        self.setup_blueprints()
        initialize(self.app, User.app_authenticate)

    def run(self, auto_reload=True):

        self.setup()
        self.app.run(auto_reload=auto_reload, **self.settings)


if __name__ == "__main__":
    server = Server("sanic")
    server.run(auto_reload=True)
