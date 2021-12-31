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


import re
from string import punctuation, whitespace

from sanic_jwt import exceptions
from sqlalchemy import Column, Index, Integer, String, select
from sqlalchemy.sql import or_
from sqlalchemy_utils import PasswordType

from .base import Base, get_async_session


class User(Base):

    __tablename__ = "user"

    invalid_chars = punctuation + whitespace
    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(PasswordType(schemes=["pbkdf2_sha512"]))

    ix_user_email = Index("ix_user_email", email)
    ix_user_username = Index("ix_user_username", username)

    email_check = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    @classmethod
    async def user_exists(cls, session, identifier):
        """
        Check if user exists.
        """
        if '@' in identifier:
            return session.query(cls).filter(or_(cls.email == identifier)).count() > 0
        else:
            return session.query(cls).filter(or_(cls.username == identifier)).count() > 0

    @classmethod
    def valid_username(cls, username):
        """
        Check if username is valid.
        """
        return username and not any(char in username for char in cls.invalid_chars)

    @classmethod
    def valid_email(cls, email):
        """
        Check if email is valid.
        """
        return cls.email_check.match(email.strip()) is not None

    @classmethod
    def valid_password(cls, password):
        """
        Check if password is valid.
        Sets a minimum length for password
        """
        return len(password) >= 8

    @classmethod
    async def add_user(cls, session, email, username, password):

        async with session.begin():
            if all([cls.valid_username(username), cls.valid_email(email), cls.valid_password(password)]):
                user = User(email=email, username=username, password=password)
                session.add(user)
                await session.commit()
                return user
            else:
                return None

    @classmethod
    async def delete_user(cls, session, email):
        query = cls.__table__.delete().\
            where(cls.email == email)

        async with session.begin():
            await session.execute(query)
            await session.commit()

    @classmethod
    async def authenticate(cls, session, email, password):
        query = select(cls).filter(cls.email == email)
        cursor = await session.execute(query)
        user = cursor.first()[0]
        if user and user.password == password:
            return user
        else:
            return None

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}

    @classmethod
    async def app_authenticate(cls, request, *args, **kwargs):
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email or not password:
            raise exceptions.AuthenticationFailed("Missing email or password.")

        async with get_async_session() as session:
            user = await cls.authenticate(session, email, password)
        if user is None:
            raise exceptions.AuthenticationFailed("User not found.")

        if password != user.password:
            raise exceptions.AuthenticationFailed("Password is incorrect.")

        return user
