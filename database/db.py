import aiosqlite
from pathlib import Path
from utils.logger import logger

DB_PATH = None

def set_db_path(path: str):
    global DB_PATH
    DB_PATH = path
    Path(path).parent.mkdir(parents=True, exist_ok=True)

async def get_connection():
    if DB_PATH is None:
        raise RuntimeError("Database path not set. Call set_db_path() first.")
    return await aiosqlite.connect(DB_PATH)

async def init_db():
    conn = await get_connection()
    try:
        await conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language TEXT DEFAULT 'es',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
                content TEXT NOT NULL,
                flow TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS user_context (
                user_id INTEGER PRIMARY KEY,
                current_flow TEXT,
                profile_type TEXT,
                tech_area TEXT,
                goal TEXT,
                target_company TEXT,
                target_person TEXT,
                pipeline_data TEXT,
                emotional_blocks TEXT,
                metadata TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                company TEXT,
                person_name TEXT,
                channel TEXT,
                last_touch TIMESTAMP,
                delivered TEXT,
                next_action TEXT,
                due_date TEXT,
                status TEXT DEFAULT 'identified',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            CREATE INDEX IF NOT EXISTS idx_conversations_user
                ON conversations(user_id);
            CREATE INDEX IF NOT EXISTS idx_conversations_flow
                ON conversations(flow);
            CREATE INDEX IF NOT EXISTS idx_opportunities_user
                ON opportunities(user_id);
            CREATE INDEX IF NOT EXISTS idx_opportunities_status
                ON opportunities(status);
        """)
        await conn.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    finally:
        await conn.close()

async def get_or_create_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None):
    conn = await get_connection()
    try:
        cursor = await conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        user = await cursor.fetchone()
        if not user:
            await conn.execute(
                """INSERT INTO users (user_id, username, first_name, last_name)
                   VALUES (?, ?, ?, ?)""",
                (user_id, username, first_name, last_name)
            )
            await conn.commit()
            logger.info(f"New user created: {user_id} ({username})")
        else:
            if username or first_name or last_name:
                await conn.execute(
                    """UPDATE users SET username=?, first_name=?, last_name=?,
                       updated_at=CURRENT_TIMESTAMP WHERE user_id=?""",
                    (username, first_name, last_name, user_id)
                )
                await conn.commit()
    finally:
        await conn.close()

async def save_message(user_id: int, role: str, content: str, flow: str = None):
    conn = await get_connection()
    try:
        await conn.execute(
            "INSERT INTO conversations (user_id, role, content, flow) VALUES (?, ?, ?, ?)",
            (user_id, role, content, flow)
        )
        await conn.commit()
    finally:
        await conn.close()

async def get_conversation_history(user_id: int, limit: int = 20):
    conn = await get_connection()
    try:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            """SELECT role, content, flow, created_at
               FROM conversations
               WHERE user_id = ?
               ORDER BY created_at DESC
               LIMIT ?""",
            (user_id, limit)
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in reversed(rows)]
    finally:
        await conn.close()

async def get_user_context(user_id: int) -> dict:
    conn = await get_connection()
    try:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            "SELECT * FROM user_context WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else {}
    finally:
        await conn.close()

async def set_user_context(user_id: int, **kwargs):
    conn = await get_connection()
    try:
        existing = await get_user_context(user_id)
        import json
        if existing:
            fields = []
            values = []
            for k, v in kwargs.items():
                if k in ('metadata', 'pipeline_data', 'emotional_blocks'):
                    v = json.dumps(v) if isinstance(v, (dict, list)) else v
                fields.append(f"{k} = ?")
                values.append(v)
            values.append(user_id)
            await conn.execute(
                f"UPDATE user_context SET {', '.join(fields)}, updated_at=CURRENT_TIMESTAMP WHERE user_id=?",
                values
            )
        else:
            keys = ['user_id']
            vals = [user_id]
            for k, v in kwargs.items():
                if k in ('metadata', 'pipeline_data', 'emotional_blocks'):
                    v = json.dumps(v) if isinstance(v, (dict, list)) else v
                keys.append(k)
                vals.append(v)
            placeholders = ', '.join(['?'] * len(keys))
            await conn.execute(
                f"INSERT INTO user_context ({', '.join(keys)}) VALUES ({placeholders})",
                vals
            )
        await conn.commit()
    finally:
        await conn.close()

async def clear_conversation(user_id: int):
    conn = await get_connection()
    try:
        await conn.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
        await conn.execute("DELETE FROM user_context WHERE user_id = ?", (user_id,))
        await conn.commit()
        logger.info(f"Conversation cleared for user {user_id}")
    finally:
        await conn.close()
