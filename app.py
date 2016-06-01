import asyncio

from aiohttp import web

from validator import validate
from swagger import document
from tokenize_uk import tokenize_text



@validate(input_schema={
    "type": "object",
    "properties": {
        "text": {"type": "string"},
    },
    "required": ["text"],
    "additionalProperties": False
})
async def tokenize_text_handler(request, *args):

    return {
        "response": tokenize_text(request["text"])
    }


app = web.Application()
app.router.add_route("POST", "/tokenize_text", tokenize_text_handler)
app = document(app)

if __name__ == '__main__':
    web.run_app(app)
