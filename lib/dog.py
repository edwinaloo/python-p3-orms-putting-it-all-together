import sqlite3

class Dog:
    @classmethod
    def create_table(cls):
        CONN = sqlite3.connect("dogs.db")
        CURSOR = CONN.cursor()

        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """)

        CONN.commit()
        CURSOR.close()
        CONN.close()

    @classmethod
    def drop_table(cls):
        CONN = sqlite3.connect("dogs.db")
        CURSOR = CONN.cursor()

        CURSOR.execute("DROP TABLE IF EXISTS dogs")

        CONN.commit()
        CURSOR.close()
        CONN.close()

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  # Initialize id as None initially

    def save(self):
        CONN = sqlite3.connect("dogs.db")
        CURSOR = CONN.cursor()

        if self.id is None:
            CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute("UPDATE dogs SET name = ?, breed = ? WHERE id = ?", (self.name, self.breed, self.id))

        CONN.commit()
        CURSOR.close()
        CONN.close()

    @classmethod
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        CONN = sqlite3.connect("dogs.db")
        CURSOR = CONN.cursor()

        CURSOR.execute("SELECT * FROM dogs")
        rows = CURSOR.fetchall()

        CURSOR.close()
        CONN.close()

        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        CONN = sqlite3.connect("dogs.db")
        CURSOR = CONN.cursor()

        CURSOR.execute("SELECT * FROM dogs WHERE name = ?", (name,))
        row = CURSOR.fetchone()

        CURSOR.close()
        CONN.close()

        if row is not None:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        CONN = sqlite3.connect("dogs.db")
        CURSOR = CONN.cursor()

        CURSOR.execute("SELECT * FROM dogs WHERE id = ?", (id,))
        row = CURSOR.fetchone()

        CURSOR.close()
        CONN.close()

        if row is not None:
            return cls.new_from_db(row)
        return None

    # Bonus methods (uncomment tests in the pytest file to run)
    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog is None:
            dog = cls.create(name, breed)
        return dog

    def update(self):
        old_name = self.name
        self.name = old_name
        self.save()
        updated_dog = Dog.find_by_name(old_name)
        return updated_dog
