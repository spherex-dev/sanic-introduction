
from functools import lru_cache, wraps

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from env import env

Base = declarative_base()


class SessionManager:

    connDict = {"main": "sqlite:///db/main.db",
                "test": "sqlite:///db/test.db",
                }

    connDictAsync = {"main": "sqlite+aiosqlite:///db/main.db",
                     "test": "sqlite+aiosqlite:///db/test.db",
                     }

    def __init__(self):
        self.engines = {}
        self.sessionMakers = {}
        self.async_engines = {}
        self.async_sessions = {}

    def get_engine(self, env=env, echo=False):

        if env not in self.engines:
            connString = self.connDict[env]
            engine = create_engine(connString, echo=echo, pool_pre_ping=True)
            self.engines[env] = engine

        else:
            engine = self.engines[env]

        return engine

    def get_session(self, env=env, echo=False):

        if env not in self.sessionMakers:
            engine = self.get_engine(env, echo)
            Session = sessionmaker(engine)
            self.sessionMakers[env] = Session

        else:
            Session = self.sessionMakers[env]

        return Session()

    def get_async_engine(self, env=env, echo=False):

        if env not in self.async_engines:
            connString = self.connDictAsync[env]
            engine = create_async_engine(connString, echo=echo, pool_pre_ping=True)
            self.async_engines[env] = engine

        else:
            engine = self.engines[env]

        return engine

    def get_async_session(self, env=env, echo=False):

        if env not in self.async_sessions:
            engine = self.get_async_engine(env, echo)
            self.async_sessions[env] = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        return self.async_sessions[env]()

    def create_tables(self, env=env):
        engine = self.get_engine(env)
        Base.metadata.create_all(engine)


session_manager = SessionManager()


def get_session(env=env, echo=False):
    return session_manager.get_session(env, echo=echo)


def get_async_session(env=env, echo=False):
    return session_manager.get_async_session(env=env, echo=echo)
