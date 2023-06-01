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
        try:
            Dog.CURSOR = conn.cursor()  # Assign the CURSOR attribute
            Dog.CURSOR.execute('''CREATE TABLE IF NOT EXISTS dogs 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                breed TEXT)''')
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def drop_table(cls):
        conn = sqlite3.connect('dog.db')
        try:
            Dog.CURSOR = conn.cursor()  # Assign the CURSOR attribute
            Dog.CURSOR.execute('DROP TABLE IF EXISTS dogs')
            conn.commit()
        finally:
            conn.close()

    def save(self):
        conn = sqlite3.connect('dog.db')
        try:
            Dog.CURSOR = conn.cursor()  # Assign the CURSOR attribute
            Dog.CURSOR.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)', (self.name, self.breed))
            self.id = Dog.CURSOR.lastrowid
            conn.commit()
        finally:
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
        try:
            Dog.CURSOR = conn.cursor()  # Assign the CURSOR attribute
            Dog.CURSOR.execute('SELECT * FROM dogs')
            rows = Dog.CURSOR.fetchall()

            dogs = []
            for row in rows:
                dog = Dog.new_from_db(row)
                dogs.append(dog)
        finally:
            conn.close()

        return dogs

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('dog.db')
        try:
            Dog.CURSOR = conn.cursor()  # Assign the CURSOR attribute
            Dog.CURSOR.execute('SELECT * FROM dogs WHERE name = ?', (name,))
            row = Dog.CURSOR.fetchone()

            if row:
                dog = Dog.new_from_db(row)
            else:
                dog = None
        finally:
            conn.close()

        return dog

    @classmethod
    def find_by_id(cls, id):
        conn = sqlite3.connect('dog.db')
        try:
            Dog.CURSOR = conn.cursor()  # Assign the CURSOR attribute
            Dog.CURSOR.execute('SELECT * FROM dogs WHERE id = ?', (id,))
            row = Dog.CURSOR.fetchone()

            if row:
                dog = Dog.new_from_db(row)
            else:
                dog = None
        finally:
            conn.close()

        return dog

    def update(self):
        conn = sqlite3.connect('dog.db')
        try:
            Dog.CURSOR = conn.cursor()  # Assign the CURSOR attribute
            Dog.CURSOR.execute('UPDATE dogs SET name = ?, breed = ? WHERE id = ?', (self.name, self.breed, self.id))
            conn.commit()
        finally:
            conn.close()
