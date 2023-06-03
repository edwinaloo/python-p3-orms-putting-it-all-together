import sqlite3

class Dog:
    @classmethod
    def create_table(cls):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def drop_table(cls):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS dogs")

        conn.commit()
        cursor.close()
        conn.close()

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  # Initialize id as None initially

    def save(self):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE dogs SET name = ?, breed = ? WHERE id = ?", (self.name, self.breed, self.id))

        conn.commit()
        cursor.close()
        conn.close()

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
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM dogs")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM dogs WHERE name = ?", (name,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is not None:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        conn = sqlite3.connect("dogs.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM dogs WHERE id = ?", (id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is not None:
            return cls.new_from_db(row)
        return None

    # Bonus methods
    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog is None:
            dog = cls.create(name, breed)
        return dog

    def update(self):
        old_name = self.name
        self.save()
        updated_dog = Dog.find_by_name(old_name)
        return updated_dog
