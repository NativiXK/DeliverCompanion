import sqlite3, time

class Connector:

    def __init__(self) -> None:
        self.__cursor = sqlite3.connect('danfes.db').cursor()
        
    @property
    def cursor(self) -> object:
        return self.__cursor

    def __create_table(self) -> None:
        self.cursor.execute("""
        SELECT count(name) FROM sqlite_master WHERE type='table' AND name='key'
        """)
        if self.cursor.fetchone()[0] == 1:
            print("Table already exists")
        else:
            self.cursor.execute("""
            CREATE TABLE keys (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                registrado_em DATE NOT NULL
            );
            """)

    def register(self, danfe_key):
        self.cursor.execute(f"""
        INSERT INTO keys (key, registrado_em) 
        VALUES {danfe_key}, {time.time()}
        """)

if __name__ == "__main__":
    db = Connector()
    print(db)