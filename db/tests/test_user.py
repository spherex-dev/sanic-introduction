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

import env

env.env = "test"

import unittest
from unittest import IsolatedAsyncioTestCase

from db.base import session_manager
from db.user import User


class TestUser(unittest.TestCase):

    def setUp(self) -> None:
        session_manager.create_tables(env.env)

    def test_validate_username(self):
        self.assertTrue(User.valid_username("jh"))
        self.assertFalse(User.valid_username(""))
        self.assertFalse(User.valid_username("sdfds$%"))

    def test_validate_email(self):
        self.assertTrue(User.valid_email("test@test.com"))
        self.assertFalse(User.valid_email(""))
        self.assertFalse(User.valid_email("not_valid"))

    def test_validate_password(self):
        self.assertTrue(User.valid_password("good_password"))
        self.assertFalse(User.valid_password("bad"))
        self.assertFalse(User.valid_password(""))
    

# class TestAsyncUser(IsolatedAsyncioTestCase):

#     def setUp(self) -> None:
#         session_manager.create_tables("test")

if __name__ == "__main__":
    unittest.main()
