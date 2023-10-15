import sqlite3 as sq

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