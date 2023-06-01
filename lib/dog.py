import sqlite3


class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None

    @classmethod
    def create_table(cls):
        conn = sqlite3.connect('dog.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS dogs 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    breed TEXT)''')

        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        conn = sqlite3.connect('dog.db')
        c = conn.cursor()

        c.execute('DROP TABLE IF EXISTS dogs')

        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect('dog.db')
        c = conn.cursor()

        c.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)', (self.name, self.breed))
        self.id = c.lastrowid

        conn.commit()
        conn.close()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        conn = sqlite3.connect('dog.db')
        c = conn.cursor()

        c.execute('SELECT * FROM dogs')
        rows = c.fetchall()

        dogs = []
        for row in rows:
            dog = cls.new_from_db(row)
            dogs.append(dog)

        conn.close()
        return dogs

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('dog.db')
        c = conn.cursor()

        c.execute('SELECT * FROM dogs WHERE name = ?', (name,))
        row = c.fetchone()

        if row:
            dog = cls.new_from_db(row)
        else:
            dog = None

        conn.close()
        return dog

    @classmethod
    def find_by_id(cls, id):
        conn = sqlite3.connect('dog.db')
        c = conn.cursor()

        c.execute('SELECT * FROM dogs WHERE id = ?', (id,))
        row = c.fetchone()

        if row:
            dog = cls.new_from_db(row)
        else:
            dog = None

        conn.close()
        return dog
