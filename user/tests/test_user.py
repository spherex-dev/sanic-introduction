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

from env_test import env
from server import Server
import unittest

class Test(unittest.TestCase):

    def setUp(self) -> None:
        from db.base import session_manager
        session_manager.create_tables(env=env.env)

    def get_app(self):
        server = Server("test")
        server.setup()
        return server.app

    def test_hello(self):
        app = self.get_app()
        request, response = app.test_client.get("/api/user/hello")
        self.assertEqual(response.json["message"], "hello")

    def test_add_user(self):
        app = self.get_app()
        user = {"username": "test", "password": "test_password", "email": "test@test.com"}
        _, response = app.test_client.post("/api/user/delete_user", json=user)
        _, response = app.test_client.post("/api/user/add_user", json=user)
        self.assertEqual(response.json["status"], "success")

        _, response = app.test_client.post("/auth", json=user)
        self.assertTrue("access_token" in response.json)
        token = response.json["access_token"]
        _, response = app.test_client.get("/auth/verify", headers={"Authorization": f"Bearer {token}"})
        self.assertTrue(response.json["valid"])

        _, response = app.test_client.get("/api/user/protected", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.json["message"], "protected")
        
        _, response = app.test_client.get("/api/user/protected")
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
