import os
from typing import Tuple, Union

import aiosqlite

_db_file = os.getenv('SQLITE_FILE', ':memory:')

_schema = "CREATE TABLE IF NOT EXISTS urls (slug TEXT, url TEXT, hits INTEGER)"
_get_url_sql  = "SELECT * FROM urls WHERE slug = (?)"
_add_url_sql  = "INSERT INTO urls VALUES (?, ?, 0)"
_inc_hits_sql = "UPDATE urls SET hits = (?) WHERE slug = (?)" 


async def init_db():
    async with aiosqlite.connect(_db_file) as db:
        await db.execute(_schema)
        await db.commit()


async def add_url(slug: str, url: str):
    async with aiosqlite.connect(_db_file) as db:
        await db.execute(_add_url_sql, (slug, url))
        await db.commit()


async def _get_row(slug: str) -> Union[aiosqlite.Row, None]:
    async with aiosqlite.connect(_db_file) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute(_get_url_sql, (slug,))
        return await cursor.fetchone()


async def get_url(slug: str) -> Union[str, None]:
    row = await _get_row(slug)
    return row['url'] if row else None


async def get_hits(slug: str) -> Union[int, None]:
    row = await _get_row(slug)
    return row['hits'] if row else None


async def inc_hits(slug: str):
    async with aiosqlite.connect(_db_file) as db:
        row = await _get_row(slug)
        
        if row is None:
            return

        hits = row['hits']

        await db.execute(_inc_hits_sql, (hits + 1, slug))
        await db.commit()
