
import sqlite3 as sq

async def db_connect():
    global db_cloths, db_wardrobe, cur_cloths, cur_wardrobe

    db_cloths = sq.connect('cloths.db')
    db_wardrobe = sq.connect('wardrobe.db')
    cur_cloths = db_cloths.cursor()
    cur_wardrobe = db_wardrobe.cursor()

    # Create 'wardrobe' table if it doesn't exist
    cur_wardrobe.execute("CREATE TABLE IF NOT EXISTS wardrobe(temp TEXT PRIMARY KEY, description TEXT)")
    db_wardrobe.commit()

async def cloth(condition):
    with sq.connect("cloths.db") as con:
        temperature = round(condition)
        cur = con.cursor()
        if temperature> 0:
            cur.execute(f"SELECT `Field2` FROM `cloths` WHERE ( ({temperature} - Field1 ) <= 2 ) LIMIT 1")
        else:
            cur.execute(f"SELECT `Field2` FROM `cloths` WHERE ( ({temperature} + Field1 ) <= -2 ) LIMIT 1")
        result = cur.fetchall()
        return result[0][0]