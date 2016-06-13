from aiohttp import web

from validator import validate
from swagger import document
from tokenize_uk import tokenize_text
from schema import TOKENIZE_TEXT_OUTPUT_SCHEMA, TOKENIZE_TEXT_INPUT_SCHEMA


@validate(
    input_schema=TOKENIZE_TEXT_INPUT_SCHEMA,
    output_schema=TOKENIZE_TEXT_OUTPUT_SCHEMA,
)
async def tokenize_text_handler(request, *args):
    return tokenize_text(request["text"])


app = web.Application()
app.router.add_route("POST", "/tokenize_text", tokenize_text_handler)
app = document(app)

if __name__ == '__main__':
    web.run_app(app)
