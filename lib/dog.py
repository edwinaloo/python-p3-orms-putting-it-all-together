import sqlite3


class Dog:
    CURSOR = None  # Define the CURSOR attribute

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None

    @classmethod
    def create_table(cls):
        conn = sqlite3.connect('dog.db')
        cls.CURSOR = conn.cursor()  # Assign the CURSOR attribute
        cls.CURSOR.execute('''CREATE TABLE IF NOT EXISTS dogs 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            breed TEXT)''')

        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        conn = sqlite3.connect('dog.db')
        cls.CURSOR = conn.cursor()  # Assign the CURSOR attribute
        cls.CURSOR.execute('DROP TABLE IF EXISTS dogs')

        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect('dog.db')
        self.CURSOR = conn.cursor()  # Assign the CURSOR attribute

        self.CURSOR.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)', (self.name, self.breed))
        self.id = self.CURSOR.lastrowid

        conn.commit()
        conn.close()

    @classmethod
    def create(cls, name, breed):
        self = cls(name, breed)  # Use 'self' instead of 'dog'
        self.save()
        return self

    @classmethod
    def new_from_db(cls, row):
        self = cls(row[1], row[2])  # Use 'self' instead of 'dog'
        self.id = row[0]
        return self

    @classmethod
    def get_all(cls):
        conn = sqlite3.connect('dog.db')
        cls.CURSOR = conn.cursor()  # Assign the CURSOR attribute

        cls.CURSOR.execute('SELECT * FROM dogs')
        rows = cls.CURSOR.fetchall()

        dogs = []
        for row in rows:
            dog = cls.new_from_db(row)
            dogs.append(dog)

        conn.close()
        return dogs

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('dog.db')
        cls.CURSOR = conn.cursor()  # Assign the CURSOR attribute

        cls.CURSOR.execute('SELECT * FROM dogs WHERE name = ?', (name,))
        row = cls.CURSOR.fetchone()

        if row:
            dog = cls.new_from_db(row)
        else:
            dog = None

        conn.close()
        return dog

    @classmethod
    def find_by_id(cls, id):
        conn = sqlite3.connect('dog.db')
        cls.CURSOR = conn.cursor()  # Assign the CURSOR attribute

        cls.CURSOR.execute('SELECT * FROM dogs WHERE id = ?', (id,))
        row = cls.CURSOR.fetchone()

        if row:
            dog = cls.new_from_db(row)
        else:
            dog = None

        conn.close()
        return dog

    def update(self):
        conn = sqlite3.connect('dog.db')
        self.CURSOR = conn.cursor()  # Assign the CURSOR attribute

        self.CURSOR.execute('UPDATE dogs SET name = ?, breed = ? WHERE id = ?', (self.name, self.breed, self.id))

        conn.commit()
        conn.close()
