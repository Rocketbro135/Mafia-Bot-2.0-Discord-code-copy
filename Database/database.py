import sqlite3

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('discord_bot_db.sqlite')
        print('SQLite version:', sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    try:
        sql_create_gamemodes_table = """
        CREATE TABLE IF NOT EXISTS gamemodes (
            guild_id INTEGER PRIMARY KEY,
            current_gamemode TEXT
            dm_time INTEGER,
            talk_time INTEGER,
            show_dead_role INTEGER 
        );
        """
        
        cursor = conn.cursor()
        cursor.execute(sql_create_gamemodes_table)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def fetch_game_settings(conn, guild_id):
    sql = "SELECT * FROM gamemodes WHERE guild_id = ?;"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (guild_id)) #(guild_id,)
        return cursor.fetchone()  # Only returns the first match, `fetchall()` can be used to get all matching records
    except sqlite3.Error as e:
        print(e)

def update_game_settings(conn, guild_id, current_gamemode, dm_time, talk_time, show_dead_role):
    sql = """INSERT OR REPLACE INTO gamemodes
             (guild_id, current_gamemode, dm_time, talk_time, show_dead_role)
             VALUES
             (?, ?, ?, ?, ?);"""
    
    try:
        cur = conn.cursor()
        cur.execute(sql, (guild_id, current_gamemode, dm_time, talk_time, show_dead_role))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

conn = create_connection()
if conn is not None:
    create_tables(conn)

