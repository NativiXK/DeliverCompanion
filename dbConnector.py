import sqlite3, time

class Connector:

    def __init__(self, db_name) -> None:
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()
        self.__create_table()
        
    @property
    def cursor(self) -> object:
        return self.__cursor

    def __create_table(self) -> None:
        self.cursor.execute("""
        SELECT count(name) FROM sqlite_master WHERE type='table' AND name='keys'
        """)
        if self.cursor.fetchone()[0] == 1:
            print("Table already exists")
        else:
            self.cursor.execute("""
            CREATE TABLE keys (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                key VARCHAR(44) NOT NULL,
                registrado_em DATE NOT NULL
            );
            """)

    def register(self, danfe_key : str):
        self.cursor.execute(f"""
        INSERT INTO keys (key, registrado_em) 
        VALUES ("{danfe_key}", {time.time()})
        """)
        self.__conn.commit()

    def delete(self, danfe_key : str):
        self.cursor.execute(f"""
        DELETE FROM keys WHERE key="{danfe_key}";        
        """)
        self.__conn.commit()

    def retrieve_all_keys(self):
        self.cursor.execute("""
        SELECT key FROM keys;
        """)

        keys = self.cursor.fetchall()

        return [i[0] for i in keys]

if __name__ == "__main__":
    db = Connector('danfes.db')
    db.register("31210106347409006953550060009454751196026791")
    db.register("31210106347409006953550060009454751196226791")
    for i in db.retrieve_all_keys():
        print(i)
    db.delete("31210106347409006953550060009454751196026791")
    db.delete("31210106347409006953550060009454751196226791")
    