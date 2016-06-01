import asyncio
import json
import functools

from aiohttp import web
from aiohttp.abc import AbstractView

import jsonschema
from tokenize_uk import tokenize_text


def validate(input_schema=None, output_schema=None):

    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(*args):
            func._input_schema = input_schema
            func._output_schema = output_schema
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

            if func._input_schema is not None:
                jsonschema.validate(req_body, func._input_schema)

            context = yield from coro(req_body, request)

            if isinstance(context, web.StreamResponse):
                return context

            if func._output_schema is not None:
                validate(context, func._output_schema)

            # response = render_template(template_name, request, context,
            #                            app_key=app_key, encoding=encoding)
            # response.set_status(status)
            return web.json_response(context)

        return wrapped
    return wrapper


@validate(input_schema={
    "type": "object",
    "properties": {
        "text": {"type": "string"},
    },
    "required": ["text"],
    "additionalProperties": False
})
async def hello(request, raw_request):

    return {
        "request": request,
        "response": tokenize_text(request["text"])
    }


app = web.Application()
app.router.add_route("POST", "/", hello)

if __name__ == '__main__':
    web.run_app(app)
