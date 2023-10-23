import logging
import datetime
from pprint import pprint
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from messages import (ALREADY_REGISTERED_MESSAGE, ALREADY_HEADMAN_MESSAGE, MUST_BE_REG_MESSAGE,
                      MUST_BE_HEADMEN_MESSAGE)
from service import UsersService


__all__ = ["RegMiddleware", "HeadmenRegMiddleware", "HeadmenCommandsMiddleware"]


class RegMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info('registration middleware started')

        user_id = event.from_user.id

        with UsersService() as con:
            if con.is_registered(user_id):
                await event.reply(ALREADY_REGISTERED_MESSAGE)
                logging.warning("middleware finished, already registered")
                return

        logging.info("registration middleware finished")
        return await handler(event, data)


class HeadmenRegMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        logging.info('headmen middleware started')

        user_id = event.from_user.id

        with UsersService() as con:
            if not con.is_registered(user_id):
                await event.reply(MUST_BE_REG_MESSAGE)
                logging.warning("headmen reg middleware finished, user must be registered")
                return

            if con.is_headmen(user_id):
                await event.reply(ALREADY_HEADMAN_MESSAGE)
                logging.warning("headmen reg middleware finished, already registered as headmen")
                return

        logging.info("headmen reg middleware finished")
        return await handler(event, data)


class HeadmenCommandsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info('headmen commands middleware started')

        user_id = event.from_user.id

        with UsersService() as con:

            if not con.is_registered(user_id):
                await event.reply(MUST_BE_REG_MESSAGE)
                logging.warning("headmen commands middleware finished, user must be registered")
                return

            if not con.is_headmen(user_id):
                await event.reply(MUST_BE_HEADMEN_MESSAGE)
                logging.warning("headmen commands middleware finished, user must me headman to use this command")
                return

            logging.info("headmen commands middleware finished")
            return await handler(event, data)


class CallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info("callback middleware started")

        user_id = event.from_user.id

        with UsersService() as con:
            if con.get_time(user_id) < datetime.datetime.now().time():
                 logging.warning("callback middleware finished, lesson was already started")
                 await event.answer("Занятия уже начались!")
                 return

        logging.info("callback middleware finished")
        return await handler(event, data)
