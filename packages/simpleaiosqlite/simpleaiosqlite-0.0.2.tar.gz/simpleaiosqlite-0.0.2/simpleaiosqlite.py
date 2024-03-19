import aiosqlite
class SQLITE(commands.Cog):
    def __init__(self, dbname: str = 'database.db'):
        self.dbname = dbname

    async def connect(self):
        self.db = await aiosqlite.connect(self.dbname)
        await self.db.execute('CREATE TABLE IF NOT EXISTS json (id TEXT, value BIGTEXT)')
        await self.db.commit()

    async def add(self, query: str, value: int):
        async with self.db.execute("SELECT value FROM json WHERE id = ?", [query]) as cursor:
            result = await cursor.fetchone()
            if result is None:
                await self.db.execute("INSERT INTO json VALUES (?, ?)", [query, value])
            else:
                newValue = int(result[0]) + value
                await self.db.execute("UPDATE json SET value = ? WHERE id = ?", [newValue, query])
            await self.db.commit()

    async def set(self, query: str, value):
        await self.db.execute("REPLACE INTO json VALUES (?, ?)", [query, value])
        await self.db.commit()

    async def get(self, query: str):
        async with self.db.execute("SELECT value FROM json WHERE id = ?", [query]) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

    async def subtract(self, query: str, value: int):
        async with self.db.execute("SELECT value FROM json WHERE id = ?", [query]) as cursor:
            result = await cursor.fetchone()
            if result is None:
                await self.db.execute("INSERT INTO json VALUES (?, ?)", [query, -value])
            else:
                newValue = int(result[0]) - value
                await self.db.execute("UPDATE json SET value = ? WHERE id = ?", [newValue, query])
            await self.db.commit()

    async def fetch(self, query: str):
        async with self.db.execute(f"SELECT value FROM json WHERE id LIKE '{query}~%'") as cursor:
            return [row[0] for row in await cursor.fetchall()]

    async def has(self, query: str):
        async with self.db.execute("SELECT value FROM json WHERE id = ?", [query]) as cursor:
            return await cursor.fetchone() is not None

    async def all(self):
        async with self.db.execute("SELECT * FROM json") as cursor:
            return await cursor.fetchall()

    async def delete(self, query: str):
        await self.db.execute("DELETE FROM json WHERE id = ?", [query])
        await self.db.commit()

    async def push(self, query: str, value: str):
        async with self.db.execute(f"SELECT * FROM json WHERE id LIKE '{query}~%'") as cursor:
            length = len(await cursor.fetchall())
            await self.set(f'{query}~{length}', value)

    async def pull(self, query: str, value: str):
        await self.db.execute(f"DELETE FROM json WHERE id LIKE '{query}~%' AND value = '{value}'")
        await self.db.commit()
