#!/usr/bin/env python3

import json

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from . import db
from .utils import generate_slug, is_valid_url


def _error(code: int, msg: str) -> HTTPException:
    return HTTPException(status_code=code, detail={"status": "Error", "msg": msg})


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.on_event('startup')
async def init_app():
    await db.init_db()


@app.post('/shorten')
async def shorten(request: Request):
    try:
        req_json = await request.json()
    except json.JSONDecodeError:
        raise _error(status.HTTP_400_BAD_REQUEST, "invalid JSON")

    if 'urlToShorten' not in req_json:
        raise _error(status.HTTP_400_BAD_REQUEST, "missing 'urlToShorten'")

    url = req_json.get('urlToShorten')

    if not is_valid_url(url):
        raise _error(status.HTTP_400_BAD_REQUEST, "invalid URL")

    slug = generate_slug()

    await db.add_url(slug, url)

    return JSONResponse(
        {
            'status': "Created", 
            "shortenedUrl": str(request.base_url) + slug
        },
        status.HTTP_201_CREATED
    )


@app.get('/{slug}')
async def get_url(slug: str):
    url = await db.get_url(slug)

    if url is None:
        raise _error(status.HTTP_404_NOT_FOUND, "not found")

    await db.inc_hits(slug)

    return JSONResponse(
        {
            "redirectTo": url
        }, 
        status.HTTP_301_MOVED_PERMANENTLY,
        headers={"Location": url}
    )


@app.get('/{slug}/views')
async def get_slug_views(slug: str):
    views = await db.get_hits(slug)

    if views is None:
        raise _error(status.HTTP_404_NOT_FOUND, "not found")

    return JSONResponse({"viewCount": views}, status.HTTP_200_OK)

