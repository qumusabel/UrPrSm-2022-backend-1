import os
from typing import Union

import aiosqlite

DB_FILE = os.getenv("SQLITE_DB", "/tmp/db.sqlite")


async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS urls (slug TEXT, url TEXT, views INTEGER)"
        )
        await db.commit()


async def add_url(slug: str, url: str):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "INSERT INTO urls VALUES (?, ?, 0)",
            (slug, url)
        )
        await db.commit()


async def _get_row(slug: str) -> Union[aiosqlite.Row, None]:
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            "SELECT * FROM urls WHERE slug = (?)",
            (slug, )
        )
        return await cursor.fetchone()


async def get_url(slug: str) -> Union[str, None]:
    row = await _get_row(slug)
    return row["url"] if row else None


async def get_views(slug: str) -> Union[int, None]:
    row = await _get_row(slug)
    return row["views"] if row else None


async def inc_views(slug: str):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "UPDATE urls SET views = views + 1 WHERE slug = (?)",
            (slug, )
        )
        await db.commit()

