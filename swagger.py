from collections import defaultdict
from aiohttp import web


def _convert_jsonschema_to_swagger(jsnschema):
    pass


def document(app):
    async def swagger_handler(request):
        return web.json_response(app["_swagger_config"])

    swagger_config = defaultdict(dict)

    for r in app.router.routes():
        desc = {
            "description": r.handler.__doc__,
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "responses": {
                "400": {"description": "Input is malformed or invalid"},
                "500": {"description": "Output malformed or invalid"},
                "405": {"description": "Method is not allowed"},
            }
        }
        # print(r.handler.__doc__)
        # print(getattr(r.handler, "_input_schema"))
        # print(getattr(r.handler, "_output_schema"))
        swagger_config[r._resource._path][r.method.lower()] = desc

    app["_swagger_config"] = swagger_config

    app.router.add_route("GET", "/swagger.json", swagger_handler)

    return app

__ALL__ = ["document", ]
