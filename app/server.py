#!/usr/bin/env python3

import json

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from . import db
from .utils import generate_slug, is_valid_url


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

def _error(code: int, msg: str) -> JSONResponse:
    return JSONResponse({"status": "Error", "msg": msg}, code)


@app.on_event('startup')
async def init_app():
    await db.init_db()


@app.post('/shorten')
async def shorten(request: Request):
    try:
        req_json = await request.json()
    except json.JSONDecodeError:
        return _error(400, "invalid JSON")

    if 'urlToShorten' not in req_json:
        return _error(400, "missing 'urlToShorten'")

    url = req_json.get('urlToShorten')

    if not is_valid_url(url):
        return _error(400, "invalid URL")

    slug = generate_slug()

    await db.add_url(slug, url)

    return JSONResponse({'url': str(request.base_url) + slug}, 201)


@app.get('/{slug}')
async def get_url(slug: str):
    url = await db.get_url(slug)

    if url is None:
        return _error(404, "not found")

    await db.inc_hits(slug)

    return JSONResponse(
            {"redirectTo": url}, 
            status_code=301, 
            headers={"Location": url}
        )


@app.get('/{slug}/views')
async def get_slug_views(slug: str):
    views = await db.get_hits(slug)

    if views is None:
        return _error(404, "not found")

    return JSONResponse({"viewCount": views}, 200)

