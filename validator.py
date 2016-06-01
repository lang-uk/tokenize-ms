import json
import functools
import asyncio

from aiohttp import web
from aiohttp.abc import AbstractView
import jsonschema


def validate(input_schema=None, output_schema=None):

    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(*args):
            if asyncio.iscoroutinefunction(func):
                coro = func
            else:
                coro = asyncio.coroutine(func)

            # Supports class based views see web.View
            if isinstance(args[0], AbstractView):
                request = args[0].request
            else:
                request = args[-1]

            try:
                req_body = yield from request.json()
            except json.decoder.JSONDecodeError:
                req_body = {}

            if input_schema is not None:
                jsonschema.validate(req_body, input_schema)
                # TODO: return validation errors

            context = yield from coro(req_body, request)

            if isinstance(context, web.StreamResponse):
                return context

            if output_schema is not None:
                validate(context, output_schema)
                # TODO: return validation errors

            return web.json_response(context)

        setattr(wrapped, "_input_schema", input_schema)
        setattr(wrapped, "_output_schema", output_schema)
        return wrapped
    return wrapper
