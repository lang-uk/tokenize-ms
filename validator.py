import json
import functools
import asyncio
from collections import defaultdict

from aiohttp import web
from aiohttp.abc import AbstractView
from jsonschema.validators import validator_for


def _raise_exception(cls, reason, data=None):
    text_dict = {
        "error": reason
    }

    if data is not None:
        text_dict["errors"] = data

    raise cls(
        text=json.dumps(text_dict),
        content_type="application/json"
    )


def _validate_data(data, schema, validator_cls):
    validator = validator_cls(schema)
    _errors = defaultdict(list)
    for err in validator.iter_errors(data):
        path = err.schema_path

        # Code courtesy: Ruslan Karalkin
        # Looking in error schema path for
        # property that failed validation
        # Schema example:
        # {
        #    "type": "object",
        #    "properties": {
        #        "foo": {"type": "number"},
        #        "bar": {"type": "string"}
        #     }
        #    "required": ["foo", "bar"]
        # }
        #
        # Related err.schema_path examples:
        # ['required'],
        # ['properties', 'foo', 'type']

        if "properties" in path:
            path.remove("properties")
        key = path.popleft()

        # If validation failed by missing property,
        # then parse err.message to find property name
        # as it always first word enclosed in quotes
        if key == "required":
            key = err.message.split("'")[1]

        _errors[key].append(str(err))

    if _errors:
        _raise_exception(
            web.HTTPBadRequest,
            "Input is invalid; There are validation errors.",
            _errors)


def validate(input_schema=None, output_schema=None):

    def wrapper(func):
        # Validating the schemas itself.
        # Die with exception if they aren't valid
        if input_schema is not None:
            _input_schema_validator = validator_for(input_schema)
            _input_schema_validator.check_schema(input_schema)

        if output_schema is not None:
            _output_schema_validator = validator_for(output_schema)
            _output_schema_validator.check_schema(output_schema)

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
            except (json.decoder.JSONDecodeError, TypeError):
                _raise_exception(
                    web.HTTPBadRequest,
                    "Input is malformed; could not decode JSON object.")

            if input_schema is not None:
                _validate_data(req_body, input_schema,
                               _input_schema_validator)
                # TODO: return validation errors

            context = yield from coro(req_body, request)

            if isinstance(context, web.StreamResponse):
                return context

            if output_schema is not None:
                _validate_data(context, output_schema,
                               _output_schema_validator)
                # TODO: return validation errors

            try:
                return web.json_response(context)
            except (TypeError, ):
                _raise_exception(
                    web.HTTPInternalServerError,
                    "Output is malformed; could not encode JSON object.")

        setattr(wrapped, "_input_schema", input_schema)
        setattr(wrapped, "_output_schema", output_schema)
        return wrapped
    return wrapper

__ALL__ = ["validate", ]
