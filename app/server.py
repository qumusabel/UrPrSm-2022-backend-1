import json

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from . import db, utils

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


def _error(code: int, msg: str) -> JSONResponse:
    return JSONResponse({"status": "Error", "details": msg}, code)


@app.on_event("startup")
async def init_app():
    await db.init_db()


@app.post("/shorten")
async def shorten(request: Request):
    try:
        req_json = await request.json()
    except json.JSONDecodeError:
        return _error(status.HTTP_400_BAD_REQUEST, "invalid JSON")

    if "urlToShorten" not in req_json:
        return _error(status.HTTP_400_BAD_REQUEST, 'missing "urlToShorten"')

    url = req_json.get("urlToShorten")

    if not utils.is_valid_url(url):
        return _error(status.HTTP_400_BAD_REQUEST, "invalid URL")

    slug = utils.generate_slug()

    await db.add_url(slug, url)

    return JSONResponse(
        {
            "status": "Created",
            "shortenedUrl": str(request.base_url) + slug
        },
        status.HTTP_201_CREATED
    )


@app.get("/{slug}")
async def get_url(slug: str):
    url = await db.get_url(slug)

    if url is None:
        return _error(status.HTTP_404_NOT_FOUND, "not found")

    await db.inc_views(slug)

    return JSONResponse(
        {
            "redirectTo": url
        },
        status.HTTP_301_MOVED_PERMANENTLY,
        headers={"Location": url}
    )


@app.get("/{slug}/views")
async def get_slug_views(slug: str):
    views = await db.get_views(slug)

    if views is None:
        return _error(status.HTTP_404_NOT_FOUND, "not found")

    return JSONResponse({"viewCount": views}, status.HTTP_200_OK)

